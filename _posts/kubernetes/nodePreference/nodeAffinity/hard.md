We are going to see how to specify hard requirements for Pod(s) to select a Node using ```spec.affinity.nodeAffinity.requiredDuringSchedulingIgnoredDuringExecution```. With this the Pods could be only launched on the Node(s) that matches with the configuration

It's good to have some basic understanding of Deployments and Match expressions to make the best use of this post.

To check the labels on Nodes
```
networkandcode@k8s-master-0:~$ kubectl get no --show-labels
NAME           STATUS   ROLES    AGE     VERSION   LABELS
k8s-master-0   Ready    master   2d23h   v1.16.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master-0,kubernetes.io/os=linux,node-role.kubernetes.io/master=
k8s-node-0     Ready    <none>   2d23h   v1.16.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node-0,kubernetes.io/os=linux
k8s-node-1     Ready    <none>   2d23h   v1.16.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node-1,kubernetes.io/os=linux
k8s-node-2     Ready    <none>   2d23h   v1.16.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node-2,kubernetes.io/os=linux
```

Let's use the label kubernetes.io/hostname for the purpose of this exercise. We are going to define a Deployment manifest as follows
```
networkandcode@k8s-master-0:~$ cat ex36-deploy-node-affinity-hard.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy36
spec:
  selector:
    matchLabels:
      tag: label36
  replicas: 20
  template:
    metadata:
      labels:
        tag: label36
    spec:
      affinity:
        # nodeAffinity configuration starts here
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
              - matchExpressions:
                - key: kubernetes.io/hostname
                  operator: In
                  values: 
                  - k8s-node-0
        # nodeAffinity configuration ends here
      containers:
      - name: ctr35
        image: nginx
...
```

In the Node Affinity configuration above, we are mapping the Pod on to a Node that has the label kubernetes.io/hostname=k8s-node-0.

Let's create the Deployment
```
networkandcode@k8s-master-0:~$ kubectl create -f ex36-deploy-node-affinity-hard.yaml 
deployment.apps/deploy36 created
```

Let's see where the Pods are launched
```
networkandcode@k8s-master-0:~$ kubectl get po -o wide
NAME                        READY   STATUS    RESTARTS   AGE   IP               NODE         NOMINATED NODE   READINESS GATES
deploy36-5585565d99-27vg7   1/1     Running   0          73s   192.168.11.218   k8s-node-0   <none>           <none>
deploy36-5585565d99-2nmnw   1/1     Running   0          73s   192.168.11.215   k8s-node-0   <none>           <none>
deploy36-5585565d99-4tpvj   1/1     Running   0          73s   192.168.11.219   k8s-node-0   <none>           <none>
deploy36-5585565d99-8msj8   1/1     Running   0          73s   192.168.11.217   k8s-node-0   <none>           <none>
deploy36-5585565d99-9892n   1/1     Running   0          73s   192.168.11.210   k8s-node-0   <none>           <none>
deploy36-5585565d99-b2krd   1/1     Running   0          73s   192.168.11.221   k8s-node-0   <none>           <none>
deploy36-5585565d99-c7wwl   1/1     Running   0          73s   192.168.11.223   k8s-node-0   <none>           <none>
deploy36-5585565d99-cpgl4   1/1     Running   0          73s   192.168.11.207   k8s-node-0   <none>           <none>
deploy36-5585565d99-dd78m   1/1     Running   0          73s   192.168.11.222   k8s-node-0   <none>           <none>
deploy36-5585565d99-fczkc   1/1     Running   0          73s   192.168.11.212   k8s-node-0   <none>           <none>
deploy36-5585565d99-g9g5s   1/1     Running   0          73s   192.168.11.216   k8s-node-0   <none>           <none>
deploy36-5585565d99-js828   1/1     Running   0          73s   192.168.11.213   k8s-node-0   <none>           <none>
deploy36-5585565d99-lh6tl   1/1     Running   0          73s   192.168.11.208   k8s-node-0   <none>           <none>
deploy36-5585565d99-m45qd   1/1     Running   0          73s   192.168.11.214   k8s-node-0   <none>           <none>
deploy36-5585565d99-pgkz5   1/1     Running   0          73s   192.168.11.209   k8s-node-0   <none>           <none>
deploy36-5585565d99-rl4c2   1/1     Running   0          73s   192.168.11.225   k8s-node-0   <none>           <none>
deploy36-5585565d99-rxmlw   1/1     Running   0          73s   192.168.11.224   k8s-node-0   <none>           <none>
deploy36-5585565d99-sf2dc   1/1     Running   0          73s   192.168.11.211   k8s-node-0   <none>           <none>
deploy36-5585565d99-trt5d   1/1     Running   0          73s   192.168.11.220   k8s-node-0   <none>           <none>
deploy36-5585565d99-wcbjd   1/1     Running   0          73s   192.168.11.206   k8s-node-0   <none>           <none>
```

Since we have specified hard i.e., mandatory requirement, all the Pods would have to be launched on k8s-node-0

Cleanup 
```networkandcode@k8s-master-0:~$ kubectl delete deploy deploy36
deployment.apps "deploy36" deleted
```

Reference: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#nodeselectorterm-v1-core

--end-of-post--
