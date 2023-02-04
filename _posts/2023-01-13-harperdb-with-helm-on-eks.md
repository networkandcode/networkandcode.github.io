---
canonical_url: https://dev.to/aws-builders/harperdb-with-helm-on-eks-3fb9
categories: aws, harperdb, helm, kubernetes
date: 2023-01-13
tags: aws, harperdb, helm, kubernetes
title: HarperDB with Helm on EKS
---

This post first appeared on [dev.to](https://dev.to/aws-builders/harperdb-with-helm-on-eks-3fb9)

This post builds on top of [this](https://dev.to/aws-builders/harperdb-on-eks-1bcb) where we discussed how to launch HarperDB on EKS with 
kubectl. Here, we would use those same manifests. But, we would go with the helm cli tool instead of kubectl for the deployment. Please 
check this [link](https://github.com/networkandcode/harperdb-deployments/tree/main/helm-charts/minimal/harperdb) for the final chart we make 
in this post.

Get set go :fire:

First, ensure [helm](https://dev.to/aws-builders/harperdb-on-eks-1bcb) is installed. If you want to use AWS cloud shell for this, please 
click on the shell icon on the top navigation bar of the cloud console, and execute the following.
```
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
$ chmod 700 get_helm.sh
$ sudo yum install openssl -y
$ ./get_helm.sh
```

Ensure the kubeconfig is updated.
```
$ aws eks update-kubeconfig --name k8s-cluster-01
```

Pl. change the cluster name above with what you have created.

Let's just create the namespace with kubectl, rest will be created with helm.
```
$ kubectl create ns harperdb
namespace/harperdb created
```

Create a directory for the helm chart.
```
$ mkdir harperdb
$ cd harperdb
```

Create a directory for templates in the chart.
```
$ mkdir templates
```

Copy the manifests from this [post](https://dev.to/aws-builders/harperdb-on-eks-1bcb) and keep it in the templates directory.
```
$ ls templates/
deploy.yaml  pvc.yaml  secret.yaml  svc.yaml
```

Create the chart file where we would just keep the name and version, we are keeping to hold just the mandatory information, though we can 
add more.
```
$ cat <<EOF > Chart.yaml 
name: harperdb
version: 1.0.0
EOF
```

So what we created so far is our harperdb helm chart, we are staring with chart version 1.0.0.

We can use this to install the release in a separate namespace. The namespace below means the helm release namespace and not the kubernetes 
namespace. And `.` refers to the chart directory which is the current directory.
```
$ helm install harperdb . -n harperdb
NAME: harperdb
LAST DEPLOYED: Fri Jan 13 09:52:08 2023
NAMESPACE: harperdb
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

We are using the same name for both the helm and kubernetes namespaces. Note that the kubernetes namespace is mentioned in all of the 
manifests.
```
$ cat templates/deploy.yaml | grep namespace
  namespace: harperdb
```

The helm release is deployed.
```
$ helm list -n harperdb
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
harperdb        harperdb        1               2023-01-13 09:52:08.953758683 +0000 UTC deployed        harperdb-1.0.0
```

This has deployed the workloads in kubernetes, which we can check with kubectl.
```
$ kubectl get deploy,pvc,secret,svc -n harperdb
NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/harperdb   1/1     1            1           5m11s

NAME                             STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/harperdb   Bound    pvc-6ef558ee-86ad-460d-8379-c34a12aaf283   5Gi        RWO            gp2            5m11s

NAME                                    TYPE                                  DATA   AGE
secret/default-token-llbqm              kubernetes.io/service-account-token   3      3h50m
secret/harperdb                         Opaque                                2      5m11s
secret/sh.helm.release.v1.harperdb.v1   helm.sh/release.v1                    1      5m11s

NAME               TYPE           CLUSTER-IP     EXTERNAL-IP                                                               PORT(S)          
AGE
service/harperdb   LoadBalancer   10.100.29.79   a86501cc7a7024fff92b7212cd844e45-1677629392.us-east-1.elb.amazonaws.com   8080:31549/TCP   
5m11s
```

Let's test with an API call. The endpoint refers to the loadbalancer service.
```
$ HDB_API_ENDPOINT=a86501cc7a7024fff92b7212cd844e45-1677629392.us-east-1.elb.amazonaws.com:8080

$ curl --location --request POST ${HDB_API_ENDPOINT} --header 'Content-Type: application/json' --header 'Authorization: Basic 
YWRtaW46cGFzc3dvcmQxMjM0NQ==' --data-raw '{
    "operation": "create_schema",
    "schema": "uat" 
}'
{"message":"schema 'uat' successfully created"}
```
Awesome, works !!!.

Let's now revisit the helm chart and do a couple changes. For now, we haven't used any values file, which is commonly used with any helm 
chart. We need values when we would like to parameterize certain things in our manifests. For instance, let's say we want to parameterize 
the service port.
```
$ cat <<EOF > values.yaml 
servicePort: 8080
EOF
```

We can the change the port section in the service template to refer to the value from values file.
```
$ cat templates/svc.yaml | grep port
  ports:
    port: {{ .Values.servicePort }}
```

Let's call this chart version 2.0.0 and upgrade our release.
```
$ cat Chart.yaml | grep version
version: 2.0.0

$ helm upgrade harperdb . -n harperdb
Release "harperdb" has been upgraded. Happy Helming!
NAME: harperdb
LAST DEPLOYED: Fri Jan 13 12:35:53 2023
NAMESPACE: harperdb
STATUS: deployed
REVISION: 2
TEST SUITE: None
```

We can verify the service port.
```
$ kubectl get svc harperdb -n harperdb -o jsonpath={.spec.ports[0].port}
8080
```

Let's do another change, this time we would try to refer to the release name and namespace as the name and namespace for each of the 
resources.
```
$ grep -ir .Release templates/
templates/pvc.yaml:  name: {{ .Release.Name }}
templates/pvc.yaml:  namespace: {{ .Release.Namespace }}
templates/svc.yaml:  name: {{ .Release.Name }}
templates/svc.yaml:  namespace: {{ .Release.Namespace }}
templates/deploy.yaml:  name: {{ .Release.Name }}
templates/deploy.yaml:  namespace: {{ .Release.Namespace }}
templates/secret.yaml:  name: {{ .Release.Name }}
templates/secret.yaml:  namespace: {{ .Release.Namespace }}
```
Note you have to modify each file, so that the grep output looks like above.

Let's change the chart version to 3.0.0, and upgrade the release.
```
$ cat Chart.yaml 
name: harperdb
version: 3.0.0

$ helm upgrade harperdb . -n harperdb
```

We can validate.
```
$ kubectl get deploy,pvc,secret,svc -n harperdb | awk '{print $1}'
NAME
deployment.apps/harperdb

NAME
persistentvolumeclaim/harperdb

NAME
secret/default-token-llbqm
secret/harperdb
secret/sh.helm.release.v1.harperdb.v1

NAME
service/harperdb
```

You could see the workload details on the EKS page. Here is a sample screenshot.
![Harperdb on EKS console](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/c8z2wy1enafeytfx084g.png)


All good, so we have reached the end of this post, we saw how to install harperdb with a minimal helm chart, tested it with an API call, and 
tweaked the helm chart a bit to understand some fundamentals of it. Thank you for reading !!!.
