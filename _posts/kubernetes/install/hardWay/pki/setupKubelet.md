We are going to create the PKI components for the kubelet, this software component is present on all of the nodes of the cluster, and not on masters. They should be present only on nodes where the actual workload such as Pods would be launched

### Prerequisites:
- [Setup CA](setupCa.md)
- BASH

### Environment:
This exercise could be carried out on cloud shell, or a Linux machine 

### Reference:
- https://github.com/networkandcode/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md#the-kubelet-client-certificates

---

### Let's keep a directory

We shall put the PKI contents of the admin user in a separate directory
```
networkandcode@Linux:~$ mkdir kubelet
networkandcode@Linux:~$ cd kubelet
```

### Define the CSR requirements
As we have 5 nodes in our setup, we need to have 5 CSRs, 5 keys and 5 certificates for the kubelets, the kubelet in each node would use the username that takes the form 'system:nodes:nodeName' for example 'system:nodes:node-1' which should be set as the CN of the CSR, here system:nodes refers to the group hence we should set that as the OU of the CSR

We need to 5 CSR configs as there 5 nodes
```
networkandcode@Linux:~$ cat > createCsrs.sh
for i in {0..4}; do
cat > kubelet-${i}-csr.json <<EOF
{
    "CN": "system:nodes:${i}",
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco",
            "O": "system:nodes",
            "OU": "k8s-hard-way"
        }
    ]
}
EOF
done
^C

networkandcode@Linux:~$ chmod +x createCsrs.sh 

networkandcode@Linux:~$ ./createCsrs.sh 
```

There should now be 5 CSR JSON files
```
networkandcode@Linux:~$ ls
createCsrs.sh  kubelet-0-csr.json  kubelet-1-csr.json  kubelet-2-csr.json  kubelet-3-csr.json  kubelet-4-csr.json
```

### Create Certificates, keys and CSRs

We need to create the certificates and keys for all the 5 nodes, this time we are going to have an option 'hostname' to specifiy the hostname, external and internal IP of the node, as kubelets represent nodes
```
networkandcode@Linux:~$ cat > setupKubelets.sh
for i in {0..4}; do

ext_ip=$(gcloud compute instances describe node-${i} \
  --format 'value(networkInterfaces[0].accessConfigs[0].natIP)')

int_ip=$(gcloud compute instances describe node-${i} \
  --format 'value(networkInterfaces[0].networkIP)')
  
cfssl gencert \
    -ca ../ca/ca-k8s.pem \
    -ca-key ../ca/ca-k8s-key.pem \
    -config ../ca/ca-config.json \
    -profile k8s-profile \
    -hostname=${i},${ext_ip},${int_ip} \
    kubelet-${i}-csr.json | cfssljson -bare kubelet-${i}

done
^C

networkandcode@Linux:~$ chmod +x setupKubelets.sh

networkandcode@Linux:~$ ./setupKubelets.sh
```
> Please ensure the instances are started, also note that the external IPs may change each time when the instances are restarted in a Cloud environment unless static Public IPs are reserved

We should now see relevant files
```
networkandcode@Linux:~$ ls
createCsrs.sh       kubelet-0.pem       kubelet-1.pem       kubelet-2.pem       kubelet-3.pem       kubelet-4.pem    setupKubelets.sh
kubelet-0.csr       kubelet-1.csr       kubelet-2.csr       kubelet-3.csr       kubelet-4.csr       kubelet.csr
kubelet-0-csr.json  kubelet-1-csr.json  kubelet-2-csr.json  kubelet-3-csr.json  kubelet-4-csr.json  kubelet-key.pem
kubelet-0-key.pem   kubelet-1-key.pem   kubelet-2-key.pem   kubelet-3-key.pem   kubelet-4-key.pem   kubelet.pem
```

### Copy certificates and keys
There is a certificiate and key for each nodes, hence we need to copy those to appropriate nodes
```
networkandcode@Linux:~$ cat > copyCertificatesAndKeys.sh 
for i in {0..4}; do
    gcloud compute scp kubelet-${i}.pem kubelet-${i}-key.pem node-${i}:/tmp/
    gcloud compute ssh node-${i} -- sudo mv /tmp/kubelet-${i}.pem /etc/kubernetes/pki/
done
^C

networkandcode@Linux:~$ chmod +x copyCertificatesAndKeys.sh 

networkandcode@Linux:~$ ./copyCertificatesAndKeys.sh 
```
--end-of-post--
