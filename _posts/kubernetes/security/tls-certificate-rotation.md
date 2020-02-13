## Topic:
We are going to see how the Kubelet certificate rotation works. By default the Kubelet TLS certificates get expired in 1 year after generation, by default, this is however a bigger duration. When the certificate rotation option is enabled, it ensures auto certification renewal when it expires, a new TLS key will be generated automatically for the Kubelet and subsequently a new TLS certificate would be requested by the kubelet, from the kube-apiserver

## Prerequisites:
- You have a running Kubernets cluster
- Basics of Kubelet and Kube API Server
- Basics of TLS authentication

## Cluster
We have a 3 node cluster launched using the Google Kubernetes Engine
```
networkandcode@cloudshell:~ $ kubectl get no
NAME                                                STATUS   ROLES    AGE     VERSION
gke-standard-cluster-1-default-pool-2b07c74f-0460   Ready    <none>   5m36s   v1.13.11-gke.14
gke-standard-cluster-1-default-pool-2b07c74f-4nrg   Ready    <none>   5m36s   v1.13.11-gke.14
gke-standard-cluster-1-default-pool-2b07c74f-l2lx   Ready    <none>   5m36s   v1.13.11-gke.14
```

## Login to a Node
A Kubelet runs as a binary on all of the instances that form the cluster, let's login to one of the nodes and check where the Kubelet binary exists
```
networkandcode@cloudshell:~ $ gcloud compute ssh gke-standard-cluster-1-default-pool-2b07c74f-0460 --zone us-central1-a

networkandcode@gke-standard-cluster-1-default-pool-2b07c74f-0460 ~ $ which kubelet
/home/kubernetes/bin/kubelet
```

## To enable certificate rotation
In the node, we can check the info about the certificate rotation option of the kubelet
```
$ sudo kubelet --help | grep rotate-certificates
      --rotate-certificates                                                                                       <Warning: Beta feature> Auto rotate the kubelet client certificates by requesting new certificates from the kube-apiserver when the certificate expiration approaches. (DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)
```
