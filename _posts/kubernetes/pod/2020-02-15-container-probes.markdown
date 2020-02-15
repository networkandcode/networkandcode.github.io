---
title: kubernetes > container probes
categories: kubernetes
---

Kubelets runnig on nodes, can periodically probe containers that are launched on those nodes, and ensure the app is running as it is intended to. In this post we are going to see 2 such standard probes used in production environments, namely liveness and readiness probes, and the standard HttpGetAction handler these probes use, to peform period health checks on web apps.

It's good to have some fundamental understanding of web servers, HTTP, HTML, and Pods to benefit more from this post.

Let's start by launching an apache pod
```
networkandcode@master $ cat > pod-apache.yaml <<EOF
---
apiVersion: v1
kind: Pod
metadata:
  name: apache
spec:
  containers:
  - name: apache
    image: httpd
...
EOF

networkandcode@master $ kubectl create -f pod-apache.yaml
pod/apache created

networkandcode@master $ kubectl get po apache
NAME     READY   STATUS    RESTARTS   AGE
apache   1/1     Running   0          12s
```

If we launch the bash terminal of this apache container, we should find the index.html file in the htdocs directory
```
networkandcode@master $ kubectl exec -it apache -- bash
root@apache:/usr/local/apache2# ls htdocs
index.html
```

Let's see the default content inside index.html
```
root@apache:/usr/local/apache2# cat htdocs/index.html
<html><body><h1>It works!</h1></body></html>
```

The apache server's homepage should display this content, and we could use CURL to see this. In  order to use curl in the apache container, we have to first install it
```
root@apache:/usr/local/apache2# apt update -y
root@apache:/usr/local/apache2# apt install curl -y

root@apache:/usr/local/apache2# curl localhost
<html><body><h1>It works!</h1></body></html>
```

