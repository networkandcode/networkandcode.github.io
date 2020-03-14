---
title: kubernetes > rbac with clusterrolebinding
categories: kubernetes
---

A cluster role binding could be used to bind a user with a cluster role which is bound to a cluster irrespective of 
namespaces. Here, we shall be creating a cluster role and then create a cluster role binding to bind that cluster role 
with a user. Hence, you should know how to add a user before trying out this exercise. Some understanding of rolebinding is 
also beneficial as clusterrolebindings are also like rolebindings except for their scope to the cluster.

Ensure you are at the right context with admin permissions
```
networkandcode@k8s-master: $ kubectl config use-context kubernetes-admin@kubernetes
Switched to context "kubernetes-admin@kubernetes".
```

### Create a cluster role
We are going to create a cluster role that should let listing deployments in all namespaces, depending on the version 
of Kubernetes, the apiVersion of Deployments could vary, so it's better to check it's apiVersion first
```
networkandcode@k8s-master: $ kubectl explain deployments | grep VERSION
VERSION:  extensions/v1beta1

networkandcode@k8s-master: $ cat clusterrole-list-deployments.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: list-deployments
rules:
- apiGroups:
  - extensions  # we don't need the version info v1beta1 here
  resources:
  - deployments
  verbs:
  - list
...

networkandcode@k8s-master: $ kubectl create -f clusterrole-list-deployments.yaml
clusterrole.rbac.authorization.k8s.io/list-deployments created

networkandcode@k8s-master: $ kubectl get clusterrole list-deployments
NAME               AGE
list-deployments   2m47s
```

Note: other common verbs for roles / clusterroles are: get, post, watch, update, create, patch, delete

### Create a cluster role binding
Let's now bind the cluster role with a user, note that the user should already be existing
```
networkandcode@k8s-master: $ cat clusterrolebinding-user2-list-deployments.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: user2-list-deployments
subjects:
- kind: User
  name: user2
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: list-deployments
  apiGroup: rbac.authorization.k8s.io
...

networkandcode@k8s-master: $ kubectl create -f clusterrolebinding-user2-list-deployments.yaml
clusterrolebinding.rbac.authorization.k8s.io/user2-list-deployments created

networkandcode@k8s-master: $ kubectl get clusterrolebinding user2-list-deployments
NAME                     AGE
user2-list-deployments   112s
```

We may now switch context to perform operations as user2
```
networkandcode@k8s-master: $ kubectl config use-context context2
Switched to context "context2".
```

Let's test
```
networkandcode@k8s-master: $ kubectl get deployments
No resources found.

networkandcode@k8s-master: $ kubectl get deployments -n kube-system
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
coredns                   2/2     2            2           49m
cloud-provider            1/1     1            1           49m

networkandcode@k8s-master: $ kubectl get deployments --all-namespaces
NAMESPACE     NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
kube-system   coredns                   2/2     2            2           49m
kube-system   cloud-provider            1/1     1            1           49m

networkandcode@k8s-master: $ kubectl get pods
Error from server (Forbidden): pods is forbidden: User "user2" cannot list resource "pods" in API group "" in thenamespace "default"
``` 
So it works as expected

--end-of-post--
