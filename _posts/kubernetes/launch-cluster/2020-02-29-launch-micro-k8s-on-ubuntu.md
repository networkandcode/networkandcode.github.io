---
title: kubernetes > launch microk8s on ubuntu
categories: kubernetes
...

MicroK8s is an all-in-one kubernetes deployment with all it's native services on a single machine

This exercise is carried out on Ubuntu 18.04
```
root@microk8s:~# lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 18.04.4 LTS
Release:        18.04
Codename:       bionic
```

Execute the following command to install microk8s on ubuntu
```
root@microk8s:~# snap install microk8s --classic
2020-02-29T11:53:47Z INFO Waiting for restart...
microk8s v1.17.3 from Canonical* installed
root@microk8s:~#                        
```

And that's it your all-in-one Kubernetes cluster is ready in a jiffy. You may start operating your Kubernetes cluster using kubectl, the only difference is that 
you would have to use the microk8s prefix

```
root@microk8s:~# microk8s.kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
microk8s   Ready    <none>   11s   v1.17.3

root@microk8s:~# microk8s.kubectl get pods
No resources found in default namespace.

root@microk8s:~# microk8s.kubectl cluster-info
Kubernetes master is running at https://127.0.0.1:16443

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

The following command could be used to view the list of available addons and their status
```
root@microk8s:~# microk8s.status
microk8s is running
addons:
cilium: disabled
dashboard: disabled
dns: disabled
fluentd: disabled
gpu: disabled
helm3: disabled
helm: disabled
ingress: disabled
istio: disabled
jaeger: disabled
juju: disabled
knative: disabled
kubeflow: disabled
linkerd: disabled
metallb: disabled
metrics-server: disabled
prometheus: disabled
rbac: disabled
registry: disabled
storage: disabled
```

For instance we may enable prometheus now, as follows
```
root@microk8s:~# microk8s.enable prometheus
--TRUNCATED--
The Prometheus operator is enabled (user/pass: admin/admin)
```

--end-of-post--
