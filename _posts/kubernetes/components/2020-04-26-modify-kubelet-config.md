---
title: kubernetes > modify kubelet config
categories: kubernetes
---

We are going to see, some overview of kubelet and its config. The prerequisites are to have basic understanding of kubeadm, kubeconfig and jsonpath.

Kubelet is the node agent that is responsible for running Pods on the node. Its present in all the instances of the cluster, 
both master(s) and nodes.

In a typical kubeadm based cluster, kubelet would exist as a binary and keeps running as service/daemon in the background. Let's see the status of 
kubelet in the master instance of our kubernetes cluster 
```
networkandcode@master $ which kubelet
/usr/bin/kubelet

networkandcode@master $ sudo systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └10-kubeadm.conf
---TRUNCATED---
```

We may check the service's configuration to find more details
```
networkandcode@master $ sudo cat /etc/systemd/system/kubelet.service.d/10-kubeadm.conf
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
In the output above, we see the kubeconfig file for kubelet as ```/etc/kubernetes/kubelet.conf```, this file holds authentication / authorization information for the kubelet to perform opertaions on the kube api server. 
We also see the configuration for the kubelet is loaded in ```/var/lib/kubelet/config.yaml```.

Let's check the kubeconfig first
```
networkandcode@master $ sudo cat /etc/kubernetes/kubelet.conf
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: --TRUNCATED--
    server: --TRUNCATED--
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: system:node:master
  name: system:node:master@kubernetes
current-context: system:node:master@kubernetes
kind: Config
preferences: {}
users:
- name: system:node:master
  user:
    client-certificate-data: --TRUNCATED--
    client-key-data: --TRUNCATED--
```

This is just like any other kubeconfig, however the key point to note is the username which is ```system:node:master```, the first two portions system:node refers to 
the group and this is a special purpose group in Kubernetes that provides the kubelet with a special 'Node Authorization' mode to perform standard operations on the API server. 
Hence, kubelet doesn't need methods such as RBAC for authorization.

Let's now see the kubelet's configuration on the master instance.
```
networkandcode@master $ cat /var/lib/kubelet/config.yaml
---TRUNCATED---
httpCheckFrequency: 20s
imageGCHighThresholdPercent: 85
imageGCLowThresholdPercent: 80
imageMinimumGCAge: 2m0s
iptablesDropBit: 15
iptablesMasqueradeBit: 14
---TRUNCATED---
```

It would have many configuration parameters for the Kubelet, few of which are listed above. Lets focus one such kubelet config parameter 'maxPods'
```
networkandcode@master $ cat /var/lib/kubelet/config.yaml | grep maxPods
maxPods: 110

networkandcode@master $ kubectl get nodes master -o jsonpath={.status.allocatable.pods}; echo
110
```

This config parameter is set to 110 in the kubelet config, which is also reflecting asis in the config status of the master instance. Let's change it to 100
```
networkandcode@master $ sed -i 's/maxPods: 110/maxPods: 100/g' /var/lib/kubelet/config.yaml

networkandcode@master $ cat /var/lib/kubelet/config.yaml | grep maxPods
maxPods: 100
```

We should now restart kubelet for the new configuration to take effect
```
networkandcode@master $ sudo systemctl restart kubelet
```

The master instance would go to NotReady state for few seconds, and revert back to Ready
```
networkandcode@master $ kubectl get nodes
NAME     STATUS     ROLES    AGE   VERSION
master   NotReady   master   75m   v1.14.0
node01   Ready      <none>   75m   v1.14.0

networkandcode@master $ kubectl get nodes --watch
NAME     STATUS   ROLES    AGE   VERSION
master   Ready    master   75m   v1.14.0
node01   Ready    <none>   75m   v1.14.0
```

The new configuration for maxPods should now be visible on the master's configuration status as well
```
networkandcode@master $ kubectl get nodes master -o jsonpath={.status.allocatable.pods}; echo
100
```

So we have modified the kubelet configuration of the master instance, in this example. Likewise we could also modify the kubelet configuration of a node by logging into 
the node via methods such as SSH.

--end-of-post--
