---
#title: kubernetes > bootstrap cluster in aws with kubeadm
#categories: kubernetes
---

In this post, we would be installing the cluster in AWS with kubeadm, so please ensure the [prerequisites](\kubernetes-prerequisites-for-cluster-in-aws) are set.


## Allow Bridged Traffic
Check if the module br_netfilter is loaded

```
$ ips=$(<k8s-node-ips.txt)

$ for ip in $ips; do ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip "lsmod | grep br_netfilter"; done 
```

if it was loaded, we should get an ouptut like this
```
br_netfilter           24576  0
bridge                172032  1 br_netfilter
```

Since it's not loaded we can load it.
```
$ cat load-br-netfilter.sh 
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
br_netfilter
EOF

sudo modprobe br_netfilter

$ for ip in $ips; do cat load-br-netfilter.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip; done
```

Verify
```
$ for ip in $ips; do ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip "lsmod | grep br_netfilter"; done 
br_netfilter           28672  0
bridge                249856  1 br_netfilter
br_netfilter           28672  0
bridge                249856  1 br_netfilter
br_netfilter           28672  0
bridge                249856  1 br_netfilter
```

We need to now let iptables see bridged traffic.
```
$ cat allow-bridge-iptables.sh 
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
sudo sysctl --system

$ for ip in $ips; do cat allow-bridge-iptables.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip; done
```

