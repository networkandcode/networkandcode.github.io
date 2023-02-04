---
canonical_url: https://dev.to/aws-builders/harperdb-on-eks-1bcb
categories: aws, eks, harperdb, kubernetes
date: 2023-01-09
tags: aws, eks, harperdb, kubernetes
title: HarperDB on EKS
---

This post first appeared on [dev.to](https://dev.to/aws-builders/harperdb-on-eks-1bcb)

Hi there :wave:, let's see how to deploy HarperDB on EKS, and then test it with an API call from CURL. You can get the Kubernetes manifests 
that we make in this post from this [link](https://github.com/networkandcode/harperdb-deployments/tree/main/kubernetes-manifests).

Hope you are already familiar with topics such as [Deployment](https://youtu.be/udSPJXMU9L4?t=1094), [Load 
Balancer](https://www.youtube.com/watch?v=7o6koGCsoSc) service, [Secret](https://www.youtube.com/watch?v=iTkz1bIacHM) and [Persistent volume 
claim](https://www.youtube.com/watch?v=vqk0Ccd7sio)

Ensure you have the required IAM permissions, have installed the aws, eksctl & kubectl cli tools, and have setup the config and credentials.

For me the config is as follows.
```
$ cat ~/.aws/config
[default]
region=us-east-1
```

## Cluster
We can now create an EKS cluster with eksctl. You may see this [video](https://www.youtube.com/watch?v=rJQb_whepEY) for cluster creation 
from the CLI.
```
$ eksctl create cluster --name eks-cluster --zones=us-east-1a,us-east-1b
```

This has taken around 20 mins for me. Once it's done we can update the kubeconfig.
```
$ aws eks update-kubeconfig --name eks-cluster
```

## Docker hub
We can visit the docker [hub](https://hub.docker.com/r/harperdb/harperdb) page of harperdb to get an idea on the ports, environment 
variables, volume path etc.

They have given an example docker command as below.
```
docker run -d \
  -v /host/directory:/opt/harperdb/hdb \
  -e HDB_ADMIN_USERNAME=HDB_ADMIN \
  -e HDB_ADMIN_PASSWORD=password \
  -p 9925:9925 \
  harperdb/harperdb
```

This tells us the volume mount path in the container is /opt/harperdb/hdb, there are 2 environment variables for username and password, and 
the container port is 9925. Finally the image is harperdb/harperdb.

We now have enough info to start writing our Kubernetes manifests.

## Kubernetes manifests
I am going to create a directory by name harperdb where I would keep all the manifests.
```
$ mkdir harperdb    
$ cd harperdb
```

Let's begin with the environment variables, we can write both username and password in a secret object.
```
$ cat <<EOF > secret.yaml 
---
apiVersion: v1
kind: Secret
metadata:
  name: harperdb
  namespace: harperdb
stringData:
  HDB_ADMIN_USERNAME: admin
  HDB_ADMIN_PASSWORD: password12345
...
EOF
```

We can now go with a persistent volume claim, that can dynamically create an EBS volume of size 5Gi in AWS.
```
$ cat <<EOF > pvc.yaml 
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: harperdb
  namespace: harperdb
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
...
EOF
```

Then comes the deployment manifest, where we can define the container image, refer to the secret for the env vars, and pvc for the volume. 
Note that the volume mount path matches with that in the docker command.
```
$ cat <<EOF > deploy.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: harperdb
  namespace: harperdb
spec:
  selector:
    matchLabels:
      app: harperdb
  template:
    metadata:
      labels:
        app: harperdb
    spec:
      containers:
      - name: harperdb
        image: harperdb/harperdb
        envFrom:
        - secretRef:
            name: harperdb
        volumeMounts:
        - name: data
          mountPath: /opt/harperdb/hdb
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: harperdb
...
EOF
```

Finally, we have to expose the deployment with a service, we know from the docker command that the container port is 9925.
```
$ cat <<EOF > svc.yaml
---
apiVersion: v1
kind: Service
metadata:
  name: harperdb
  namespace: harperdb
spec:
  selector:
    app: harperdb
  type: LoadBalancer
  ports:
  - name: http
    port: 8080
    targetPort: 9925
...
EOF
```
Note that we have used 8080 as the service port.

## Workloads

Create a namespace by name harperdb, where we can create our objects.
```
$ kubectl create ns harperdb
namespace/harperdb created
```

We are good to create objects with the 4 manifests.
```
$ ls
deploy.yaml	pvc.yaml	secret.yaml	svc.yaml

$ kubectl create -f .
deployment.apps/harperdb created
persistentvolumeclaim/harperdb created
secret/harperdb created
service/harperdb created
```

## Fix PVC
The pvc should be in pending status.
```
$ kubectl get pvc
NAME       STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   AGE
harperdb   Pending                                      gp2            7m3s
```

Please follow this [link](https://aws.amazon.com/premiumsupport/knowledge-center/eks-persistent-storage/) to add IAM role in AWS cloud, and 
ebs csi objects on the cluster. This should fix the PVC issue.

Once done, the pvc should be bound to a persistent volume(pv).
```
$ kubectl get pvc -n harperdb    
NAME       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
harperdb   Bound    pvc-7c83e38c-b00a-4194-8c67-ba5c9c1118e7   5Gi        RWO            gp2            9s
```

And the pv should be mapped to an EBS volume.
```
$ kubectl get pv 
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                  STORAGECLASS   REASON   
AGE
pvc-7c83e38c-b00a-4194-8c67-ba5c9c1118e7   5Gi        RWO            Delete           Bound    harperdb/harperdb      gp2                     
64s

$ kubectl describe pv pvc-7c83e38c-b00a-4194-8c67-ba5c9c1118e7 | grep VolumeID
    VolumeID:   vol-0bbca736346f02aa1
```

Note that a persistent volume is a cluster level object and not bound to a namespace. We can check the volume details from the aws cli.
```
$ aws ec2 describe-volumes --volume-ids vol-0bbca736346f02aa1 --query "Volumes[0].Size"      
5

$ aws ec2 describe-volumes --volume-ids vol-0bbca736346f02aa1 --query "Volumes[0].Tags"
[
    {
        "Key": "ebs.csi.aws.com/cluster",
        "Value": "true"
    },
    {
        "Key": "CSIVolumeName",
        "Value": "pvc-7c83e38c-b00a-4194-8c67-ba5c9c1118e7"
    },
    {
        "Key": "kubernetes.io/created-for/pv/name",
        "Value": "pvc-7c83e38c-b00a-4194-8c67-ba5c9c1118e7"
    },
    {
        "Key": "kubernetes.io/created-for/pvc/namespace",
        "Value": "harperdb"
    },
    {
        "Key": "kubernetes.io/created-for/pvc/name",
        "Value": "harperdb"
    }
]
```

## Volume permission fix

So the pvc seems good. Let's check our application status.
```
$ kubectl get po -n harperdb
NAME                        READY   STATUS             RESTARTS      AGE
harperdb-79694c8b75-6ckn7   0/1     CrashLoopBackOff   4 (80s ago)   3m25s
```

The application was crashing, but the volume was getting mounted, and the env vars were fine too. I tried commenting out volumeMounts and 
volume and updated the deployment.
```
$ cat deploy.yaml | grep #
        #volumeMounts:
        #- name: data
          #mountPath: /opt/harperdb/hdb
      #volumes:
      #- name: data
        #persistentVolumeClaim:
          #claimName: harperdb

$ kubectl apply -f deploy.yaml
```

The pod was running, and I checked the permissions of the directory where we need to mount the volume. And subsequently the id of the group.
```
$ kubectl exec -it deploy/harperdb -n harperdb -- bash

ubuntu@harperdb-858cc7967d-5jcqm:~$ ls -l /opt/harperdb
total 0
drwxr-xr-x 11 ubuntu ubuntu 155 Jan  9 06:59 hdb

ubuntu@harperdb-858cc7967d-5jcqm:~$ id
uid=1000(ubuntu) gid=1000(ubuntu) groups=1000(ubuntu)

ubuntu@harperdb-858cc7967d-5jcqm:~$ exit
```

So the group id of the running user is 1000, hence we can set this as the group owner for the volume directory with the fsGroup option. If 
we don't specify this then the mountPath would by default be set with root(user) and root(group) as the owner for the directory and the 
running user ubuntu wouldn't have permissions on the mountPath to create any new files. This 
[video](https://www.youtube.com/watch?v=PzzFsvadZdY) has information about fsGroup.

We have to change the deployment as follows. We have added the security context with the fsGroup.
```
$ cat deploy.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: harperdb
  namespace: harperdb
spec:
  selector:
    matchLabels:
      app: harperdb
  template:
    metadata:
      labels:
        app: harperdb
    spec:
      securityContext:
        fsGroup: 1000
      containers:
      - name: harperdb
        image: harperdb/harperdb
        envFrom:
        - secretRef:
            name: harperdb
        volumeMounts:
        - name: data
          mountPath: /opt/harperdb/hdb
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: harperdb
...
```

Alternately, we could also set mountPath to just /opt/harperdb, where we wouldn't have to set the securityContext. But I thought this is a 
good use case to know about the fsGroup.

Update the deployment.
```
$ kubectl apply -f deploy.yaml
```

Check the workloads.
```
$ kubectl get all -n harperdb
NAME                           READY   STATUS    RESTARTS   AGE
pod/harperdb-cc4f49dfc-m7d5p   1/1     Running   0          55s

NAME               TYPE           CLUSTER-IP     EXTERNAL-IP                                                              PORT(S)          
AGE
service/harperdb   LoadBalancer   10.100.54.78   a0ba701c9c5a4463bb636551c79b4158-169592876.us-east-1.elb.amazonaws.com   8080:31819/TCP   
55s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/harperdb   1/1     1            1           57s

NAME                                 DESIRED   CURRENT   READY   AGE
replicaset.apps/harperdb-cc4f49dfc   1         1         1       57s
```

## API call

Send a CURL command to test schema creation. The endpoint is from the external IP column in the service. You may check this 
[video](https://www.youtube.com/watch?v=25L8VvXgx8w) to know how to obtain the curl command for harperdb.
```
$ HDB_API_ENDPOINT=http://a0ba701c9c5a4463bb636551c79b4158-169592876.us-east-1.elb.amazonaws.com:8080

$ curl --location --request POST ${HDB_API_ENDPOINT} \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM0NQ==' \
--data-raw '{
    "operation": "create_schema",
    "schema": "qa" 
}'

{"message":"schema 'qa' successfully created"}
```

All good, it's working... 

## Persistence

Test persistence by deleting the pod.
```
$ kubectl delete po -n harperdb -l app=harperdb
pod "harperdb-cc4f49dfc-m7d5p" deleted
```

This should launch a new pod.
```
$ kubectl get po -n harperdb
NAME                       READY   STATUS    RESTARTS   AGE
harperdb-cc4f49dfc-c6vnc   1/1     Running   0          57s
```

We can try sending the same API call again.
```
$ curl --location --request POST ${HDB_API_ENDPOINT} \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM0NQ==' \
--data-raw '{
    "operation": "create_schema",
    "schema": "qa"
}'

{"error":"Schema 'qa' already exists"}
```

It's not creating a new schema, because the existing schema is restored from the attached volume. Hence, it's persistent.

## Clean up

Let's do the clean up...

Delete all the objects that were created via manifests.
```
$ kubectl delete -f .
deployment.apps "harperdb" deleted
persistentvolumeclaim "harperdb" deleted
secret "harperdb" deleted
service "harperdb" deleted
```

Then delete the namespace.
```
$ kubectl delete ns harperdb
namespace "harperdb" deleted
```

Delete the folder.
```
$ cd ..
$ rm -rf harperdb
```

Finally delete the cluster.
```
$ eksctl delete cluster --name eks-cluster
```

That's it for the post, Thank you for reading !!!
