We need to provision a Certificate Authority (CA) using CFSSL, Here we are setting up a CA ourself manually so that we can generate signed TLS certificates for the components of the cluster, In real world CAs are companies such as Symantec, GlobaSign etc.

### Prerequisites: 
- [Setup Cloud](../cloud/setupCloud.md)
- HTTPS
- [Install CFSSL](installGoAndCfssl.md)
- BASH

### Environment: 
This exercise could be carried out on the Google cloud shell, or a Linux machine

### Reference:
- https://coreos.com/os/docs/latest/generate-self-signed-certificates.html
- https://github.com/networkandcode/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md

---

### Let's keep a directory

We shall keep information related to CA in a separate directory
```
networkandcode@Linux:~$ mkdir ca
networkandcode@Linux:~$ cd cka
```

### Generate default CSR config

Similarly we need to generate a CA CSR (Certificate signing request) for the Kubernetes cluster.
Generate the default csr file
```
networkandcode@Linux:~$ cfssl print-defaults csr
{
    "CN": "example.net",
    "hosts": [
        "example.net",
        "www.example.net"
    ],
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco"
        }
    ]
}
```

### Create CSR config 

We are going to create a ca-csr file in json format using the reference above, we would change the CN (Common Name) to k8s-hard-way, remove the hosts field, add two fields O(Organizanation) and OU(Organization Unit) to names, and keep the rest as is
```
networkandcode@Linux:~$ cat > ca-csr.json <<EOF
{
    "CN": "k8s-hard-way",
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco",
            "O": "networkandcode",
            "OU": "CA"
        }
    ]
}
EOF
```
> You may modify CN, O, U and other details too based on your preference

### Create PKI components for the CA

Let's create the CSR, private key, CSR using the CSR config defined above. The certificate of the CA authority doesn't have to be signed by some other authority, hence we use the keyword -initca to self sign it. However we need the CA certificate, it's key and profile to sign rest of the client / server certificates of the cluster
```
networkandcode@Linux:~/tech/kubernetes/cka/installation$ cfssl gencert -initca ca-csr.json | cfssljson -bare ca-k8s
2019/10/19 12:06:59 [INFO] generating a new CA key and certificate from CSR
2019/10/19 12:06:59 [INFO] generate received request
2019/10/19 12:06:59 [INFO] received CSR
2019/10/19 12:06:59 [INFO] generating key: ecdsa-256
2019/10/19 12:06:59 [INFO] encoded CSR
2019/10/19 12:06:59 [INFO] signed certificate with serial number 473399627357096017760119908565808697458509233563
```
> The first part ```cfssl gencert -initca ca-csr.json``` would create a certificate, a certificate request, and an EC private key in encoded form, all 3 in a single dictionary(json). Note that EC stands for Elliptic curve, and it's generating an EC key because we have specified ECDSA as the algorithm in the ca-csr.json file, we could also use RSA as the algorithm instead of ECDSA. These are then fed into the second part 'cfssjson -bare ca-k8s' which would split those 3 from the json and create 3 different files, one for each, all starting with the name ca-k8s as specified at the end of the command

The 3 files are as follows
```
networkandcode@Linux:~$ ls ca-k8s*
ca-k8s.csr  ca-k8s-key.pem  ca-k8s.pem
```
> ca-k8s.csr is the certificate signing request, ca-k8s-key.pem is the EC private key, and ca-k8s.pem is the certificate, you may use the cat command to view the encoded content in each of the files

The CA setup is now done, note that the CA certificate is also called root certificate

### Copy the CA key and certificate
We need to copy the certificate and key to appropriate instances
Let's create an appropriate directory ```/etc/kubernetes/pki``` on the remote instances where these could be stored
```
networkandcode@Linux:~$ cd ..
networkandcode@Linux:~$ cat > ./createPkiDir.sh
for i in {0..2}; do
gcloud compute ssh master-${i} -- sudo mkdir -p /etc/kubernetes/pki
done
for i in {0..4}; do
gcloud compute ssh node-${i} -- sudo mkdir -p /etc/kubernetes/pki
done
^C

networkandcode@Linux:~$ chmod +x createPkiDir.sh
```
Copy the CA / Root certificate to all the instances
```
networkandcode@Linux:~$ cd ca
networkandcode@Linux:~$ cat > copyCaCertificate.sh 
for i in {0..2}; do
    gcloud compute scp ca-k8s.pem master-${i}:/tmp
    gcloud compute ssh master-${i} -- sudo mv /tmp/ca-k8s.pem /etc/kubernetes/pki
done

for i in {0..4}; do
    gcloud compute scp ca-k8s.pem node-${i}:/tmp
    gcloud compute ssh node-${i} -- sudo mv /tmp/ca-k8s.pem /etc/kubernetes/pki
done
^C

networkandcode@Linux:~$ chmod +x ./copyCaCertificate.sh 

networkandcode@Linux:~$ ./copyCaCertificate.sh 
```
> we are first copying the certificate using SCP, to the tmp folder of the remote instance, and then move it from their to the path in /etc as modying anything under /etc needs root privileges, we do this cause we couldn't use sudo directly with scp. chmod +x is used to make the code executable

Copy the CA key to only the masters
```
networkandcode@Linux:~$ cat > copyCaKey.sh 
for i in {0..2}; do
    gcloud compute scp ca-k8s-key.pem master-${i}:/tmp
    gcloud compute ssh master-${i} -- sudo mv /tmp/ca-k8s-key.pem /etc/kubernetes/pki
done
^C

networkandcode@Linux:~$ chmod +x copyCaKey.sh 

networkandcode@Linux:~$ ./copyCaKey.sh 
```

### Generate default CA config
```
networkandcode@Linux:~$ cd ca
networkandcode@Linux:~$ cfssl print-defaults config
{
    "signing": {
        "default": {
            "expiry": "168h"
        },
        "profiles": {
            "www": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            }
        }
    }
}
```

### Create CA config

We are going to use the json content above as a reference to make the ca config file for our cluster, we would change the default expiry to 8760h i.e. 1 year, and we would need only profile and which we are going to name as 'k8s-profile'
```
networkandcode@Linux:~$ cat > ca-config.json <<EOF
{
    "signing": {
        "default": {
            "expiry": "8760h"
        },
        "profiles": {
            "k8s-profile": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            }
         }       
     }
}
EOF
```
> We don't need this CA config, as of now, but it is going to be used when we need to generate client / server certificates for different components of the Kubernetes cluster

--end-of-post--
