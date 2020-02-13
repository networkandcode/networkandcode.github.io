We are going to create the PKI components for kube-apiserver, this software component is present only on the masters

### Prerequisites:
- [Setup CA](setupCa.md)
- BASH

### Environment:
This exercise could be carried out on cloud shell, or a Linux machine 

### Reference:
- https://github.com/networkandcode/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md#the-kubernetes-api-server-certificate

---

### Let's keep a directory

We shall put the PKI contents of kube-apiserver in a separate directory
```
networkandcode@Linux:~$ mkdir kube-apiserver
networkandcode@Linux:~$ cd kube-apiserver
```

### Define the CSR requirements
```
networkandcode@Linux:~$ cat > kube-apiserver-csr.json <<EOF
{
    "CN": "kubernetes",
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

### Create certificate, key and CSR
```
networkandcode@Linux:~$ cfssl gencert \
    -ca ../ca/ca-k8s.pem \
    -ca-key ../ca/ca-k8s-key.pem \
    -config ../ca/ca-config.json \
    -profile k8s-profile \
    kube-proxy-csr.json | cfssljson -bare kube-proxy
```

We should now see relevant files
```
networkandcode@Linux:~$ ls
kube-proxy.csr  kube-proxy-csr.json  kube-proxy-key.pem  kube-proxy.pem
```
--end-of-post--
