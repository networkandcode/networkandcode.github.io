The components of a Kubernetes cluster comprise of certain HTTPS clients and HTTPS servers, for example kube-apiserver and  kubectl form an HTTPS server-client combination. Secure communication between an HTTPS client and HTTPS server is ensured using TLS certficiates. In real world when we access an HTTPS website from our browser, certificates are generated automatically in the backend and we don't realize it. However we have an opportunity here to generate those certficates ourselves and understand more. The whole process or setup of generating encoded keys, certificates, signing them to enable secure communication is called Public Key Infrastructure (PKI). Hence, as a first step, we are going to install GO and CFSSL on an Ubuntu machine. CFFLS is a tool written in 'GO' to generate TLS certificates and self sign them.

> Certificates of websites are signed using authorized certificate authorities which incurs cost and not self signed. 'go' or 'golang' is a programming language open sourced by Google

### Prerequisite: 
Linux

### Platform:
Ubuntu

### Install Go

Download the binary distribution
```
networkandcode@Linux:/tmp$ wget https://dl.google.com/go/go1.13.1.linux-amd64.tar.gz
```

Extract contents from the compressed file
```
networkandcode@Linux:/tmp$ tar -xzf go1.13.1.linux-amd64.tar.gz
```

There should be a new directory by the name 'go'
```
networkandcode@Linux:/tmp$ ls go
```

Remove the downloaded binary now
```
networkandcode@Linux:/tmp$ rm go1.13.1.linux-amd64.tar.gz 
```

Move the 'go' directory to /usr/local
```
networkandcode@Linux:/tmp$ sudo mv go /usr/local
```

Add the binary to the PATH environment variable
```
networkandcode@Linux:/tmp$ export PATH=$PATH:/usr/local/go/bin
```

The GO CLI should now work
```
networkandcode@Linux:/usr/local$ go
Go is a tool for managing Go source code.

Usage:

	go <command> [arguments]
--TRUNCATED--
```

Set GOPATH
```
networkandcode@Linux:/tmp$ export GOPATH=/usr/local/go/
```

### Install CFSSL

Clone the cfssl repo 
```
networkandcode@Linux:/tmp$ git clone git@github.com:cloudflare/cfssl.git
```

Create a directory in the go src path
```
networkandcode@Linux:/tmp$ sudo mkdir -p $GOPATH/src/github.com/cloudflare
```

Move cfssl to the cloudflare directory
```
networkandcode@Linux:/tmp$ sudo mv cfssl/ $GOPATH/src/github.com/cloudflare
```

Make using GO
```
networkandcode@Linux:/tmp$ cd $GOPATH/src/github.com/cloudflare/cfssl
networkandcode@Linux:/usr/loca/go/src/github.com/cloudflare/cfssl$ make
```

The cfssl binaries should now be available
```
networkandcode@Linux:~$ ls /usr/loca/go/src/github.com/cloudflare/cfssl/bin/
cfssl         cfssl-certinfo  cfssl-newkey  mkbundle
cfssl-bundle  cfssljson       cfssl-scan    multirootca
```

Add cfssl binaries to path
```
networkandcode@Linux:~$ export PATH=$PATH:$GOPATH/src/github.com/cloudflare/cfssl/bin
```

cfssl cli should now work
```
networkandcode@Linux:~$ cfssl
No command is given.
Usage:
Available commands:
--TRUNCATED--
```

--end-of-post--
