---
title: kubernetes > role of docker
categories: kubernetes
---

The fundamental API object in kubernetes is a pod which contains one or more containers in it.
These containers are packaged in a format compatible to the container runtime on which they are executed.
Docker is a common container runtime, so there is interaction between kubernetes and docker to let the apps run.

So the real work loads are containers where the apps run. Let's create a sample Pod and illustrate this in a practical way.

The prerequisites for this post, is to have some fundamental understanding of Kubernetes and Docker containers.

We define a Pod manifest which has an apache container in it, the apache image would be fetched from docker hub, if its not present locally.
```
networkandcode@k8s-master:$ cat > pod-apache.yaml <<EOF
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-apache
spec:  containers:
  - name: apache
    image: httpd
...
EOF
```

The Pod is going to be launched
```
networkandcode@k8s-master:$ kubectl create -f pod-apache.yaml
pod/pod-apache created
```

Let's see where the Pod is launched
```
networkandcode@k8s-master:$ kubectl get pods pod-apache -o wide
NAME         READY   STATUS    RESTARTS   AGE   IP          NODE    NOMINATED NODE   READINESS GATES
pod-apache   1/1     Running   0          87s   10.44.0.4   node2   <none>           <none>
```

Keep a **separate tab or window** open, and issue the --watch flag to capture events of the Pod
```
networkandcode@k8s-master:$ kubectl get pods pod-apache --watch -o wide
NAME         READY   STATUS    RESTARTS   AGE    IP          NODE    NOMINATED NODE   READINESS GATES
pod-apache   1/1     Running   0          2m2s   10.44.0.4   node2   <none>           <none>
```

So the Pod is on node2, we may now access node2, using a possible method based on the reachablity to node2
and check the list of docker containers there, and subsequently filter the pod name there
```
networkandcode@node2:$ docker container ls | grep pod-apache
91b19b56d72b        httpd                   "httpd-foreground"       26 seconds ago      Up 23 seconds                         k8s_apache_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_0
3fdbe0446a74        k8s.gcr.io/pause:3.1    "/pause"                 28 seconds ago      Up 27 seconds                         k8s_POD_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_0
```

It shows two containers, one is the container image for the actual application, in this case apache that has the httpd image, 
and the second container representing the pod itself, this is the pod sandbox container

If we remove the apache container forcefully, with its container id, kubernetes should launch a new apache container immediately
```
networkandcode@node2:$ docker container rm 91b19b56d72b --force
91b19b56d72b

networkandcode@node2:$ docker container ls | grep pod-apache
3d70ded781da        httpd                   "httpd-foreground"       5 minutes ago       Up 5 minutes                         k8s_apache_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_0
3fdbe0446a74        k8s.gcr.io/pause:3.1    "/pause"                 8 minutes ago       Up 8 minutes                         k8s_POD_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_0
networkandcode@node2:$
```

So a new apache container was launched with a new container id **3d70ded781da**, let's see the live Pod events on the other tab
```
networkandcode@k8s-master:$ kubectl get pods pod-apache --watch -o wide
NAME         READY   STATUS    RESTARTS   AGE    IP          NODE    NOMINATED NODE   READINESS GATES
pod-apache   1/1     Running   0          2m2s   10.44.0.4   node2   <none>           <none>
pod-apache   0/1     ContainerCreating   0          2m28s   10.44.0.4   node2   <none>           <none>
pod-apache   1/1     Running             0          2m45s   10.44.0.4   node2   <none>           <none>```
```

It shows the container was restarted, however the RESTARTS column shows '0'

This time, we shall gracefull stop the container, and then remove it, instead of forcefully removing it
```
networkandcode@node2:$ docker container stop 3d70ded781da
3d70ded781da
networkandcode@node2:$ docker container rm 3d70ded781da
3d70ded781da
```

The live Pod events, this time transitions the status from completed to running, and has an entry of '1' at the RESTARTS column
```
networkandcode@k8s-master:$ kubectl get pods pod-apache --watch -o wide
NAME         READY   STATUS    RESTARTS   AGE    IP          NODE    NOMINATED NODE   READINESS GATES
pod-apache   1/1     Running   0          2m2s   10.44.0.4   node2   <none>           <none>
pod-apache   0/1     ContainerCreating   0          2m28s   10.44.0.4   node2   <none>           <none>
pod-apache   1/1     Running             0          2m45s   10.44.0.4   node2   <none>           <none>
pod-apache   0/1     Completed           0          12m     10.44.0.4   node2   <none>           <none>
pod-apache   1/1     Running             1          12m     10.44.0.4   node2   <none>           <none>
pod-apache   1/1     Running             1          12m     10.44.0.4   node2   <none>           <none>
```

Docker should show a new container ID for the apache container, as usual
```
networkandcode@node2:$ docker container ls | grep pod-apache
c9ea78dac905        httpd                   "httpd-foreground"       4 minutes ago       Up 4 minutes                         k8s_apache_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_1
3fdbe0446a74        k8s.gcr.io/pause:3.1    "/pause"                 16 minutes ago      Up 16 minutes                         k8s_POD_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_0
```

This time if we delete the Pod sandbox container, it would kill both the containers - the apache container as well as
the pod sandbox container, and kubernetes would restart them both. 

First we would forcefully remove it, the Pod status doesnt change, however the RESTARTS counter increases by one
```
networkandcode@node2:$ docker container rm 3fdbe0446a74 --force
3fdbe0446a74

