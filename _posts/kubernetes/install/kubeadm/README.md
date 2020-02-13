This code could be used to launch an Ubuntu Kubernetes cluster with Single control plane (1 Master) and 3 Nodes on Google cloud platform. You have to run this from a Linux machine with gcloud installed, or on the Google cloud shell

```git clone git@github.com:networkandcode/tech.git```
or
```git clone https://github.com/networkandcode/tech.git```

please set the project using gcloud
```
gcloud config set project <project-id>
```
you may check the list of available projects using ```gcloud projects list```
you may also create a new project if required using ```gcloud projects create <project-id>```

```
cd tech/kubernetes/cka/install/kubeadm
./launch.sh
--TRUNCATED--
Run 'kubectl get nodes' on the control-plane to see this node join the cluster.

````````````````````````````````````````````````````
```
To access the master: gcloud compute ssh master
Your cluster is ready, login to the master and enjoy
networkandcode@Linux:~/tech/kubernetes/cka/install/kubeadm$ gcloud compute ssh master
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-1044-gcp x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Mon Oct 21 05:19:23 UTC 2019

  System load:  1.04              Users logged in:        0
  Usage of /:   31.4% of 9.52GB   IP address for ens4:    10.128.15.219
  Memory usage: 24%               IP address for docker0: 172.17.0.1
  Swap usage:   0%                IP address for tunl0:   192.168.219.64
  Processes:    158


25 packages can be updated.
14 updates are security updates.


Last login: Mon Oct 21 05:13:06 2019 from 137.97.77.11
networkandcode@master:~$ kubectl get nodes
NAME     STATUS   ROLES    AGE   VERSION
master   Ready    master   91s   v1.16.2
node-0   Ready    <none>   52s   v1.16.2
node-1   Ready    <none>   43s   v1.16.2
node-2   Ready    <none>   33s   v1.16.2
networkandcode@master:~$ 
```
--end-of-post--
