# Demo - Network Policy

## Create objects in 'frontend' Namespace

### Create Namespace

#### Define Manifest
```
networkandcode@k8s-master-0:~$ cat ns-frontend.yaml <<EOF
---
apiVersion: v1
kind: Namespace
metadata:
  name: frontend
...
EOF
```

#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f ns-frontend.yaml 
namespace/frontend created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get ns frontend
NAME       STATUS   AGE
frontend   Active   35s
```

### Create Deployment

#### Define Manifest
```
networkandcode@k8s-master-0:~$ cat deploy-frontend.yaml <<EOF
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: frontend
spec:
  selector:
    matchLabels:
      role: frontend
  template:
    metadata:
      labels:
        role: frontend
    spec:
      containers:
      - name: frontend
        image: calico/star-probe:v0.1.0
        command:
        - probe
        - --http-port=80
        - --urls=http://frontend.frontend:80/status,http://backend.backend:6379/status,http://client.client:9000/status
        ports:
        - containerPort: 80
...
EOF
```

#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f deploy-frontend.yaml 
deployment.apps/frontend created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get deploy frontend -n frontend
NAME       READY   UP-TO-DATE   AVAILABLE   AGE
frontend   1/1     1            1           2m36s
```

### Create Service

#### Define Manifest
```
networkandcode@k8s-master-0:~$ cat svc-frontend.yaml 
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: frontend
spec:
  selector:
    role: frontend
  ports:
  - port: 80
...
```

#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f svc-frontend.yaml 
service/frontend created
```
#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get svc frontend -n frontend
NAME       TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
frontend   ClusterIP   10.104.202.128   <none>        80/TCP    2m16s
```
  
## Create objects in 'backend' Namsespace

### Create Namespace

#### Define manifest
```
networkandcode@k8s-master-0:~$ cat > ns-backend.yaml <<EOF
---
kind: Namespace
apiVersion: v1
metadata:
  name: backend
...
```
#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f ns-backend.yaml 
namespace/backend created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get ns backend
NAME      STATUS   AGE
backend   Active   25s
```

### Create Deployment

#### Define Manifest
```
networkandcode@k8s-master-0:~$ cat deploy-backend.yaml <<EOF
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: backend
spec:
  selector:
    matchLabels:
      role: backend
  template:
    metadata:
      labels:
        role: backend
    spec:
      containers:
      - name: backend
        image: calico/star-probe:v0.1.0
        command:
        - probe
        - --http-port=6379
        - --urls=http://frontend.frontend:80/status,http://backend.backend:6379/status,http://client.client:9000/status
        ports:
        - containerPort: 6379
...
EOF
```

#### Create API object using Manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f deploy-backend.yaml 
deployment.apps/backend created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get deploy backend -n backend
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
backend   1/1     1            1           24m
```

### Expose Deployment via a ClusterIP service

#### Define manifest
```
networkandcode@k8s-master-0:~$ cat svc-backend.yaml 
---
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: backend
spec:
  ports:
  - port: 6379
  selector:
    role: backend
...
```

#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f svc-backend.yaml 
service/backend created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get svc backend -n backend
NAME      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
backend   ClusterIP   10.96.10.177   <none>        6379/TCP   2m42s
```

##  Create objects in 'mgmt' Namespace

### Create Namespace

#### Define manifest
```
networkandcode@k8s-master-0:~$ cat > ns-mgmt.yaml <<EOF
---
kind: Namespace
apiVersion: v1
metadata:
  name: mgmt
...
EOF
```

#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f ns-mgmt.yaml
namespace/mgmt created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get ns mgmt
NAME   STATUS   AGE
mgmt   Active   18m
```

### Create Deployment


#### Define Manifest
```
networkandcode@k8s-master-0:~$ cat > deploy-mgmt.yaml <<EOF
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: mgmt
  namespace: mgmt
spec:
  selector:
    matchLabels:
      role: mgmt
  template:
    metadata:
      labels:
        role: mgmt
    spec:
      containers:
      - name: mgmt
        image: calico/star-collect:v0.1.0
        ports:
        - containerPort: 9001
...
EOF
```

#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f deploy-mgmt.yaml 
deployment.apps/mgmt created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get deploy mgmt -n mgmt
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
mgmt   1/1     1            1           6m10s
```

### Expose Deployment via a NodePort service

#### Define manifest
```
networkandcode@k8s-master-0:~$ cat > svc-mgmt.yaml <<EOF
---
apiVersion: v1
kind: Service
metadata:
  name: mgmt
  namespace: mgmt
spec:
  selector:
    role: mgmt
  type: NodePort
  ports:
  - port: 9001
...
EOF
```

#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f svc-mgmt.yaml 
service/mgmt created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get svc mgmt -n mgmt
NAME   TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
mgmt   NodePort   10.105.145.220   <none>        9001:32708/TCP   48s
```

## Create objects in 'client' namespace

### Create Namespace

#### Define manifest
```
networkandcode@k8s-master-0:~$ cat > ns-client.yaml <<EOF
---
kind: Namespace
apiVersion: v1
metadata:
  name: client
...
EOF
```

#### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f ns-client.yaml
namespace/client created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get ns client
NAME     STATUS   AGE
client   Active   121m
```

### Create Deployment

#### Define Manifest
```
networkandcode@k8s-master-0:~$ cat > deploy-client.yaml <<EOF
---
kind: Deployment
apiVersion: apps/v1
metadata:
  name: client
  namespace: client
spec:
  selector:
    matchLabels:
      role: client
  template:
    metadata:
      labels:
        role: client
    spec:
      containers:
      - name: client
        image: calico/star-collect:v0.1.0
        ports:
        - containerPort: 9000
...
EOF
```

#### Create API object
```
networkandcode@k8s-master-0:~$ kubectl create -f deploy-client.yaml 
deployment.apps/client created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get deploy client -n client
NAME     READY   UP-TO-DATE   AVAILABLE   AGE
client   1/1     1            1           94m
```

### Expose the deployment using ClusterIP service
```
networkandcode@k8s-master-0:~$ cat svc-client.yaml 
---
apiVersion: v1
kind: Service
metadata:
  name: client
  namespace: client
spec:
  ports:
  - port: 9000
  selector:
    role: client
...
```

### Create API object using manifest
```
networkandcode@k8s-master-0:~$ kubectl create -f svc-client.yaml 
service/client created
```

#### Verify
```
networkandcode@k8s-master-0:~$ kubectl get svc client -n client
NAME     TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
client   ClusterIP   10.108.119.142   <none>        9000/TCP   91m```
```

## Let's access the mgmt UI on NodePort

### Check the node where the mgmt Pod is running
```
networkandcode@k8s-master-0:~$ kubectl get po -o wide -n mgmt | grep mgmt
mgmt-84dd4cc6ff-rrfdj   1/1     Running   0          10d   192.168.11.193   k8s-node-0   <none>           <none>
```

### Let's check the Public IP of the node
