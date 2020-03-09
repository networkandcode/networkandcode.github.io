---
title: kubernetes > add a user with tls
categories: kubernetes
---

In this exercise we would add an extra user to kubeconfig, that uses TLS for authentication. Its good to have some 
fundamental understanding of OpenSSL, kubeadm and kubeconfig to benefit more from this post

To let a user authenticate via TLS with the kube-apiserver, we need to generate a TLS key for the user, and a 
signed TLS certificate for the user. The signature will be provided by the cluster CA, that should have been typically 
setup by kubeadm during the cluster launch.

Let's create a new TLS RSA private key of modulus 4096 bit, for the new user, using OpenSSL
```
networkandcode@master $ openssl genrsa -out user2.key 4096

networkandcode@master $ cat user2.key
-----BEGIN RSA PRIVATE KEY-----
REDACTED
-----END RSA PRIVATE KEY-----
```

We now need to generate a CSR (certificate signing request) for this key, 
as the username is 'user2' it can be specified as the CN (common name)
```
networkandcode@master $ openssl req -new -out user2.csr -key user2.key -subj "/CN=user2"

networkandcode@master $ cat user2.csr
-----BEGIN CERTIFICATE REQUEST-----
REDACTED
-----END CERTIFICATE REQUEST-----
```
This CSR should now be signed by the cluster CA (cluster authority) so that we get a signed certificate. 
We could do this using the CertificateSignigRequest API object of Kubernetes.

We need to create a CSR object which has the base 64 encoded CSR in it. So, our first step is to encode the CSR
```
networkandcode@master $ cat user2.csr | base64 | tr -d '\n
```

The command above does the encoding, but we could better save it in a variable, let's say user2_csr_base64
```
networkandcode@master $ export user2_csr_base64=$(cat ./user2.csr | base64 | tr -d '\n')

```

We now define our Kubernetes CSR object as follows
```
networkandcode@master $ cat > csr-user2.yaml <<EOF
---
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  name: csr-user2
spec:
  groups:
  - system:authenticated
  request: ${user2_csr_base64}
  usages:
  - "client auth"
...
EOF
```
In the manifest above, we are importing data from the variable we defined earlier, the 'cllient auth' usage is enough 
as our user is only a client, the 'system:authenticated' allows only authentication to the cluster.

The CSR object can now be created after substituing the variable
```
networkandcode@master $ cat csr-user2.yaml | envsubst | kubectl create -f -
certificatesigningrequest.certificates.k8s.io/csr-user2 created
```

Our CSR object is created, but in pending state, as it has to be signed by the cluster CA
```
networkandcode@master $ kubectl get csr csr-user2
NAME        AGE     REQUESTOR          CONDITION
csr-user2   2m17s   kubernetes-admin   Pending
```

The Requestor column has 'kubernetes-admin', as its the current user that kubectl is scoped to

Let's approve it, a.k.a sign it
```
networkandcode@master $ kubectl certificate approve csr-user2
certificatesigningrequest.certificates.k8s.io/csr-user2 approved

networkandcode@master $ kubectl get csr csr-user2
NAME        AGE     REQUESTOR          CONDITION
csr-user2   4m11s   kubernetes-admin   Approved,Issued
```

The CSR object would now have the base64 encoded, signed certificate within it, we may retrieve it
```
networkandcode@master $ kubectl get csr csr-user2 -o jsonpath={.status.certificate}
```

We could decode it and save it as a file
```
networkandcode@master $ kubectl get csr csr-user2 -o jsonpath={.status.certificate} | base64 --decode > user2.crt
```

ok, so by now we have the key and the signed certificate, as an optional step, we could move them both to the directory 
where other PKI data is stored
```
networkandcode@master $ mv user2.key /etc/kubernetes/pki/
networkandcode@master $ mv user2.crt /etc/kubernetes/pki/
```

It's time to modify kubeconfig now, to add the new user, its key, and certificate
```
networkandcode@master $ kubectl config set-credentials user2 --client-key=/etc/kubernetes/pki/user2.key --client-certificate=/etc/kubernetes/pki/user2.crt
User "user2" set.
```

And now we need to add a new context, that maps this user with the cluster, note that the cluster name is 'kubernetes'
```
networkandcode@master $ kubectl config set-context context2 --cluster kubernetes --user user2
Context "context2" created.
```

Finally switch context, to issue kubectl commands as the new user 'user2'
```
networkandcode@master $ kubectl config use-context context2
Switched to context "context2".
```

Let's try a command as 'user2'
```
networkandcode@master $ kubectl version
Client Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.0", GitCommit:"641856db18352033a0d96dbc99153fa3b27298e5", GitTreeState:"clean", BuildDate:"2019-03-25T15:53:57Z", GoVersion:"go1.12.1", Compiler:"gc", Platform:"linux/amd64"}
Server Version: version.Info{Major:"1", Minor:"14", GitVersion:"v1.14.0", GitCommit:"641856db18352033a0d96dbc99153fa3b27298e5", GitTreeState:"clean", BuildDate:"2019-03-25T15:45:25Z", GoVersion:"go1.12.1", Compiler:"gc", Platform:"linux/amd64"}
```

This works, but the following wouldn't work
```
networkandcode@master $ kubectl get nodes
Error from server (Forbidden): nodes is forbidden: User "user2" cannot list resource "nodes" in API group "" at the cluster scope
```

This is because the 'system:authenticated' group we mentioned in the CSR object, would allow only authentication to the cluster, with no other authorization

--end-of-post--

