---
title: kubernetes > configure soft node affinity
categories: kubernetes
---

The Node Affinity feature we are going to see here helps the Pod(s) to prefer launching on Node(s) of choice, the associated section in the Pod manifest is ```spec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution```

It's good to some have understanding of Deployments to make better use of this post

We have a cluster of 3 nodes
```
networkandcode@k8s-master-0:~$ kubectl get no
NAME           STATUS   ROLES    AGE   VERSION
k8s-master-0   Ready    master   2d    v1.16.3
k8s-node-0     Ready    <none>   2d    v1.16.3
k8s-node-1     Ready    <none>   2d    v1.16.3
k8s-node-2     Ready    <none>   2d    v1.16.3
```

Let's check the existing labels on the instances
```
networkandcode@k8s-master-0:~$ kubectl get nodes --show-labels
NAME           STATUS   ROLES    AGE     VERSION   LABELS
k8s-master-0   Ready    master   2d18h   v1.16.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master-0,kubernetes.io/os=linux,node-role.kubernetes.io/master=
k8s-node-0     Ready    <none>   2d18h   v1.16.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node-0,kubernetes.io/os=linux
k8s-node-1     Ready    <none>   2d18h   v1.16.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node-1,kubernetes.io/os=linux
k8s-node-2     Ready    <none>   2d18h   v1.16.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node-2,kubernetes.io/os=linux
```
Let's go with the kubernetes.io/hostname label for our exercise, as it is unique for each instance. We are now going to define a deployment with 20 replicas
```
networkandcode@k8s-master-0:~$ cat ex35-deploy-node-affinity-soft.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy35
spec:
  selector:
    matchLabels:
      tag: label35
  replicas: 20
  template:
    metadata:
      labels:
        tag: label35
    spec:
      affinity:
        # nodeAffinity configuration starts here
        nodeAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 1
            preference:
              matchExpressions:
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
The weight parameter in the manifest above is associated with the preference section, and it ranges from 1 to 100, higher number denoting higher preference, we could have a list of such preferences and associated weights, so while the Pod gets scheduled it could prefer one among the list based on the weight. However here we only have a single preference section with associated weight 1. The weight is going to be considered in some artithmetic calculation, when there are multiple matchExpressions too. Our case is simple though as we only have a single target node i.e., node-0. The Pods of this Deployment are going to prefer k8s-node-0 based on a match expression we have set.

Let's launch the deployment
```
networkandcode@k8s-master-0:~$ kubectl create -f ex35-deploy-node-affinity-soft.yaml 
deployment.apps/deploy35 created
```

We see the Pods are launched on all the nodes
```
networkandcode@k8s-master-0:~$ kubectl get po -o wide 
NAME                        READY   STATUS    RESTARTS   AGE   IP               NODE         NOMINATED NODE   READINESS GATES
deploy35-6df945f555-6kdlx   1/1     Running   0          24m   192.168.140.65   k8s-node-2   <none>           <none>
deploy35-6df945f555-8fs55   1/1     Running   0          24m   192.168.11.200   k8s-node-0   <none>           <none>
deploy35-6df945f555-9ks96   1/1     Running   0          24m   192.168.11.205   k8s-node-0   <none>           <none>
deploy35-6df945f555-9pzvs   1/1     Running   0          24m   192.168.11.203   k8s-node-0   <none>           <none>
deploy35-6df945f555-c6ssc   1/1     Running   0          24m   192.168.109.69   k8s-node-1   <none>           <none>
deploy35-6df945f555-crx2f   1/1     Running   0          24m   192.168.140.67   k8s-node-2   <none>           <none>
deploy35-6df945f555-ddqjv   1/1     Running   0          24m   192.168.11.204   k8s-node-0   <none>           <none>
deploy35-6df945f555-j6wcm   1/1     Running   0          24m   192.168.109.65   k8s-node-1   <none>           <none>
deploy35-6df945f555-jlrbk   1/1     Running   0          24m   192.168.11.196   k8s-node-0   <none>           <none>
deploy35-6df945f555-knhq9   1/1     Running   0          24m   192.168.11.198   k8s-node-0   <none>           <none>
deploy35-6df945f555-n8f6r   1/1     Running   0          24m   192.168.11.199   k8s-node-0   <none>           <none>
deploy35-6df945f555-pnqsv   1/1     Running   0          24m   192.168.140.66   k8s-node-2   <none>           <none>
deploy35-6df945f555-qctx6   1/1     Running   0          24m   192.168.140.68   k8s-node-2   <none>           <none>
deploy35-6df945f555-qp7qk   1/1     Running   0          24m   192.168.11.197   k8s-node-0   <none>           <none>
deploy35-6df945f555-rq55k   1/1     Running   0          24m   192.168.11.201   k8s-node-0   <none>           <none>
deploy35-6df945f555-rr8v2   1/1     Running   0          24m   192.168.11.202   k8s-node-0   <none>           <none>
deploy35-6df945f555-szwvf   1/1     Running   0          24m   192.168.109.66   k8s-node-1   <none>           <none>
deploy35-6df945f555-vc4sv   1/1     Running   0          24m   192.168.109.67   k8s-node-1   <none>           <none>
deploy35-6df945f555-vlcj6   1/1     Running   0          24m   192.168.140.69   k8s-node-2   <none>           <none>
deploy35-6df945f555-zg6wt   1/1     Running   0          24m   192.168.109.68   k8s-node-1   <none>           <none>
```

Let's check the count of Pods launched on node-0
```
networkandcode@k8s-master-0:~$ kubectl get po -o wide | grep node-0 | wc
     10      90    1170
```
So there are 10 Pods as the first output of wc, on the left refers to the no. of lines, so in this case most of the Pods, i.e., 50% of 20 Pods in the Deployment have been launched on node-0 as it was preferred, and rest of the Pods were launched on nodes 1 and 2. This is how soft preference i.e., ```spec.affinity.nodeAffinity.preferredDuringSchedulingIgnoredDuringExecution``` works.

Reference: https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.15/#preferredschedulingterm-v1-core

Cleanup
```
networkandcode@k8s-master-0:~$ kubectl delete deploy deploy35
deployment.apps "deploy35" deleted
```

--end-of-post--
