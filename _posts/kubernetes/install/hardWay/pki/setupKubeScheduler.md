We are going to create the PKI components for kube-scheduler, this software component is present only on the masters

### Prerequisites:
- [Setup CA](setupCa.md)
- BASH

### Environment:
This exercise could be carried out on cloud shell, or a Linux machine 

### Reference:
- https://github.com/networkandcode/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md#the-scheduler-client-certificate

---

### Let's keep a directory

We shall put the PKI contents of kube-scheduler in a separate directory
```
networkandcode@Linux:~$ mkdir kube-scheduler
networkandcode@Linux:~$ cd kube-scheduler
```

### Define the CSR requirements
The CN and OU for kube-scheduler is system:kube-scheduler
```
networkandcode@Linux:~$ cat > kube-scheduler-csr.json <<EOF
{
    "CN": "system:kube-scheduler",
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco",
            "O": "system:kube-scheduler",
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
    kube-scheduler-csr.json | cfssljson -bare kube-scheduler
```

We should now see relevant files
```
networkandcode@Linux:~$ ls
kube-scheduler.csr       kube-scheduler-key.pem
kube-scheduler-csr.json  kube-scheduler.pem
```
--end-of-post--
