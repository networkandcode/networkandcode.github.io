---
title: kubernetes > about the cluster-admin cluster role binding
categories: kubernetes
---

When a cluster is launched with kubeadm, the kubeconfig is set to use the default 'kubernetes-admin' user that has 
admin permissions on the kube-apiserver, let's explore more about it

The reader should have some understanding of kubeconfig, jsonpath, TLS, awk, and cluster role binding to make the most from this post

The default kubeconfig exits at .kube/config, and it's context is set as follows
```
networkandcode@k8s-master: $ kubectl config current-context
kubernetes-admin@kubernetes
```

The list of contexts can be viewed as follows, in a fresh cluster there is only one context though
```
networkandcode@k8s-master: $ kubectl config view -o jsonpath={.contexts}; echo
[map[context:map[cluster:kubernetes user:kubernetes-admin] name:kubernetes-admin@kubernetes]]
```

The output above shows the user associated with context 'kubernetes-admin@kubernetes' is 'kubernetes-admin'

Likewise, the list of users can be viewed as follows
```
networkandcode@k8s-master: $ kubectl config view -o jsonpath={.users}; echo
[map[name:kubernetes-admin user:map[client-certificate-data:REDACTED client-key-data:REDACTED]]]
```

There is only one user 'kubernetes-admin' and it has a client certificate and client key, that lets this user authenticate 
against the kube-apiserver

We could extract just the certificate from the kubeconfig, which is typically located in .kube/config, using 'grep'
```
networkandcode@k8s-master: $ grep client-certificate-data .kube/config    
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM4akNDQWRxZ0F3SUJBZ0lJRFUvRCtyM0Fv--TRUNCATED--
```

The output has a key(client-certificate-data) and it's value, we may filter only the value using awk
```
networkandcode@k8s-master: $ grep client-certificate-data .kube/config | awk '{print $2}'
LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUM4ak--TRUNCATED--
```

This certificate is in base64 form, we may decode it to get the actual x509 certificate
```
networkandcode@k8s-master: $ grep client-certificate-data .kube/config | awk '{print $2}' | base64 --decode
-----BEGIN CERTIFICATE-----
MIIC8jCCAdqgAwIBAgIIDU/D+r3AowMwDQYJKoZIhvcNAQELBQAwFTETMBEGA1UE
AxMKa3ViZXJ--TRUNCATED--
-----END CERTIFICATE-----
```

We may now see this certificate in text form using 'openssl x509 -text', to know more details about it.
However we would only filter 'Subject:' to see the Organization(O) and CommonName(CN)
```
networkandcode@k8s-master: $ grep client-certificate-data .kube/config | awk '{print $2}' | base64 --decode | openssl x509 -text | grep Subject:
        Subject: O=system:masters, CN=kubernetes-admin
```

Note that Organization is equivalent to groups and CN is equivalent to username, so this certificate is associated 
with user 'kubernetes-admin' who belongs to group 'system:masters'

Now, let's see the cluster-admin cluster role binding, that maps this group with a cluster role
```
networkandcode@k8s-master: $ kubectl get clusterrolebinding cluster-admin
NAME            AGE
cluster-admin   45m

networkandcode@k8s-master: $ kubectl get clusterrolebinding cluster-admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  creationTimestamp: "2020-03-16T05:06:05Z"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: cluster-admin
  resourceVersion: "97"
  selfLink: /apis/rbac.authorization.k8s.io/v1/clusterrolebindings/cluster-admin
  uid: d6db19d9-6743-11ea-b7e0-0242ac11001b
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:masters
```

This manifest shows that the 'cluster-admin' clusterrolebinding binds the group 'system:masters' with the clusterrole 'cluster-admin'. So the name used for 
the clusterrolebinding and clusterrole is same. Let's now see details about the clusterrole
```
networkandcode@k8s-master: $ kubectl get clusterrole cluster-admin -o yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  creationTimestamp: "2020-03-16T05:06:04Z"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: cluster-admin
  resourceVersion: "42"
  selfLink: /apis/rbac.authorization.k8s.io/v1/clusterroles/cluster-admin
  uid: d69bb085-6743-11ea-b7e0-0242ac11001b
rules:
- apiGroups:
  - '*'
  resources:
  - '*'
  verbs:
  - '*'
- nonResourceURLs:
  - '*'
  verbs:
  - '*'
```

From the manifest, we see this role 'cluster-role' allows all actions on all resources and nonresource URLs

So, when a cluster is bootstrapped with kubeadm, it creates a certificate for the user 'kubernetes-admin' belonging to group 'system:masters', creates a clusterrole 
'cluster-admin' with all permissions on the cluster, creates a clusterrolebinding 'cluster-admin' that maps the clusterrole 'cluster-admin' with the group 
'system:masters'. Thus the user 'kubernetes-admin' gets admin permissions to perform operations in the kubernetes cluster

--end-of-post--


