---
#categories: aws
#title: appwrite > install on aws eks
---

Appwrite is an opensource self hosted backend server, that helps offloading tasks such as 
authentication, storage, database etc. So that developers can focus mainly on their frontend 
development. In this post we shall install Appwrite on AWS EKS(Elastic Kubernetes Service), as a 
deployment and expose it with a LoadBalancer service.

The minimum [resource requirements](https://appwrite.io/docs/installation#systemRequirements) for 
Appwrite are 1CPU, and 2GB RAM, these specs should help while we write the 
[CPU](https://networkandcode.github.io/2019/03/28/kubernetes-pods-containers-resources-cpu/) and 
[Memory](https://networkandcode.github.io/2019/03/28/kubernetes-pods-containers-resources-memory/) 
restrictions in the 
[YAML](https://yaml.org/spec/1.1/#:~:text=YAML%20uses%20three%20dashes%20(%E2%80%9C%20%2D%2D%2D,%E2%80%9D%20%2D%20%E2%80%9C%20%23%20%E2%80%9D).) 
manifest of our kubernetes deployment.

Let's launch an EKS cluster with 
[eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html).
```
$ eksctl create cluster \
--name hacktoberfest-2021 \
--region us-west-2 \
--fargate
```

For more cluster customizations, you may visit the 
[EKS getting started guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html).
Also install [kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl) and 
[AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) on your machine.

Let's check the list of clusters using 
[aws eks cli](https://docs.aws.amazon.com/cli/latest/reference/eks/index.html). We need to specify the 
region or configure the default region prior to listing. In my case its us-west-2.
```
$ aws eks list-clusters --region us-west-2
{
    "clusters": [
        "hacktoberfest-2021"
    ]
}
```

There is only one cluster as shown above. We shall update the kubeconfig, so that we can use kubectl 
to interact with our aks cluster.
```
$ aws eks update-kubeconfig --name hacktoberfest-2021 --region us-west-2
Added new context arn:aws:eks:us-west-2:<account-id>:cluster/hacktoberfest-2021 to /home/networkandcode/.kube/config
```

We can now start using kubectl, lets validate the context first.
```
$ kubectl config current-context
arn:aws:eks:us-west-2:<account-id>:cluster/hacktoberfest-2021
```

Let's create a separate namespace where we can deploy appwrite.
```
$ kubectl create ns appwrite
namespace/appwrite created
```

I am now going to write the manifest for the Appwrite 
[deployment](https://networkandcode.github.io/2019/04/02/kubernetes-deployment/) and 
[service](https://networkandcode.github.io/2019/09/04/kubernetes-expose-pods-using-services/). I would 
be using the image tag 
[0.10.4](https://hub.docker.com/layers/appwrite/appwrite/0.10.4/images/sha256-5eb01c3fb7da40a9ade0862e3669a8ccd23c88c780bfeb835720af0d4df3fbf6?context=explore).
```
$ cat appwrite.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: appwrite
spec:
  selector:
    matchLabels:
      name: appwrite
  template:
    metadata:
      labels:
        name: appwrite
    spec:
      containers:
      - name: appwrite
        image: appwrite/appwrite:0.10.4
        resources:
          requests:
            cpu: 1
            memory: 2Gi
          limits:
            cpu: 1.2
            memory: 2.4Gi
---
apiVersion: v1
kind: Service
metadata:
  name: appwrite
spec:
  selector:
    name: appwrite
  ports:
  - name: http
    port: 80
  type: LoadBalancer
```

It's time to create the kubernetes deployment and service for appwrite.
```
$ kubectl create -f appwrite.yaml 
deployment.apps/appwrite created
service/appwrite created
```

The pod should be up in some time.
```
$ kubectl get po
NAME                       READY   STATUS    RESTARTS   AGE
appwrite-995bd5c85-b6t28   1/1     Running   0          119s
```

Let's check its events.
```
$ kubectl describe po appwrite-995bd5c85-b6t28 | grep -A 15 Events:
Events:
  Type     Reason           Age   From               Message
  ----     ------           ----  ----               -------
  Warning  LoggingDisabled  12m   fargate-scheduler  Disabled logging because aws-logging configmap was not found. configmap "aws-logging" not found
  Normal   Scheduled        11m   fargate-scheduler  Successfully assigned default/appwrite-995bd5c85-b6t28 to fargate-ip-192-168-154-212.us-west-2.compute.internal
  Normal   Pulling          11m   kubelet            Pulling image "appwrite/appwrite:0.10.4"
  Normal   Pulled           11m   kubelet            Successfully pulled image "appwrite/appwrite:0.10.4" in 17.415206687s
  Normal   Created          11m   kubelet            Created container appwrite
  Normal   Started          11m   kubelet            Started container appwrite
```

All seems good so far, let's now see if the endpoints are ok.
```
$ kubectl get ep appwrite
NAME       ENDPOINTS            AGE
appwrite   192.168.154.212:80   15m
```

And this IP should be of our Appwrite pod.
```
$ kubectl get po -o wide | grep 192.168.154.212
appwrite-995bd5c85-b6t28   1/1     Running   0          15m   192.168.154.212   fargate-ip-192-168-154-212.us-west-2.compute.internal   <none>           <none>
```

Excellent, let's now get the external IP of our service
```
$ kubectl get svc appwrite
NAME       TYPE           CLUSTER-IP      EXTERNAL-IP                                                              PORT(S)        AGE
appwrite   LoadBalancer   10.100.166.56   ab3d79aa8f6344be295e2a935af952d2-763666154.us-west-2.elb.amazonaws.com   80:30109/TCP   16m

$ kubectl get svc appwrite | awk '{print $4}'
EXTERNAL-IP
ab3d79aa8f6344be295e2a935af952d2-763666154.us-west-2.elb.amazonaws.com
```

Use this IP(thats not an IP though, its an [FQDN](https://kb.iu.edu/d/aiuv)) to access the Appwrite UI 
over the browser.
```


