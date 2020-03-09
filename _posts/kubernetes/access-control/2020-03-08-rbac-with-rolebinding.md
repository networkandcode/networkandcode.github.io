---
title: kubernetes > rbac with rolebinding
categories: kubernetes
---

RBAC(Role Based Access Control) is one of the authorization modes supported by the Kube api server. And in this post we would see 
see some functionality of role, clusterrole and rolebinding objects that are used for ensuring RBAC in Kubernetes.

You should know how to launch a cluster using kubeadm, and how to create a user with TLS, to make the most use of this post.

This exercise is performed in a cluster launched with kubeadm, let's ensure we are in the right context, that ensures issuing kubectl commands 
as admin
```
networkandcode@k8s-master: $ kubectl config use-context kubernetes-admin@kubernetes
Switched to context "kubernetes-admin@kubernetes".
```

we can check if RBAC is enabled as follows
```
networkandcode@k8s-master: $ kubectl get po kube-apiserver-master -n kube-system -o yaml | grep authorization-mode
    - --authorization-mode=Node,RBAC
```
So both Node and RBAC authorization modes are enabled in the API server

Since RBAC is enabled, we could now go ahead and create a 'Role' object, which is specific to a namespace. Let's define 
a manifest
```
networkandcode@k8s-master: $ cat > role-get-pods.yaml <<EOF
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: get-pods
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - list
...
EOF
```
The manifest above could be used to create a role with name 'get-pods' in the 'default' namespace. And this role 
should allow listing 'pods'. apiGroups refers to the list of apiGroups and since we are dealing 
only with Pods here, we just need mention "" for the core apiGroup. Note that apiGroup doesn't include the version as in
apiVersion. For instance if we have to refer to Deployments, whose apiVersion is apps/v1, the corresponding apiGroup would be "apps"

It's time to create the role
```
networkandcode@k8s-master: $ kubectl create -f role-get-pods.yaml

role.rbac.authorization.k8s.io/get-pods created

networkandcode@k8s-master: $ kubectl get roles
NAME       AGE
get-pods   24s
```

So the role, that can allow listing 'Pods' is ready. But someone(for example a user) has to make use of this role. This is where 'rolebinding' 
comes into picture. We shall prepare a manifest for the 'rolebinding' object in the 'default' namespace
```
networkandcode@k8s-master: $ cat > rolebinding-user2-get-pods.yaml <<EOF
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: user2-get-pods
subjects:
- kind: User
  name: user2
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: get-pods
  apiGroup: rbac.authorization.k8s.io
...
EOF
```

The rolebinding manifest above when applied, should map the subjects(in this case only user2) with the role 'get-pods' that was created already. Subjects 
could be users, groups, or service accounts. Note that both 'role' and 'rolebinding' objects are scoped to a namespace. We may now create the rolebinding
```
networkandcode@k8s-master: $ kubectl create -f rolebinding-user2-get-pods.yaml
rolebinding.rbac.authorization.k8s.io/user2-get-pods created

networkandcode@k8s-master: $ kubectl get rolebindings
NAME             AGE
user2-get-pods   42s
```

