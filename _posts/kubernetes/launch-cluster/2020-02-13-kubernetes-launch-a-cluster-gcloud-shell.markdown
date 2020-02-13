---
layout: page
title: "kubernetes > launch a cluster with kubeadm and gcloud shell"
date: 2020-02-13 07:56:00 +0530
categories: kubernetes gcp
---

Task: Create a Kubernetes cluster using VMs with kubeadm, not GKE

OS on all the instances: Ubuntu 1804

We would execute all the commands on the Google cloud shell

Click the cloud shell icon (>_) at the top right corner of the Google cloud dashboard

***Set region and zone***
```
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a
```

***To create a kubernetes master instance and 3 node instances, all with ubuntu 1804***
```
gcloud compute instances create k8s-master --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud --custom-cpu=2 --custom-memory=4
gcloud compute instances create k8s-node1 --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud
gcloud compute instances create k8s-node2 --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud
gcloud compute instances create k8s-node3 --image-family ubuntu-1804-lts --image-project ubuntu-os-cloud
```

***Prepare Docker installation file***
```
nano  install-docker.sh  # keep the following contents inside this file
```
```
sudo su
groupadd docker
usermod -aG docker $USER
# Install Docker CE
## Set up the repository:
### Install packages to allow apt to use a repository over HTTPS
apt-get update -y && apt-get install apt-transport-https ca-certificates curl software-properties-common -y

### Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add --

### Add Docker apt repository.
add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"

## Install Docker CE.
apt-get update -y && apt-get install docker-ce=18.06.2~ce~3-0~ubuntu -y

# Setup daemon.
cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF

mkdir -p /etc/systemd/system/docker.service.d

# Restart docker.
systemctl daemon-reload
systemctl restart docker
```
***Install Docker on all the instances***
```
cat install-docker.sh | gcloud compute ssh k8s-master
cat install-docker.sh | gcloud compute ssh k8s-node1
cat install-docker.sh | gcloud compute ssh k8s-node2
cat install-docker.sh | gcloud compute ssh k8s-node3
```

***Prepare Kuberenetes repos file***
```
nano add-k8s-repos.sh  # add the following contents in this file
```
```
sudo su 
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add --
cat <<EOF > /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update -y
```

***Add Kubernetes repos on all the instances***
```
cat add-k8s-repos.sh | gcloud compute ssh k8s-master
cat add-k8s-repos.sh | gcloud compute ssh k8s-node1
cat add-k8s-repos.sh | gcloud compute ssh k8s-node2
cat add-k8s-repos.sh | gcloud compute ssh k8s-node3
```

***Prepare kubeadm and kubelet installation file***
```
cat > install-kubeadm-kubelet.sh <<EOF
sudo apt-get install -y kubeadm kubelet
sudo apt-mark hold kubeadm kubect
EOF
```

***Install kubeadm and kubelet on all instances***
```
cat install-kubeadm-kubelet.sh | gcloud compute ssh k8s-master
cat install-kubeadm-kubelet.sh | gcloud compute ssh k8s-node1
cat install-kubeadm-kubelet.sh | gcloud compute ssh k8s-node2
cat install-kubeadm-kubelet.sh | gcloud compute ssh k8s-node3
```

***Prepare kubectl installation file***
```
cat > install-kubectl.sh <<EOF
sudo apt-get install -y kubectl
sudo apt-mark hold kubectl
EOF
```

***Install kubectl on master***
```
cat install-kubectl | gcloud compute ssh k8s-master
```

***Initialize the control plane a.k.a master***
```
echo "sudo kubeadm init --pod-network-cidr=192.168.0.0/16" | gcloud compute ssh k8s-master
```

Note down the final two lines of the output, that has the token information, for example
```
kubeadm join 10.128.0.4:6443 --token wznnx1.zkjl7tjgvc7tj5xw \
--discovery-token-ca-cert-hash sha256:bebca8ab84f7f8545e30b3334d0d77793afbf032b05a9e6a8c4fb80fb367b9a1
```

***Prepare kubeconfig setup file***
```
cat > setup-kubeconfig.sh <<EOF
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
EOF
```

***Setup kubeconfig on  the master***
```
cat setup-kubeconfig.sh | gcloud compute ssh k8s-master
```

***Prepare pod networking setup file, here we have chosen Calico plugin***
```
cat > setup-pod-networking.sh <<EOF
kubectl apply -f https://docs.projectcalico.org/v3.3/getting-started/kubernetes/installation/hosted/rbac-kdd.yaml
kubectl apply -f https://docs.projectcalico.org/v3.3/getting-started/kubernetes/installation/hosted/kubernetes-datastore/calico-networking/1.7/calico.yaml
EOF
```

***Setup Pod networking for the cluster***
```
cat setup-pod-networking.sh | gcloud compute ssh k8s-master
```

***Prepare a file with token information for adding nodes to the cluster, this step refers to the token copied few steps back***
```
cat > join-nodes-to-cluster.sh <<EOF
sudo kubeadm join 10.128.0.4:6443 --token wznnx1.zkjl7tjgvc7tj5xw \
--discovery-token-ca-cert-hash sha256:bebca8ab84f7f8545e30b3334d0d77793afbf032b05a9e6a8c4fb80fb367b9a1
```

***Add nodes to the cluster***
```
cat join-nodes-to-cluster.sh | gcloud compute ssh k8s-node1
cat join-nodes-to-cluster.sh | gcloud compute ssh k8s-node2
cat join-nodes-to-cluster.sh | gcloud compute ssh k8s-node3
```

***SSH into the master and start working***
```
gcloud compute ssh k8s-master

shakir@k8s-master:~ kubectl get nodes
NAME STATUS ROLES AGE VERSION
k8s-master Ready master 140m v1.15.2
k8s-node1 Ready 119m v1.15.2
k8s-node2 Ready 119m v1.15.2
k8s-node3 Ready 119m v1.15.2
```

--end-of-post--

