---
title: kubernetes > add an extra scheduler
categories: kubernetes
---
The kube-scheduler is responsible for scheduling Pods on Nodes, i.e. it would assign Pods to available Nodes, however it is not responsible for running the Pods, which is kubelet's job. A cluster needs to have atleast one scheduler, and its also possible to run multiple schedulers based on the need

We have a k8s cluster launched using kubeadm, and it has one scheduler as follows, in the kube-system namespace
```
networkandcode@k8s-master-0:~$ kubectl get po -n kube-system | grep scheduler
kube-scheduler-k8s-master-0                1/1     Running   3          3d23h
```

Let's check the container image in the scheduler Pod
```
networkandcode@k8s-master-0:~$ kubectl get po kube-scheduler-k8s-master-0 -n kube-system -o jsonpath={.spec.containers[].image}
k8s.gcr.io/kube-scheduler:v1.16.4
```

kube-scheduler is the default scheduler used in Kubernetes, however we could also write custom kubernetes schedulers with custom names.

Let's check one of the Pods' spec and see the schedulerName defined in it, for instance we can check the kube-apiserver which is in the kube-system namespace
```
networkandcode@k8s-master-0:~$ kubectl get po kube-apiserver-k8s-master-0 -n kube-system -o jsonpath={.spec.schedulerName}
default-scheduler
```
The Pod's ```spec.schedulerName``` has the value ```default-scheduler``` which refers to the default kube-scheduler Pod we saw earlier

Let's now launch a second scheduler in our cluster, however we could use the usual kube-scheduler image, but give it a custom name. For this purpose we can leverage the configuration of the default scheduler Pod which is usually stored in ```/etc/kubernetes/manifests/kube-scheduler.yaml``` of the master
```
networkandcode@k8s-master-0:~$ ls /etc/kubernetes/manifests/
etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml
```

We can create a new configuration file for the second scheduler in the same folder by copying contents from the existing file ``kube-scheduler.yaml`` and doing few modifications to it
```
networkandcode@k8s-master-0:~$ cd /etc/kubernetes/manifests
networkandcode@k8s-master-0:~$
networkandcode@k8s-master-0:~$ sudo cp kube-scheduler.yaml kube-extra-scheduler.yaml
```

Before modifying the new file, let's see the logs of the existing scheduler
```
networkandcode@k8s-master:~$ kubectl logs kube-scheduler-k8s-master-0 -n kube-system
I1223 07:26:42.928378       1 serving.go:319] Generated self-signed cert in-memory
I1223 07:26:43.546765       1 server.go:148] Version: v1.16.4
I1223 07:26:43.547054       1 defaults.go:91] TaintNodesByCondition is enabled, PodToleratesNodeTaints predicate is mandatory
W1223 07:26:43.560915       1 authorization.go:47] Authorization is disabled
W1223 07:26:43.561176       1 authentication.go:79] Authentication is disabled
I1223 07:26:43.561271       1 deprecated_insecure_serving.go:51] Serving healthz insecurely on [::]:10251
I1223 07:26:43.564017       1 secure_serving.go:123] Serving securely on 127.0.0.1:10259
I1223 07:26:43.671382       1 leaderelection.go:241] attempting to acquire leader lease  kube-system/kube-scheduler...
I1223 07:27:00.264646       1 leaderelection.go:251] successfully acquired lease kube-system/kube-scheduler
```
The logs show that the default insecure port is 10251 and the default secure port is 10259, as these values are not explicitly mentioned in the manifest ```kube-scheduler.yaml```. Note that the insecure port is deprecated and we could however use it on the new scheduler to avoid port conflicts

These ports should be active on the master
```
kubeTrain@k8s-master-0:~$ telnet localhost 10251
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
^C
Connection closed by foreign host.
kubeTrain@k8s-master-0:~$ telnet localhost 10259
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
```

We need two such ports for the new scheduler to avoid port conflict, let's see if 10255 and 10260 are not used in the cluster, so that we can it use for the new scheduler
```
kubeTrain@k8s-master-0:~$ telnet localhost 10255
Trying 127.0.0.1...
telnet: Unable to connect to remote host: Connection refused

kubeTrain@k8s-master-0:~$ telnet localhost 10260
Trying 127.0.0.1...
telnet: Unable to connect to remote host: Connection refused
```
As the telnet connection is refused, we could use these ports

Let's now modify the new file, so that it would look like
```
networkandcode@k8s-master-0:~$ sudo cat kube-extra-scheduler.yaml
apiVersion: v1
kind: Pod
metadata:
  --TRUNCATED--
  labels:
    component: kube-extra-scheduler
    tier: control-plane
  name: kube-extra-scheduler
  --TRUNCATED--
spec:
containers:
  - command:
    - kube-scheduler
    - --authentication-kubeconfig=/etc/kubernetes/scheduler.conf
    - --authorization-kubeconfig=/etc/kubernetes/scheduler.conf
    - --bind-address=127.0.0.1
    - --kubeconfig=/etc/kubernetes/scheduler.conf
    - --leader-elect=false
    - --scheduler-name=kube-extra-scheduler
    - --port=10255
    - --secure-port=10260
  --TRUNCATED--
    livenessProbe:
      --TRUNCATED--
      httpGet:
        host: 127.0.0.1
        path: /healthz
        port: 10260
        scheme: HTTP
    --TRUNCATED--
    name: kube-extra-scheduler
  --TRUNCATED--
```