## Container runtime
I am choosing [Docker](https://docs.docker.com/engine/install/ubuntu/), as its commonly used, let's install it.
```
$ cat install-docker.sh 
sudo apt-get update -y
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update -y
sudo apt-get install docker-ce docker-ce-cli containerd.io -y

$ for ip in $ips; do cat install-docker.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip; done
```

Setup systemd as the container cgroup driver.
```
$ cat systemd-docker.sh 
sudo mkdir /etc/docker
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

$ for ip in $ips; do cat systemd-docker.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip; done
```

Enable docker to automatically start during reboots, and restart it.
```
$ cat restart-docker.sh
sudo systemctl enable docker
sudo systemctl daemon-reload
sudo systemctl restart docker

$ for ip in $ips; do cat restart-docker.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip; done
```

## Add the kubernetes repo
We need to add the kubernetes repo to install kubeadm, kubelet and kubectl from there.
```
$ cat add-k8s-repo.sh 
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update -y

$ for ip in $ips; do cat restart-docker.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip; done
```

## kubectl
We have added the repo to the kubernetes nodes, however we also need it in the local machine for installing kubectl. The machine from which I want to use kubectl runs on Amazon Linux, hence I will go with yum based installation. Note: if your machine is Ubuntu, you can run the same script above on your local machine too.
```
$ cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-\$basearch
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
exclude=kubelet kubeadm kubectl
EOF
```

We can now install kubectl.
```
$ sudo yum install -y kubectl --disableexcludes=kubernetes
```

## kubeadm and kubelet

Install kubeadm and kubelet on kubernetes nodes.
```
$ cat > install-kubeadm-kubelet.sh <<EOF                                                                                     
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
EOF

$ for ip in $ips; do cat install-kubeadm-kubelet.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip; done
```

## Bootstrap cluster
We can now initialze the clluster from the master node. First init the cluster with a subnet for the pod network.
```
$ ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$K8S_MASTER_IP "sudo kubeadm init --pod-network-cidr=192.168.0.0/16
```

Before joining the nodes, allow the port 6443 on the security group.
```
$ aws ec2 authorize-security-group-ingress --group-id $KUBEADM_SG_ID --protocol tcp --port 6443 --cidr 10.0.0.0/28
```
6443 is used on the api server on the master node, and hence we need to allow ingress traffic to the master, from other nodes in the cluster, and 10.0.0.0/28 is the subnet where all the nodes including the master are launched.


You should see the join command, as part of the output, once the control plane is initiated successfully. Execute that command on the worker nodes.
```
$ cat > kubeadm-join.sh <<EOF                                                                                                
sudo kubeadm join 10.0.0.9:6443 --token ******* \
     --discovery-token-ca-cert-hash sha256:***************
EOF

$ cat kubeadm-join.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$K8S_NODE1_IP
$ cat kubeadm-join.sh | ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$K8S_NODE2_IP
```

## kubeconfig

The nodes have now joined the cluster, we need to setup kubeconfig on the machine from which we can run kubebctl commands to access the kubernetes cluster.

Login to the master
```
$ ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$K8S_MASTER_IP
```

The kubeconfig gets generated and saved in the master, during the control plane  initialization, we can copy the config from the default location and save it in the location wehere kubectl reads the config.
```
mkdir -p ~/.kube
sudo cp /etc/kubernetes/admin.conf ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config

$ ls ~/.kube/config
/home/ec2-user/.kube/config
```

## Network addon
We have to setup a network addon for which we can choose [calico](https://projectcalico.docs.tigera.io/getting-started/kubernetes/quickstart)
```
kubectl create -f https://docs.projectcalico.org/manifests/tigera-operator.yaml
kubectl create -f https://docs.projectcalico.org/manifests/custom-resources.yaml
```

All the nodes are now ready.
```
$ kubectl get nodes
NAME                                     STATUS   ROLES                  AGE     VERSION
ip-10-0-0-4.us-east-2.compute.internal   Ready    <none>                 117s    v1.22.4
ip-10-0-0-6.us-east-2.compute.internal   Ready    <none>                 2m18s   v1.22.4
ip-10-0-0-9.us-east-2.compute.internal   Ready    control-plane,master   3m29s   v1.22.4
```

## Allow other ports
There are certain other ports that we need to allow on the security group, for proper communication  in the kubernetes cluster. Execute these on your machine where aws cli is configured.
```
# kubelet
$ aws ec2 authorize-security-group-ingress --group-id $KUBEADM_SG_ID --protocol tcp --port 10250 --cidr 10.0.0.0/28

# nodeport services
$ aws ec2 authorize-security-group-ingress --group-id $KUBEADM_SG_ID --protocol tcp --port 30000-32767 --cidr 10.0.0.0/28

# etcd
$ aws ec2 authorize-security-group-ingress --group-id $KUBEADM_SG_ID --protocol tcp --port 2379-2380 --cidr 10.0.0.0/28{

# kube-scheduler
$ aws ec2 authorize-security-group-ingress --group-id $KUBEADM_SG_ID --protocol tcp --port 10259 --cidr 10.0.0.0/28

# kube-controll-manager
$ aws ec2 authorize-security-group-ingress --group-id $KUBEADM_SG_ID --protocol tcp --port 10257 --cidr 10.0.0.0/2
```


## Init
Initialize control plane with kubeadm

```
$ cat > kubeadm-init-config <<EOF
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
networking:
  podSubnet: "192.168.0.0/16"
apiServer:
  extraArgs:
    cloud-provider: "aws"
controllerManager:
  extraArgs:
    cloud-provider: "aws"
EOF
```

```
$ scp -i ~/.ssh/kubeadmKeyPair.pem kubeadm-init-config ubuntu@$K8S_MASTER_IP:~/kubeadm-init-config
```

```
$ ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$K8S_MASTER_IP "sudo kubeadm init --config kubeadm-init-config"
```

## Join Node1
```
ubuntu@ip-10-0-0-6:~$ cat > kubeadm-join-config <<EOF
apiVersion: kubeadm.k8s.io/v1beta3
kind: JoinConfiguration
discovery:
  bootstrapToken:
    token: tfu3n6.pg2j5ms8ecnfsgwg
    apiServerEndpoint: "10.0.0.9:6443"
    caCertHashes:
      - "sha256:97c5c01cbcb8bd802fc05a3d26cb9e9fb8126ecd2cc18d3f4504daeab54b23ec"
nodeRegistration:
  name: ip-10-0-0-6.us-east-2.compute.internal
  kubeletExtraArgs:
    cloud-provider: aws
    
ubuntu@ip-10-0-0-6:~$ sudo kubeadm join --config kubeadm-join-config 
```

## Join Node2
