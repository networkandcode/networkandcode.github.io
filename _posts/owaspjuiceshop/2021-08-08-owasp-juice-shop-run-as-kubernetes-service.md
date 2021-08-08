---
title: owasp juice shop > run as kubernetes service
categories: owasp juice shop
---

Hello, we shall run the OWASP juice shop as a deployment, and expose it as a service in a local 
kubernetes cluster launched with kind. Hence, familiarity with kubernetes deployment and service is 
essential to follow along. You can try this with any cluster, though I am using a cluster that was 
launched with kind. For those not aware, kind is a tool that makes launching k8s clusters on your 
local machine easy.

My cluster is ready.
```
$ kubectl get  nodes
NAME                 STATUS   ROLES                  AGE   VERSION
kind-control-plane   Ready    control-plane,master   10h   v1.21.1
```

Here is the manifest for our deployment.
```
$ cat juice-shop-deployment.yaml 
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: juice-shop
spec:
  template:
    metadata:
      labels:
        app: juice-shop
    spec:
      containers:
      - name: juice-shop
        image: bkimminich/juice-shop
  selector:
    matchLabels:
      app: juice-shop
...
```

Let's launch it.
```
$ kubectl create -f juice-shop-deployment.yaml 
deployment.apps/juice-shop created
```

Boom, the pod is running.
```
$ kubectl get po --watch
NAME                          READY   STATUS              RESTARTS   AGE
juice-shop-699c69578f-fzdfq   0/1     ContainerCreating   0          83s
juice-shop-699c69578f-fzdfq   1/1     Running             0          91s

$ kubectl get deployment
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
juice-shop   1/1     1            1           3m8s
```

Time to launch the service. Here is the manifest of it.
```
$ cat juice-shop-service.yaml 
---
kind: Service
apiVersion: v1
metadata:
  name: juice-shop
spec:
  type: NodePort
  selector:
    app: juice-shop
  ports:
  - name: http
    port: 8000
    targetPort: 3000
...
```

So we are using the service port as 8000, and the container port for the juice shop image is 3000. 
Let's launch it.
```
$ kubectl create -f juice-shop-service.yaml 
service/juice-shop created
```

Let's check the service and endpoints.
```
$ kubectl get svc juice-shop
NAME         TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
juice-shop   NodePort   10.96.119.165   <none>        8000:31167/TCP   21s

$ kubectl get ep juice-shop
NAME         ENDPOINTS         AGE
juice-shop   10.244.0.5:3000   59s
```

The endpoint above should match with the pod, let's validate.
```
$ kubectl get po -o wide
NAME                          READY   STATUS    RESTARTS   AGE     IP           NODE                 NOMINATED NODE   READINESS GATES
juice-shop-699c69578f-fzdfq   1/1     Running   0          7m23s   10.244.0.5   kind-control-plane   <none>           <none>

$ kubectl get po -o wide | awk '{print $6}'
IP
10.244.0.5
```

Cool, the IP is matching with the Endpoint. Alright, we can now try accessing the app.

Firts, lets try it via the node's IP as its a node port service. Note that the node port is 31167 which 
we obtained from the kubect get svc command.
```
$ kubectl get no -o wide
NAME                 STATUS   ROLES                  AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE       KERNEL-VERSION      CONTAINER-RUNTIME
kind-control-plane   Ready    control-plane,master   11h   v1.21.1   172.18.0.2    <none>        Ubuntu 21.04   5.11.0-25-generic   containerd://1.5.2

$ kubectl get no -o wide | awk '{print $6}'
INTERNAL-IP
172.18.0.2
```

Let's then curl the node IP with the node port.
```
$ curl 172.18.0.2:31167
--TRUNCATED--
<script src="runtime-es2018.js" type="module"></script><script src="runtime-es5.js" nomodule defer></script><script src="polyfills-es5.js" nomodule defer></script><script src="polyfills-es2018.js" type="module"></script><script src="vendor-es2018.js" type="module"></script><script src="vendor-es5.js" nomodule defer></script><script src="main-es2018.js" type="module"></script><script src="main-es5.js" nomodule defer></script></body>
</html>
```

It works!!!. We can now see it via the browser.
![OWASP Juice Shop](/assets/owasp-juice-shop-run-as-kubernetes-service-1.png)


This time, lets try to port foward the service, and then access it via the localhost port.
```
$ kubectl port-forward svc/juice-shop 8080:8000
Forwarding from 127.0.0.1:8080 -> 3000
Forwarding from [::1]:8080 -> 3000

```

So we should be to reach the service, if we access the localhost on port 8080.

First via curl. Please open a different terminal for curl, as the kubectl port-forward program is  
running continuously.
```
$ curl localhost:8080
--TRUNCATED--
<script src="runtime-es2018.js" type="module"></script><script src="runtime-es5.js" nomodule defer></script><script src="polyfills-es5.js" nomodule defer></script><script src="polyfills-es2018.js" type="module"></script><script src="vendor-es2018.js" type="module"></script><script src="vendor-es5.js" nomodule defer></script><script src="main-es2018.js" type="module"></script><script src="main-es5.js" nomodule defer></script></body>
</html>
```

curl works, lets check on the browser.
![OWASP Juice Shop](/assets/owasp-juice-shop-run-as-kubernetes-service-2.png)

You can close the port forwarding with Ctrl C, when you no longer want to access the juice shop through 
the local host port.
```
$ kubectl port-forward svc/juice-shop 8080:8000
Forwarding from 127.0.0.1:8080 -> 3000
Forwarding from [::1]:8080 -> 3000
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
Handling connection for 8080
^C$ 
```

Well, so we were able to access the juice shop via the node port and via the local host port. Read 
once more for clarity :). Thank you !!!

--end-of-post--
