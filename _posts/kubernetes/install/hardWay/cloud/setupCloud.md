### Prerequisites:
- Google cloud platform
- Google cloud shell
- Linux
- IP address subnetting

### Environment: 
This exercise could be carried out on the Google cloud shell, or a Linux machine on which gcloud is installed

### Reference: 
https://github.com/kelseyhightower/kubernetes-the-hard-way

---

We are gonna install a Kubernetes HA cluster the hardway, on Google cloud platform, without bootstrapping tools such as kubeadm or RKE

> If you are doing this from your own machine instead of gcloud shell, please login first to GCP using 'gcloud auth login'

### Create a new project, and set it as the active project
```
networkandcode@Linux:~$ gcloud projects create k8s-hard-way-nc
```
> Project IDs are globally unique, so create a unique project ID, or skip this step, if you want to use an existing project, here I have used k8s-hard-way-nc. You also need to enable billing for a new project through the [API consle](https://console.developers.google.com/billing/projects) -- click on the 3 dots icon to the right of the project name - Change billing - Set Account

### Set Defaults on Google cloud
```
networkandcode@Linux:~$ cat > setDefaults.sh <<EOF
gcloud config set project k8s-hard-way-nc
gcloud config set compute/region asia-south1
gcloud config set compute/region asia-south1-a
EOF
networkandcode@Linux:~$ chmod +x setDefaults.sh 
networkandcode@Linux:~$ ./setDefaults.sh 
```
> You set the project, region and zone of choice. The list of existing projects, regions, and zones could be checked using ```gcloud projects list```, ```gcloud compute regions list```, and ```gcloud compute zones list``` respectively

### Install kubectl
```
networkandcode@Linux:~$ wget https://storage.googleapis.com/kubernetes-release/release/v1.15.3/bin/linux/amd64/kubectl
networkandcode@Linux:~$ chmod +x kubectl 
networkandcode@Linux:~$ sudo mv kubectl /usr/local/bin
```
> We are installing version 1.15.3 here

### Reserve a static public / external IP, that would be later used to expose the kube-apiserver to the Internet
```
networkandcode@Linux:~$ gcloud compute addresses create kube-apiserver --region asia-south1
```
> Hit 'y' to enable billing

### Launch masters and nodes for the cluster
Kubernetes is a distributed system which means different software components of Kubernetes are going to be installed. A Kubernetes cluster should have atleast one master instance and one node instance. It's also possible to have an all-in-one installation with a single instance acting as both master and node, however that's recommended only for limited testing and learning. The master instances are collectively referred to as the control plane of the cluster, and the nodes are where the actual Kubernetes workloads such as Pods, Deployments would be launched, except few exceptions though. Our setup is going to contain 3 masters and 5 nodes. Since this setup has more than 1 master, its referred to as a HA(High Availability) setup

Launch 3 masters
```
networkandcode@Linux:~$ cat > launchMasters.sh <<EOF 
for i in 0 1 2; do
    gcloud compute instances create master-${i} \
    --image-family ubuntu-1804-lts \
    --image-project ubuntu-os-cloud
done
EOF

networkandcode@Linux:~$ chmod +x launchMasters.sh

networkandcode@Linux:~$ ./launchMasters.sh
```

Launch 5 nodes
```
networkandcode@Linux:~$ cat > launchNodes.sh <<EOF
for i in {0..4}; do
    gcloud compute instances create node-${i} \
    --image-family ubuntu-1804-lts \
    --image-project ubuntu-os-cloud \
    --metadata pod-cidr=192.168.${i}.0/24
done
EOF

networkandcode@Linux:~$ chmod +x launchNodes.sh

networkandcode@Linux:~$ ./launchNodes.sh
```
> We have given a metada to the nodes that identfies the network for Pods that are to be launched in that node, for this setup we are using the IP subnet 192.168.0.0/16 for the overall cluster, and this network could be broken into multiple /24 subnets i.e. 192.168. 0 - 255 . 0/24. CIDR refers to classless inter-domain routing, which means even though /16 is the default prefix for class A (10.x.x.x) networks (with classful addressing) we have used that prefix with a class C network (192.168.x.x), this is called classless addressing

### Try to access the masters and nodes through SSH
```
networkandcode@Linux:~$ cat > testConnectivity.sh <<EOF
echo 'Checking connection to masters'

for i in {0..2}; do
    exit | gcloud compute ssh master-${i}
    echo 'connection successful to master-${i}'
done

echo 'Checking connection to nodes'
for i in {0..4}; do
    exit | gcloud compute ssh node-${i}
    echo 'connection successful to node-${i}'
done
EOF

chmod +x testConnectivity.sh
./testConnectivity.sh
```

### Create firewall rules
We need to allow all TCP, UDP, and ICMP access between Pods and Nodes. The subnet we have chosen for the Pods is 192.168.0.0/16 and the subnet chosen for the nodes is the default subnet provided by Google cloud
```
networkandcode@Linux:~$ gcloud compute firewall-rules create pods-to-nodes --allow tcp,udp,icmp --source-ranges 192.168.0.0/16
```
> We don't have to attach the firewall rule to a specific node subnet cause the nodes are using the default subnet

We need another rule to allow TCP ports 22 (SSH), 6443 (HTTPS port of the kube-apiserver), and ICMP from external clients on the Internet to the public / external IPs of the nodes
```
networkandcode@Linux:~/tech/kubernetes/cka/installation$ gcloud compute firewall-rules create internet-to-nodes --allow tcp:22,tcp:6443,icmp --source-ranges 0.0.0.0/0
```
> Note that ICMP is a protocol generally used to test reachability to an IP address, the utility 'ping' uses ICMP. The IP 0.0.0.0/0 means any IP address/network. This means that any IP address either internal / external would be allowed to access the nodes on the ports/protocols mentioned


### To stop all instances to avoid costs
```
networkandcode@Linux:~$ cat > stopInstances.sh
for i in {0..2}; do
    gcloud compute instances stop master-${i}
done

for i in {0..4}; do
    gcloud compute instances stop node-${i}
done
^C

networkandcode@Linux:~$ chmod +x stopInstances.sh

networkandcode@Linux:~$ ./stopInstances.sh
```

### To start all instances
```
networkandcode@Linux:~$ cat > startInstances.sh
for i in {0..2}; do
    gcloud compute instances start master-${i}
done

for i in {0..4}; do
    gcloud compute instances start node-${i}
done
^C

networkandcode@Linux:~$ chmod +x startInstances.sh

networkandcode@Linux:~$ ./startInstances.sh
```

--end-of-post--
