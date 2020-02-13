We are going to create the PKI components for kube-apiserver, this software component is present only on the masters

### Prerequisites:
- [Setup CA](setupCa.md)
- BASH
- Google Cloud

### Environment:
This exercise could be carried out on cloud shell, or a Linux machine on which gcloud is installed

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

We need to add hostnames that are the private IPs of the masters, the localhost IP, and the external IP of the loadbalancer that we reserved earlier
```
networkandcode@Linux:~$ cat > setupApiserver.sh 
ext_ip=$(gcloud compute addresses describe kube-apiserver \
  --region $(gcloud config get-value compute/region) \
  --format 'value(address)')

int_ip_0=$(gcloud compute instances describe master-0 \
        --format 'value(networkInterfaces[0].networkIP)')
int_ip_1=$(gcloud compute instances describe master-1 \
        --format 'value(networkInterfaces[0].networkIP)')
int_ip_2=$(gcloud compute instances describe master-2 \
        --format 'value(networkInterfaces[0].networkIP)')


cfssl gencert \
  -ca=../ca/ca-k8s.pem \
  -ca-key=../ca/ca-k8s-key.pem \
  -config=../ca/ca-config.json \
  -hostname=${ext_ip},${int_ip_0},${int_ip_1},${int_ip_2},127.0.0.1,kubernetes.default \
  -profile=k8s-profile \
  kube-apiserver-csr.json | cfssljson -bare kube-apiserver
^C
```

We should now see relevant files
```
networkandcode@Linux:~$ $ ls
kube-apiserver.csr  kube-apiserver-csr.json  kube-apiserver-key.pem  kube-apiserver.pem  setupApiserver.sh
```

### Copy the certificate and key
We need to copy the certificate and key to instances where the kube-apiserver will be installed, which is typically the masters
```
networkandcode@Linux:~$ cat > copyCertificateAndKey.sh 
 for i in {0..2}; do
    gcloud compute scp kube-apiserver.pem kube-apiserver-key.pem master-${i}:/tmp/
    gcloud compute ssh master-${i} -- sudo mv /tmp/kube-apiserver* /etc/kubernetes/pki/
done
^C

networkandcode@Linux:~$ chmod +x copyCertificateAndKey.sh 

networkandcode@Linux:~$ ./copyCertificateAndKey.sh
```
--end-of-post--