user2 now has permission to issue 'kubectl get pods'. Let's switch the context to perfom actions as user2
```
networkandcode@k8s-master: $ kubectl config use-context context2
Switched to context "context2".
```
The context2 above scopes 'user2' with the current cluster 'kubernetes'. 
You  may refer to [https://networkandcode.github.io/kubernetes/2020/02/27/add-a-kubectl-user-with-tls.html] to setup a similar context

Let's view the list of Pods as user2
```
networkandcode@k8s-master: $ kubectl get pods
No resources found.
```
So the rolebinding works as user2 is able to list pods in the default namespace, there are no Pods though as they were not yet created. 

Let's try a different command, for instance lets list nodes in the cluster, it shouldn't work as it doesn't have permission to do so
```
networkandcode@k8s-master: $ kubectl get nodes
Error from server (Forbidden): nodes is forbidden: User "user2" cannot list resource "nodes" in API group "" at the cluster scope
```

Let's switch to the admin context and do the cleanup, delete the rolebinding and role we created
```
networkandcode@k8s-master: $ kubectl config use-context kubernetes-admin@kubernetes
Switched to context "kubernetes-admin@kubernetes".

networkandcode@k8s-master: $ kubectl delete -f rolebinding-user2-get-pods.yaml
rolebinding.rbac.authorization.k8s.io "user2-get-pods" deleted

networkandcode@k8s-master: $ kubectl delete -f role-get-pods.yaml
role.rbac.authorization.k8s.io "get-pods" deleted
```

We are now going to see a different use case, we could also let a rolebinding refer to a clusterole instead of a role, however the rolebinding 
would still be able to apply the clusterrole with in the namespace, as the rolebinding is only a namespace resource

For instance let's create a 'clusterrole' object which would allow the user to list Pods irrespective of the namespace. 
Note that clusterrole is bound to a cluster and doesn't restrict with in a namespace
```
networkandcode@k8s-master: $ cp role-get-pods.yaml clusterrole-get-pods.yaml

networkandcode@k8s-master: $ sed -i 's/Role/ClusterRole/g' clusterrole-get-pods.yaml

networkandcode@k8s-master: $ cat clusterrole-get-pods.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: get-pods
rules:
- apiGroups:
  - ""
  resources:
  - pods
  verbs:
  - list
...

```

We have prepared a manifest to create a 'clusterrole' which has specifications similar to that of the role created earlier, the only difference is that the 
clusterrole is bound to the cluster, where as role is bound to the namespace. Before creating the clusterrole object, we need to ensure we are scoped to the admin context
```
networkandcode@k8s-master: $ kubectl config current-context
kubernetes-admin@kubernetes

networkandcode@k8s-master: $ kubectl create -f clusterrole-get-pods.yaml
clusterrole.rbac.authorization.k8s.io/get-pods created

networkandcode@k8s-master: $ kubectl get clusterrole get-pods
NAME       AGE
get-pods   117s
```

A rolebinding should now be created to map user2 with the newly created clusterrole. Again we are going to create a rolebinding similar to the existing role binding 
created before, with just one change, binding it with a clusterrole instead of role
```
networkandcode@k8s-master: $ cat rolebinding-user2-get-pods-allns.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: user2-get-pods-all-ns
subjects:
- kind: User
  name: user2
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: get-pods
  apiGroup: rbac.authorization.k8s.io
...

networkandcode@k8s-master: $ kubectl create -f rolebinding-user2-get-pods-allns.yaml
rolebinding.rbac.authorization.k8s.io/user2-get-pods-all-ns created

networkandcode@k8s-master: $ kubectl get rolebinding
NAME                    AGE
user2-get-pods-all-ns   17s
```

Let's switch context, and this time as 'user2' we should only be able to list Pods in the default namespace but not all namespaces as the rolebinding is still 
a 'namespace' object eventhough we are referring to a clusterrole in it.
```
networkandcode@k8s-master: $ kubectl config use-context context2
Switched to context "context2".

networkandcode@k8s-master: $ kubectl get pods
No resources found.

networkandcode@k8s-master: $ kubectl get pods --all-namespaces
Error from server (Forbidden): pods is forbidden: User "user2" cannot listresource "pods" in API group "" at the cluster scope
```

Let's do the cleanup, delete the rolebinding and clusterrole
```
networkandcode@k8s-master: $ kubectl config use-context kubernetes-admin@kubernetes
Switched to context "kubernetes-admin@kubernetes".

networkandcode@k8s-master: $ kubectl delete -f rolebinding-user2-get-pods-allns.yaml
rolebinding.rbac.authorization.k8s.io "user2-get-pods-all-ns" deleted

networkandcode@k8s-master: $ kubectl delete -f clusterrole-get-pods.yaml
clusterrole.rbac.authorization.k8s.io "get-pods" deleted
```
--end-of-post--
