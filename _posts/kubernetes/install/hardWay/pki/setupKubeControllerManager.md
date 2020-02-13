We are going to create the PKI components for the kube-controller-manager, this software component is present on all the masters of the cluster, and not on nodes

### Prerequisites:
- [Setup CA](setupCa.md)
- BASH

### Environment:
This exercise could be carried out on cloud shell, or a Linux machine 

### Reference:
- https://github.com/networkandcode/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md#the-controller-manager-client-certificate
- https://github.com/networkandcode/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md#the-service-account-key-pair

---

### Let's keep a directory

We shall put the PKI contents of kube-controller-manager in a separate directory
```
networkandcode@Linux:~$ mkdir kube-controller-manager
networkandcode@Linux:~$ cd kube-controller-manager
```

### Define the CSR requirements
The kube-controller-manager would authenticate with the kube-apiserver using system:kube-controller-manager which is both the CN and OU

```
networkandcode@Linux:~$ cat > kube-controller-manager-csr.json <<EOF
{
    "CN": "system:kube-controller-manager",
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco",
            "O": "system:kube-controller-manager",
            "OU": "k8s-hard-way"
        }
    ]
}
EOF
```

### Create certificate, key and CSR
```
networkandcode@Linux:~$ cfssl gencert \
    -ca ../ca/ca-k8s.pem \
    -ca-key ../ca/ca-k8s-key.pem \
    -config ../ca/ca-config.json \
    -profile k8s-profile \
    kube-controller-manager-csr.json | cfssljson -bare kube-controller-manager
```

We should now see relevant files
```
networkandcode@Linux:~$ ls
kube-controller-manager.csr  kube-controller-manager-csr.json  kube-controller-manager-key.pem  kube-controller-manager.pem
```

### Define the service account CSR
The kube-controller-manager is responsible for generating and signing service account tokens, for which it needs a service account key and certificate which we have to generate

```
networkandcode@Linux:~$ cat > service-account-csr.json <<EOF
{
    "CN": "service-accounts",
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco",
            "O": "Kubernetes",
            "OU": "k8s-hard-way"
        }
    ]
}
EOF
```

### Generate the certificate, CSR and key
```
networkandcode@Linux:~$ cfssl gencert \
    -ca ../ca/ca-k8s.pem \
    -ca-key ../ca/ca-k8s-key.pem \
    -config ../ca/ca-config.json \
    -profile k8s-profile \
    service-account-csr.json | cfssljson -bare service-account
```

We should now see relevant files
```
networkandcode@Linux:~$ ls
ube-controller-manager.csr       kube-controller-manager-key.pem  service-account.csr       service-account-key.pem
kube-controller-manager-csr.json  kube-controller-manager.pem      service-account-csr.json  service-account.pem
```

## Copy Service Account Certificate and Key
We have to copy these only to the masters
```
networkandcode@Linux:~$ cat > copySaCertAndKey.sh 
for i in {0..2}; do
    gcloud compute scp service-account.pem service-account-key.pem master-${i}:/tmp/
    gcloud compute ssh master-${i} -- sudo mv /tmp/service-account* /etc/kubernetes/pki/
done
^C

networkandcode@Linux:~$ chmod +x copySaCertAndKey.sh 

networkandcode@Linux:~$ ./copySaCertAndKey.sh 
```
--end-of-post--
