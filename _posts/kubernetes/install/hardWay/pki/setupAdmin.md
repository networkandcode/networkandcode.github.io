We are going to create the PKI components for the admin user, when we issue kubectl commands to administer a cluster, it is actually sending requests as a user to the api-server, hence there is a need to configure atleast one user which would have admin rights on the cluster, the user would also be specified in the kubeconfig. Hence we have to ensure the required PKI components are present for this user

### Prerequisites:
- [Setup CA](setupCa.md)

### Environment:
This exercise could be carried out on cloud shell, or a Linux machine 

### Reference:
- https://github.com/networkandcode/kubernetes-the-hard-way/blob/master/docs/04-certificate-authority.md#the-admin-client-certificate

---

### Let's keep a directory

We shall put the PKI contents of the admin user in a separate directory
```
networkandcode@Linux:~$ mkdir k8s-admin
networkandcode@Linux:~$ cd k8s-admin
```

### Define the CSR requirements
```
networkandcode@Linux:~$ cat > k8s-admin-csr.json <<EOF
{
    "CN": "k8s-admin",
    "key": {
        "algo": "ecdsa",
        "size": 256
    },
    "names": [
        {
            "C": "US",
            "ST": "CA",
            "L": "San Francisco",
            "O": "system:masters",
            "OU": "k8s-hard-way"
        }
    ]
}
EOF
```
> The common name is specified as k8s-admin, and a user entry is to be added in kubeconfig with the same name. The organization system:masters makes this user the real admin, OU is just named like k8s-hardway, you may keep some name of your choice too

### Create the Certificate, key and CSR

The generated certificate will be signed by the k8s-profile of the CA using the CA's private key and root(CA) certificate, the details of this profile is mentioned in the CA config file

```
networkandcode@Linux:~$ cfssl gencert -ca ../ca/ca-k8s.pem -ca-key ../ca/ca-k8s-key.pem -config ../ca/ca-config.json -profile=k8s-profile k8s-admin-csr.json | cfssljson -bare k8s-admin
2019/10/19 15:27:39 [INFO] generate received request
2019/10/19 15:27:39 [INFO] received CSR
2019/10/19 15:27:39 [INFO] generating key: ecdsa-256
2019/10/19 15:27:39 [INFO] encoded CSR
2019/10/19 15:27:39 [INFO] signed certificate with serial number 403563889263831903341184765400756822732239928278
2019/10/19 15:27:39 [WARNING] This certificate lacks a "hosts" field. This makes it unsuitable for
websites. For more information see the Baseline Requirements for the Issuance and Management
of Publicly-Trusted Certificates, v.1.1.6, from the CA/Browser Forum (https://cabforum.org);
specifically, section 10.2.3 ("Information Requirements").
```
We should now see 3 more files all starting with k8s-admin as given at the end of the cfssljson command
```
networkandcode@Linux:~$ ls
k8s-admin.csr  k8s-admin-csr.json  k8s-admin-key.pem  k8s-admin.pem
```
> k8s-admin.csr is the CSR based on the CSR config provided, k8s-admin-key.pem is the EC private key, and k8s-admin.pem is the client certificate

If we look at the certificate, it doesn't say anything like client certificate, but we know it's a client certificate because it needs to communicate with the kube-apiserver using tools such as kubectl

```
networkandcode@Linux:~$ cat k8s-admin.pem
-----BEGIN CERTIFICATE-----
MIICXDCCAgKgAwIBAgIURrBuQBBS1qzYLat3bg513jF5+9YwCgYIKoZIzj0EAwIw
bzELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAkNBMRYwFAYDVQQHEw1TYW4gRnJhbmNp
c2NvMRcwFQYDVQQKEw5uZXR3b3JrYW5kY29kZTELMAkGA1UECxMCQ0ExFTATBgNV
BAMTDGs4cy1o--TRUNCATED--
-----END CERTIFICATE-----
```

--end-of-post--
