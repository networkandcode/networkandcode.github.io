---
title: kubernetes > launch a cluster with kind
categories: kind
---

We can launch a cluster easily with kind on our Linux system. Lets see how to do it.
Its assumed kubectl is already installed to interact with the cluster, and you are aware of the basics 
of kubectl.

Download the kind binary.
```
$ curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.11.1/kind-linux-amd64
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    98  100    98    0     0    266      0 --:--:-- --:--:-- --:--:--   266
100   624  100   624    0     0    834      0 --:--:-- --:--:-- --:--:--   834
100 6660k  100 6660k    0     0  2644k      0  0:00:02  0:00:02 --:--:-- 4256k
```

Check the permissions of the downloaded file.
```
$ ls kind -ltr
-rw-rw-r-- 1 networkandcode networkandcode 6820758 Aug  7 22:47 kind
```

Its not executable, hence give it executable permission.
```
$ chmod +x kind

$ ls kind -ltr
-rwxrwxr-x 1 networkandcode networkandcode 6820758 Aug  7 22:47 kind
```

We can now move it to a dir, which is part of the path environment variable.

Let's see whats in the path.
```
$ echo $PATH
/home/networkandcode/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

We can move kind to any of these directories. Let's  move it to /usr/bin.
```
$ sudo mv kind /usr/bin/kind

$ which kind
/usr/bin/kind
```

All set, we can now start using kind. Let's check its version.
```
$ kind --version
kind version 0.11.1
```

Excellent, let's create our cluster.
```
$ kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.21.1) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a question, bug, or feature request? Let us know! https://kind.sigs.k8s.io/#community 🙂
```

Boom, a single node cluster should be ready.
```
$ kubectl get nodes
NAME                 STATUS   ROLES                  AGE   VERSION
kind-control-plane   Ready    control-plane,master   95s   v1.21.1
```

So as we saw its very easy to create a kubernetes cluster in our system with kind. This would help with 
kubernetes based development, or for learning many of the concepts of kubernetes, with out the need of 
launching a cluster on cloud, or with heavy resources.

Hope you liked the post, thank you for reading.

--end-of-post---
