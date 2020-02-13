---
title: kubernetes > add static pods
---

We are going to see some information about Kubelet and how to add static Pods to a cluster. It is good to have some knowledge of the components of a Kubernetes cluster and some basics of services in Linux, for better understanding of this post.

A Kubelet is a core Kubernetes component which is present on all of the instances of a Kubernetes cluster, and it is responsible for executing Pods on the instance where it resides. Static Pods are those that are directly controlled by the kubelet with out the need of controlling those Pods using clients such as Kubectl. Usually we pass commands such as ``` 'kubectl create' ``` to create Pods as per the defined manifest. However with static Pods, we just keep the Pod manifests in a specific directory that the Kubelet is told to watch, and then create Pods called as static Pods from those manifests.

A kubelet is usually present as a binary, and we could check its location using ```which```
```
networkancdcode@k8s-master-0:~$ which kubelet
/usr/bin/kubelet
```

Note that we are on the master instance, and there are unique kubelets on each instance that forms the cluster

In a typical kubeadm based cluster, the kubelet would usually run as a service, whose configuration is present in the following location
```
networkancdcode@k8s-master-0:~$ sudo ls /etc/systemd/system/kubelet.service.d/
10-kubeadm.conf
```

The contents of the configuration file would be
```
networkancdcode@k8s-master-0:~$ sudo cat /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
# Note: This dropin only works with kubeadm and kubelet v1.11+
[Service]
Environment="KUBELET_KUBECONFIG_ARGS=--bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf"
Environment="KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml"
# This is a file that "kubeadm init" and "kubeadm join" generates at runtime, populating the KUBELET_KUBEADM_ARGS variable dynamically
EnvironmentFile=-/var/lib/kubelet/kubeadm-flags.env
# This is a file that the user can use for overrides of the kubelet args as a last resort. Preferably, the user should use
# the .NodeRegistration.KubeletExtraArgs object in the configuration files instead. KUBELET_EXTRA_ARGS should be sourced from this file.
EnvironmentFile=-/etc/default/kubelet
ExecStart=
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
```

The last line of the output above mentions the path where the kubelet binary is stored '/usr/bin/kubelet', followed the options that it takes, one of the options is ```$KUBELET_CONFIG_ARGS``` which is defined in the same file above as ```KUBELET_CONFIG_ARGS=--config=/var/lib/kubelet/config.yaml```. This is nothing but the configuration fle of the kubelet itself.

Let's now check the kubelet configuration of the master instance, and filter only the staticPodPath section in it
```
networkancdcode@k8s-master-0:~$ sudo cat /var/lib/kubelet/config.yaml | grep staticPodPath
staticPodPath: /etc/kubernetes/manifests
```

This says that Pod manifests saved in the '/etc/kubernetes/manifests' folder are watched by the kubelet and static Pods are created based on those manifests

This folder has some existing files which are responsible for those respective Static Pods running only in the master
```
networkancdcode@k8s-master-0:~$ ls /etc/kubernetes/manifests/
etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-extra-scheduler.yaml  kube-scheduler.yaml
```

Static Pods do not need any higher level controllers such as Deployments to control them, as that job is done directly by the kubelet itself. For instance, let's try deleting one of the static Pods 'etcd Pod' running in the kube-system namespace
```
networkancdcode@k8s-master-0:~$ kubectl get po -n kube-system | grep etcd
etcd-k8s-master-0                          1/1     Running   7          8d

networkancdcode@k8s-master-0:~$ kubectl delete po etcd-k8s-master-0 -n kube-system
pod "etcd-k8s-master-0" deleted

networkancdcode@k8s-master-0:~$ kubectl get po -n kube-system | grep etcd
etcd-k8s-master-0                          0/1     Pending   0          4s

networkancdcode@k8s-master-0:~$ kubectl get po -n kube-system | grep etcd
etcd-k8s-master-0                          1/1     Running   7          11s
```

We see that a new etcd Pod gets created by the kubelet keeps watching the manifests in the ```staticPodPath``` and creates a new etcd Pod based on the etcd manifest in ```/etc/kubernetes/manifests/etcd.yaml```

Let's try adding a new Pod manifest to the staticPodPath directory
```
networkancdcode@k8s-master-0:~$ cd /etc/kubernetes/manifests/
networkancdcode@k8s-master-0:~$ cat ex38-po-static.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: po38
spec:
  containers:
  - name: ctr38
    image: httpd
...
```

This should create a Pod automatically
```
networkancdcode@k8s-master-0:~$ kubectl get po
NAME                READY   STATUS    RESTARTS   AGE
po38-k8s-master-0   1/1     Running   0          78s
```

Cleanup, removing the file should delete the Pod automatically
```
networkandcode@k8s-master-0:~$ sudo rm /etc/kubernetes/manifests/ex38-po-static.yaml
networkandcode@k8s-master-0:~$ kubectl get po
No resources found in default namespace.
```

In this post we have seen about kubelet and how kubelet controls static Pods. We have added a new staticPod and finally performed cleanup.

Thank you for reading and wish you happy learning.

Reference: https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/

--end-of-post--
