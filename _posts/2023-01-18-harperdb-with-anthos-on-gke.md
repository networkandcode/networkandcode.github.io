---
canonical_url: https://dev.to/networkandcode/harperdb-with-anthos-on-gke-2nef
categories: anthos, gke, harperdb, kubernetes
date: 2023-01-18
tags: anthos, gke, harperdb, kubernetes
title: HarperDB with Anthos on GKE
---

This post first appeared on [dev.to](https://dev.to/networkandcode/harperdb-with-anthos-on-gke-2nef)

## Introduction
[Anthos](https://cloud.google.com/anthos) is a service from Google cloud using which we can deploy and manage workloads using various 
options such as cloud run, GKE, self managed clusters, hybrid cloud clusters, edge based workloads and so on. In this post, we would focus 
on the autopilot GKE based cluster and deploy [HarperDB](https://harperdb.io) on it with a Helm chart. Please check this 
[link](https://github.com/networkandcode/harperdb-deployments/tree/main/helm-charts/minimal/harperdb) for the helm chart, we use in this 
post.

Let's get started... 

## Enable Anthos
Search for Anthos on the Google cloud console and enable the Anthos API.
![Search for Anthos](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/npyylvuegnn9szqyoouf.png)

## GKE
We would be going with an Anthos managed GKE cluster, so  click on the configure option in the auto pilot option.
![Auto pilot](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dp1mleldlecyempgey9o.png)

I have kept all options to their defaults. Wait for the cluster to get created. The notifications link should show the status of creation.
![Notification for cluster creation in progress](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nvk28v8j6jkb8oa4buel.png)

We should now have a GKE cluster by name autopilot-cluster-1.
![Notification for cluster creation completed]
(https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2h66wwysiu3al2u44ync.png)

Refresh the page to see the cluster.
![Un registered cluster](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ccbl0jpoko2l5ixic4y7.png)

## Register
We have created the GKE cluster via Anthos, however we also need to register it. Click register and go back to the clusters page, the 
cluster should show under Anthos managed clusters.
![Anthos managed cluster](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/36jd6nfoyffdkulaqbiy.png)

We can now use the GKE cluster to launch any applications in the usual way with kubectl or helm.

## Kubeconfig
Go the cloud shell and run the following command to update kubeconfig.
```
$ gcloud container clusters get-credentials autopilot-cluster-1 --region us-central1
Fetching cluster endpoint and auth data.
kubeconfig entry generated for autopilot-cluster-1.
```

Both kubectl and helm would use this kubeconfig to interact with the cluster.

## Namespace
Let's create a namespace with kubectl.
```
$ kubectl create ns harperdb
namespace/harperdb created
```

## Helm
We can deploy the Kubernetes objects with Helm, for which let's check if there is any publicly available helm chart for harperdb chart in 
the artifact hub.
```
$ helm search hub harperdb
No results found
```

We don't have a chart yet on the hub. Hence, I would be using a local minimal helm chart, whose files are as follows.
```
$ ls harperdb -tR
harperdb:
templates  Chart.yaml  values.yaml

harperdb/templates:
svc.yaml  deploy.yaml  pvc.yaml  secret.yaml
```

For more info on the contents of files in this chart, pl. checkout this [post](https://dev.to/aws-builders/harperdb-with-helm-on-eks-3fb9).

Alright, so let's install our helm release on the GKE cluster managed by Anthos.
```
$ helm install harperdb . -n harperdb
W0114 05:34:47.808566     817 warnings.go:70] Autopilot set default resource requests for Deployment harperdb/harperdb, as resource requests 
were not specified. See http://g.co/gke/autopilot-defaults
NAME: harperdb
LAST DEPLOYED: Sat Jan 14 05:34:39 2023
NAMESPACE: harperdb
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

## Resources
Though we have not setup any resource requests in the deployment template, the autopilot cluster had enabled it for us. We can check the 
deployment spec to see what they have set. Note that it's a good practice to mention resource requests and limits in the template.
```
$ kubectl get deploy harperdb -n harperdb -o jsonpath={.spec.template.spec.containers[].resources} | jq
{
  "limits": {
    "cpu": "500m",
    "ephemeral-storage": "1Gi",
    "memory": "2Gi"
  },
  "requests": {
    "cpu": "500m",
    "ephemeral-storage": "1Gi",
    "memory": "2Gi"
  }
}
```

## Pod
Check the pod status.
```
$ kubectl get po -n harperdb
NAME                        READY   STATUS    RESTARTS   AGE
harperdb-559d48f4f7-6dftw   1/1     Running   0          6m9s
```

## API test
The pod is running, we can get the service IP and try sending an API call.
```
$ HDB_API_ENDPOINT_IP=$(kubectl get svc harperdb -n harperdb -o jsonpath={.status.loadBalancer.ingress[0].ip})

$ curl --location --request POST http://${HDB_API_ENDPOINT_IP}:8080 --header 'Content-Type: application/json' --header 'Authorization: Basic 
YWRtaW46cGFzc3dvcmQxMjM0NQ==' --data-raw '{
    "operation": "create_schema",
    "schema": "prod"
}'
{"message":"schema 'prod' successfully created"}
```

So our installation went smooth and it's working.

## Clean up 
The clean up involves four steps. Deleting the helm chart directory from cloudshell `rm -rf harperdb`. 

Unregistering the cluster from the Anthos console. 
![Unregister cluster](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/batd1bbwsmgkslp3rsx9.png)

Delete the cluster from the GKE console.
![Delete the cluster](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/fsxmrubutxiaxmdux1ez.png)

Finally disable the Anthos API.
```
$ gcloud services disable anthos.googleapis.com
Warning: Disabling this service will also automatically disable any running Anthos clusters.

Do you want to continue (y/N)?  y
```

## Summary
So we have seen how to create an autopilot cluster from the Anthos console, installed a helm release for HarperDB on it, and tested it with 
a sample schema creation. Thank you for reading !!!