In the manifest above we have used the insecure port 10255, secure port as 10260, and the health check was pointed to the secure port 10260. We have disabled the leader election, which would be required when we have multiple schedulers in High Availabilty mode. And we have given the new scheduler, a name 'kube-extra-scheduler'. Once this file is saved, it should automatically create a new scheduler Pod, with out the use of any kubectl create or apply commands.

```
networkandcode@k8s-master:~$ kubectl get po -n kube-system | grep scheduler
kube-extra-scheduler-k8s-master-0          1/1     Running   1          106s
kube-scheduler-k8s-master-0                1/1     Running   17         5d23h
```
The first Pod in the output above refers to the new scheduler, we could use this name in our Pod spec to schedule Pod using the new scheduler instead of the default one.

We can now see the new ports active on the master
```
kubeTrain@k8s-master-0:~$ telnet localhost 10255
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
^C
Connection closed by foreign host.
kubeTrain@k8s-master-0:~$ telnet localhost 10260
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
^CConnection closed by foreign host.
```

Let's define a Pod manifest and specify the scheduler Name there
```
networkandcode@k8s-master:~$ cat ex37-po-extra-scheduler.yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: po37
spec:
  containers:
  - name: ctr37
    image: httpd
  schedulerName: kube-extra-scheduler
...
```

We shall now create the Pod and check its status
```
networkandcode@k8s-master:~$ kubectl create -f ex37-po-extra-scheduler.yaml
pod/po37 created

networkandcode@k8s-master:~$ kubectl get po -o wide
NAME   READY   STATUS    RESTARTS   AGE   IP               NODE         NOMINATED NODE   READINESS GATES
po37   1/1     Running   0          10s   192.168.140.76   k8s-node-2   <none>           <none>
```

Let's see the events of the Pod
```
networkandcode@k8s-master:~$ kubectl describe po po37 | tail -10
Tolerations:     node.kubernetes.io/not-ready:NoExecute for 300s
                 node.kubernetes.io/unreachable:NoExecute for 300s
Events:
  Type    Reason     Age        From                  Message
  ----    ------     ----       ----                  -------
  Normal  Scheduled  <unknown>  kube-extra-scheduler  Successfully assigned default/po37 to k8s-node-2
  Normal  Pulling    84s        kubelet, k8s-node-2   Pulling image "httpd"
  Normal  Pulled     83s        kubelet, k8s-node-2   Successfully pulled image "httpd"
  Normal  Created    83s        kubelet, k8s-node-2   Created container ctr37
  Normal  Started    83s        kubelet, k8s-node-2   Started container ctr37
```

The output above has a 'Scheduled' event thats says 'kube-extra-scheduler' has successfully assigned this Pod to the Node

Clean up
Let's delete the manifest
```
networkandcode@k8s-master:~$ sudo rm /etc/kubernetes/manifests/kube-extra-scheduler.yaml
networkandcode@k8s-master:~$ kubectl get po -n kube-system | grep scheduler
kube-scheduler-k8s-master-0                1/1     Running   17         5d23h
```
The new scheduler Pod is gone now

The Pod would still be running
```
networkandcode@k8s-master:~$ kubectl get po
NAME   READY   STATUS    RESTARTS   AGE
po37   1/1     Running   0          11m
```

This is because the Pod needs the scheduler to only schedule it and not for executing it
```
networkandcode@k8s-master:~$ kubectl describe po po37 | tail -5
  Normal  Scheduled  <unknown>  kube-extra-scheduler  Successfully assigned default/po37 to k8s-node-2
  Normal  Pulling    12m        kubelet, k8s-node-2   Pulling image "httpd"
  Normal  Pulled     12m        kubelet, k8s-node-2   Successfully pulled image "httpd"
  Normal  Created    12m        kubelet, k8s-node-2   Created container ctr37
  Normal  Started    12m        kubelet, k8s-node-2   Started container ctr37
```

Let's delete the Pod, and try creating it again
```
networkandcode@k8s-master:~$ kubectl delete po po37
pod "po37" deleted

networkandcode@k8s-master:~$ kubectl create -f ex37-po-extra-scheduler.yaml
pod/po37 created
```

The Pod would be in Pending state as it couldnt be scheduled by a scheduler which is not present. And the Pod won't show any events as it doesn't get any from the Scheduler
```
networkandcode@k8s-master:~$ kubectl get po po37
NAME   READY   STATUS    RESTARTS   AGE
po37   0/1     Pending   0          2m13s
networkandcode@k8s-master:~$ kubectl describe po po37 | grep Events
Events:          <none>
```

Let's do the cleanup by deleting the Pod
```
networkandcode@k8s-master:~$ kubectl delete po po37
pod "po37" deleted
```
--end-of-post--