networkandcode@k8s-master:$ kubectl get pods pod-apache --watch -o wide
NAME         READY   STATUS    RESTARTS   AGE    IP          NODE    NOMINATED NODE   READINESS GATES
--TRUNCATED--
pod-apache   1/1     Running             1          18m     <none>      node2   <none>           <none>
pod-apache   1/1     Running             2          18m     10.44.0.4   node2   <none>           <none>
```

Finally, we would now gracefully stop and remove the pod sandbox container, there is no change in status this time too, 
the RESTARTS counter should go up by one
```
networkandcode@node2:$ docker container ls | grep pod-apache
9e8cf9c01c67        httpd                   "httpd-foreground"       3 minutes ago       Up 3 minutes                         k8s_apache_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_2
53fbecd4180f        k8s.gcr.io/pause:3.1    "/pause"                 3 minutes ago       Up 3 minutes                         k8s_POD_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_0

                         k8s_POD_pod-apache_default_36253f3c-4ed5-11ea-a10e-0242294e2d14_0

networkandcode@node2:$ docker container stop 53fbecd4180f
53fbecd4180f
networkandcode@node2:$ docker container rm 53fbecd4180f
53fbecd4180f


networkandcode@k8s-master:$ kubectl get pods pod-apache --watch -o wide
--TRUNCATED--
pod-apache   1/1     Running             3          22m     10.44.0.4   node2   <none>           <none>
```


Let's now see more details about the Pod events with the describe command, at the master
```
networkandcode@k8s-master:$ kubectl describe pods pod-apache

--TRUNCATED--

Start Time:         Fri, 14 Feb 2020 02:53:43 +0000
Labels:             <none>
Annotations:        <none>
Status:             Running
IP:                 10.44.0.4
Containers:
  apache:
    Container ID:   docker://401942ae7cd209794eaed22cfea3b35b0316f416bca7dced6325702c55a97fb6
    Image:          httpd
    Image ID:       docker-pullable://httpd@sha256:b783a610e75380aa152dd855a18368ea2f3becb5129d0541e2ec8b662cbd8afb
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Fri, 14 Feb 2020 03:16:19 +0000
    Last State:     Terminated
      Reason:       Completed
      Exit Code:    0
      Started:      Fri, 14 Feb 2020 03:12:13 +0000
      Finished:     Fri, 14 Feb 2020 03:16:15 +0000
    Ready:          True
    Restart Count:  3

--TRUNCATED--

Events:
  Type    Reason          Age                  From               Message
  ----    ------          ----                 ----               -------
  Normal  Scheduled       32m                  default-scheduler  Successfully assigned default/pod-apache to node2
  Normal  Killing         9m32s (x2 over 13m)  kubelet, node2     Stopping container apache
  Normal  SandboxChanged  9m32s                kubelet, node2     Pod sandbox changed, it will be killed and re-created.
  Normal  Pulling         9m30s (x5 over 32m)  kubelet, node2     Pulling image "httpd"
  Normal  Pulled          9m29s (x5 over 32m)  kubelet, node2     Successfully pulled image "httpd"
  Normal  Created         9m27s (x5 over 31m)  kubelet, node2     Created container apache
  Normal  Started         9m27s (x5 over 31m)  kubelet, node2     Started container apache

```

Although there are slight changes in the status of the Pod, in each case it's clear that Kubernetes montiors the underlying Docker containers 
and auto recovers them when they are removed

--end-of-post--
