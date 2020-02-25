---
title: kubernetes > add a kubectl user with token
categories: kubernetes
---

We are going to see how to add an extra kubectl user. 
The prerequisite for this topic is some fundamental understanding of kubeadm, and the use of jsonpath with kubectl.

When a cluster is bootstrapped with kubeadm, 
it creates a user with relevant TLS key and certificate, and assigns it admin privileges. This user details are then copied on to kubeconfig, that 
kubectl could use to interact with the API server and perform CRUD operations on the API objects.

When we issue commands through kubectl, it sources configuration a.k.a kubeconfig, by default from the file ~/.kube/config. The kubeconfig contains details such as 
the clusters, contexts, users and so on

```
networkandcode@master$ cat .kube/config
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tL--redacted--
    server: https://172.17.0.3:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: redacted
    client-key-data: redacted
```

Context refers to the username and cluster combination, so currently the context is 'kubernetes-admin@kubernetes' which is the name of the context, 
and in this context there are sections such as user and cluster which are defined as 'kubernetes-admin' and 'kubernetes' respectively. 

So, kubectl would source the client key and certificate generated for the 'kubernetes-admin' user, and CA certificate generated 
for the 'kubernetes' cluster. Note that the TLS keys and certificates would be in base64 encoded form in kubeconfig. 

In a kubeadm based cluster, the certificates are located typically at /etc/kubernetes/pki, if we check the ca certificate here and then encode, it should match with 
the ca certificate we saw in the kubeconfig
```
networkandcode@master$ base64 /etc/kubernetes/pki/ca.crt
LS0tLS1--redacted--
```

So the kubernetes-admin user is using TLS key and certificate to authenticate with the API server. However we could also authenticate using service account 
tokens which are signed bearer tokens. 

We could create a service account token for a new user easily using kubectl. When we create a new service account in kubernetes, it would generate a secret 
internally that holds the cluster CA certificate and a token, both in base64 encoded form
```
networkandcode@master $ cat sa-admin2.yaml <<EOF
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin2
...
EOF

networkandcode@master $ kubectl create -f sa-admin2.yaml
serviceaccount/admin2 created

networkandcode@master $ kubectl get sa
NAME      SECRETS   AGE
admin2    1         8s
default   1         137m

networkandcode@master $ kubectl get sa admin2 -o yaml
--TRUNCATED--
secrets:
- name: admin2-token-tcktp

networkandcode@master $ kubectl get secret admin2-token-tcktp
NAME                 TYPE                                  DATA   AGE
admin2-token-gk8r5   kubernetes.io/service-account-token   3      105s

networkandcode@master $ kubectl get secret admin2-token-tcktp -o yaml
apiVersion: v1
data:
  ca.crt: redacted
  --TRUNCATED--
  token: redacted
--TRUNCATED--
```

Let's decode the token and store it in a variable 'token'
```
networkandcode@master $ token=$(kubectl get secret admin2-token-tcktp -o jsonpath={.data.token} | base64 --decode)
```

We may now edit kubeconfig, by adding a new user to it
```
networkandcode@master $ kubectl config set-credentials admin2 --token=$token
User "admin2" set.
```

The users section of kubeconfig should now show an extra user
```
networkandcode@master $ cat ~/.kube/config
--TRUNCATED--
users:
- name: admin2
  user:
    token: redacted
- name: kubernetes-admin
  user:
    client-certificate-data: redacted
    client-key-data: redacted
```

So we have chosen token based authentication for admin2, where as 'kubernetes-admin' is using TLS key and certificate

We need to now add a context, with the user and cluster combination
```
networkandcode@master $ kubectl config set-context context2 --cluster=kubernetes --user=admin2
Context "context2" created.
```

The kubeconfig's contexts section should now show a new context
```
networkandcode@master $ cat ~/.kube/config
--TRUNCATED--
contexts:
- context:
    cluster: kubernetes
    user: admin2
  name: context2
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
--TRUNCATED--
```

We may now switch the context, so that we could perform operations on the cluster as 'admin2'
```
networkandcode@master $ kubectl config use-context context2
Switched to context "context2".
```

The kubeconfig file should have been modified to show the correct current context
```
networkandcode@master $ cat ~/.kube/config | grep current-context
current-context: context2

# This is an alternate command
networkandcode@master $ kubectl config current-context
context2
```

We may also use ```kubectl config view``` to view the kubeconfig

Our first command as 'admin2'
```
networkandcode@master $ kubectl cluster-info
Kubernetes master is running at https://172.17.0.66:6443
KubeDNS is running at https://172.17.0.66:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

Let's try few other commands
```
networkandcode@master $ kubectl get ns
NAME              STATUS   AGE
default           Active   49m
kube-node-lease   Active   49m
kube-public       Active   49m
kube-system       Active   49m

networkandcode@master $ kubectl create ns ns2
namespace/ns2 created
```

So, we were able to add an additonal user with token based authentication, to our kubeconfig file, and performed operations using it through kubectl

--end-of-post--
