---
title: kubernetes > check the components of a cluster
categories: kubernetes
---

We are going to see the installed components of a Kubernetes cluster

Prerequisites: 
- You already have a running cluster
- Basic understandng of Kubernetes objects such as Namespaces, Pods, Deployments, DaemonSets
- Basic 'get' commands of kubectl

---

I have a running cluster with a single master and three nodes, launched using kubeadm and calico network plugin
```
networkandcode@master:~$ kubectl get no
NAME     STATUS   ROLES    AGE   VERSION
master   Ready    master   10h   v1.16.2
node-0   Ready    <none>   10h   v1.16.2
node-1   Ready    <none>   10h   v1.16.2
node-2   Ready    <none>   10h   v1.16.2
```

There is a namespace called kube-system on which most of the Kubernetes software or system components are installed as Kubernetes objects itself
```
networkandcode@master:~$ kubectl get ns kube-system
NAME          STATUS   AGE
kube-system   Active   10h

networkandcode@master:~$ kubectl get all -n kube-system
NAME                                          READY   STATUS    RESTARTS   AGE
pod/calico-kube-controllers-55754f75c-wq2kn   1/1     Running   1          10h
pod/calico-node-4xcrk                         1/1     Running   1          10h
pod/calico-node-8fg7z                         1/1     Running   1          10h
pod/calico-node-bhz45                         1/1     Running   1          10h
pod/calico-node-z6zhd                         1/1     Running   1          10h
pod/coredns-5644d7b6d9-wfgv8                  1/1     Running   1          10h
pod/coredns-5644d7b6d9-x96d2                  1/1     Running   1          10h
pod/etcd-master                               1/1     Running   1          10h
pod/kube-apiserver-master                     1/1     Running   1          10h
pod/kube-controller-manager-master            1/1     Running   1          10h
pod/kube-proxy-hprv8                          1/1     Running   1          10h
pod/kube-proxy-ljfwh                          1/1     Running   1          10h
pod/kube-proxy-lmh8x                          1/1     Running   1          10h
pod/kube-proxy-m46d9                          1/1     Running   1          10h
pod/kube-scheduler-master                     1/1     Running   1          10h

NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
service/kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   10h

NAME                         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                 AGE
daemonset.apps/calico-node   4         4         4       4            4           beta.kubernetes.io/os=linux   10h
daemonset.apps/kube-proxy    4         4         4       4            4           beta.kubernetes.io/os=linux   10h

NAME                                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/calico-kube-controllers   1/1     1            1           10h
deployment.apps/coredns                   2/2     2            2           10h

NAME                                                DESIRED   CURRENT   READY   AGE
replicaset.apps/calico-kube-controllers-55754f75c   1         1         1       10h
replicaset.apps/coredns-5644d7b6d9                  2         2         2       10h
```

If we group them, we see there are primarily 8 software components: 
- calico-kube-controllers
- calico-node 
- coredns
- etcd-master
- kube-apiserver-master
- kube-controller-manager-master
- kube-proxy
- kube-scheduler-master

Let's look at each of these components now

### calico-kube-controllers

It is the calico network controller which is installed only on the master(s), It is an add on networking component though part of the calico network addon installation, and not a native Kubernetes component. The associated Pod is part of a deployment with replicas equal to the number of masters, as we have a single master here, the no. of Pod replicas is 1
```
networkandcode@master:~$ kubectl get po -n kube-system -o wide | grep calico-kube-controllers
calico-kube-controllers-55754f75c-wq2kn   1/1     Running   1          11h   192.168.219.70   master   <none>           <none>
```

### calico-node

It is launched on all of the instances, i.e. both master(s) and nodes. It's part of a daemonSet, which launches Pods on all the available instances by default. This software piece enables inter Pod communication in the cluster. This is an addon component too which has formed as I have chosen calico network plugin during the launch of the cluster
```
networkandcode@master:~$ kubectl get po -n kube-system -o wide | grep calico-node
calico-node-4xcrk                         1/1     Running   1          11h   10.128.15.226    master   <none>           <none>
calico-node-8fg7z                         1/1     Running   1          11h   10.128.15.229    node-1   <none>           <none>
calico-node-bhz45                         1/1     Running   1          11h   10.128.15.228    node-2   <none>           <none>
calico-node-z6zhd                         1/1     Running   1          11h   10.128.15.227    node-0   <none>           <none>
```

### coredns

It is reponsible for the DNS lookups in the cluster, which do the IP / Domian name resolutions. These Pods are part of a deployment with 2 replicas, both launched on the master
```
networkandcode@master:~$ kubectl get po -n kube-system -o wide | grep coredns
coredns-5644d7b6d9-wfgv8                  1/1     Running   1          11h   192.168.219.68   master   <none>           <none>
coredns-5644d7b6d9-x96d2                  1/1     Running   1          11h   192.168.219.69   master   <none>           <none>
```

## etcd-master
This a persistent key value style datastore which stores all the configuration of the Kubernetes objects. Hence it's highly important to backup this. As the name suggests it runs only on the master(s). It's a standalone Pod and not controller by higher level objects such as Deployments / DaemonSets
```
networkandcode@master:~$ kubectl get po -n kube-system -o wide | grep etcd-master
etcd-master                               1/1     Running   1          11h   10.128.15.226    master   <none>           <none>
```

### kube-apiserver-master
This is the apiserver which exposes all the objects, and our client tools such as kubectl interact with this to make CRUD operations on the cluster. This is typically launched only on the master(s). This Pod is standalone as well
```
networkandcode@master:~$ kubectl get po -n kube-system -o wide | grep kube-apiserver-master
kube-apiserver-master                     1/1     Running   1          11h   10.128.15.226    master   <none>           <none>
```

### kube-controller-manager-master
This standalone Pod is a combination of multiple controllers such as replication controller, endpoints controller, namespace controller, and serviceaccounts controller. Each responsible for achieving the desired state of the cluster from it's current state for their respective scope. This Pod runs on the master(s)
```
networkandcode@master:~$ kubectl get po -n kube-system -o wide | grep kube-controller-manager
kube-controller-manager-master            1/1     Running   1          11h   10.128.15.226    master   <none>           <none>
```

### kube-proxy
This is responsible for networking concepts such as services, port forwarding etc. and help exposing the Pods/Applications. These Pods are controlled by DaemonSets and are launched on all instances
```
networkandcode@master:~$ kubectl get po -n kube-system -o wide | grep kube-proxy
kube-proxy-hprv8                          1/1     Running   1          11h   10.128.15.228    node-2   <none>           <none>
kube-proxy-ljfwh                          1/1     Running   1          11h   10.128.15.227    node-0   <none>           <none>
kube-proxy-lmh8x                          1/1     Running   1          11h   10.128.15.229    node-1   <none>           <none>
kube-proxy-m46d9                          1/1     Running   1          11h   10.128.15.226    master   <none>           <none>
```

### kube-scheduler-master
Standalone Pod running on the master responsible for scheduling Pods on available Nodes
```
networkandcode@master:~$ kubectl get po -n kube-system -o wide | grep kube-scheduler-master
kube-scheduler-master                     1/1     Running   1          11h   10.128.15.226    master   <none>           <none>
```

---

So we have seen important standard components that make the Kubernetes cluster, and we could also add many other addon components like Promethus, Grafana etc. However we haven't seen an very important component yet, which is 'kubelet' that runs on nodes and helps registering the node with the kube-apiserver. 'kubelet' doesn't run like a Pod as other components. rather it runs as a binary. Note that when we launch a cluster using kubeadm, kubelet has to be installed separately

--end-of-post--
