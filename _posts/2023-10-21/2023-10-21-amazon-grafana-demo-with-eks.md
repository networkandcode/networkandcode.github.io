---
canonical_url: "https://dev.to/aws-builders/amazon-grafana-demo-with-eks-3mfp"
date: "2023-10-21"
title: "Amazon Grafana demo with EKS"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fsource.unsplash.com%2Ffeatured%2F%3Fcolor%26box"
tags: "sre, devops, aws, kubernetes"
categories: "sre, devops, aws, kubernetes"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/amazon-grafana-demo-with-eks-3mfp)**

Hello :wave:, in the previous [post](https://dev.to/aws-builders/grafana-on-aws-marketplace-3189), we have seen about Grafana Cloud with an AWS subscription. In this post, we are going to see about Amazon Grafana(which is a fully managed service in AWS), with some demo on couple of metrics collected via Prometheus from EKS. Let's get into action!!!

## Create cluster
I have created an EKS cluster for the purpose of this exercise. For more info on creating clusters you can see this [video](https://www.youtube.com/watch?v=rJQb_whepEY).
```
eksctl create cluster --name grafana-demo-eks --zones=us-east-1a,us-east-1b

aws eks list-clusters
```
```
{
    "clusters": [
        "grafana-demo-eks"
    ]
}
```

## Install Prometheus
We would be fetching metrics with prometheus, hence we can add the helm repo for prometheus on the local system.
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

Scope to the cluster and create a separate namespace on which we can install prometheus.
```
aws eks update-kubeconfig --name grafana-demo-eks
kubectl create namespace prometheus
```

The prometheus [chart](https://artifacthub.io/packages/helm/prometheus-community/prometheus) comes with a stack of components, by default. We don't need all of those. For this exercise, we'd  just need the prometheus server and kube-state-metrics. We also don't need persistent volume for this lab. So we can define a values file like below.
```
cat <<EOF > my-values.yaml 
server:
  persistentVolume:
    enabled: false
alertmanager:
  enabled: false
prometheus-pushgateway:
  enabled: false
prometheus-node-exporter:
  enabled: false
EOF
```

We can now install a prometheus helm release with the prometheus helm chart.
```
helm install prometheus prometheus-community/prometheus -n prometheus -f my-values.yaml 
```

The status of helm release installation can be checked.
```
helm ls -n prometheus 
```

And the pods should be running.
```
kubectl get po -n prometheus
NAME                                            READY   STATUS    RESTARTS   AGE
prometheus-kube-state-metrics-59649d78f-249vb   1/1     Running   0          77s
prometheus-server-547848c6c5-xpzcb              2/2     Running   0          77s
```

## Access Prometheus
We can access prometheus via port-forwarding.
```
kubectl port-forward svc/prometheus-server 8080:80 -n prometheus
```
```
Forwarding from 127.0.0.1:8080 -> 9090
Forwarding from [::1]:8080 -> 9090
```
Note: you can press `ctrl c` to stop port fowarding...

You should be able to access the prometheus expression browser on `http://localhost:8080`.

Let's try a sample query `kube_apiserver_clusterip_allocator_allocated_ips` with promql.
![Prometheus expression browser](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jhdas9bbmkclw2d66bcz.png)

So you are seeing a couple of hits, it seems good.

## AMP
We would now setup Amazon Prometheus. The idea is to forward metrics from the local prometheus we installed previously, to Amazon managed Prometheus.
![Amazon Prometheus Icon](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lgfu2z9j4szwwp2fdoap.png)

I have created a workspace in Amazon Prometheus, with the name `grafana-demo-k8s`. Once created, it would show you all useful details that are required to rewrite metrics from our local prometheus. Make a note of the remote write URL on this page.

Follow this [link](https://docs.aws.amazon.com/prometheus/latest/userguide/set-up-irsa.html#set-up-irsa-ingest) to set up service roles for the ingestion of metrics from Amazon EKS clusters.
```
./createIRSA-AMPIngest.sh 
```

Setup variables for the AWS account ID and AMP rewrite URL.
```
ACCOUNT_ID=<ACCOUNT_ID>
REMOTE_WRITE_URL=<REMOTE_WRITE_URL>
```

Update values file with the details of AMP.
```
cat <<EOF > my-values.yaml 
server:
  persistentVolume:
    enabled: false
  remoteWrite:
  - url: ${REMOTE_WRITE_URL}
    sigv4:
      region: us-east-1
    queue_config:
      max_samples_per_send: 1000
      max_shards: 200
      capacity: 2500
alertmanager:
  enabled: false
prometheus-pushgateway:
  enabled: false
prometheus-node-exporter:
  enabled: false

serviceAccounts:
  server:
    name: "amp-iamproxy-ingest-service-account"
    annotations:
      eks.amazonaws.com/role-arn: "arn:aws:iam::${ACCOUNT_ID}:role/amp-iamproxy-ingest-role"
```

Substitue the variables in the values file and make a new file.
```
envsubst < my-values.yaml > my-subst-values.yaml  
```

Upgrade the helm release with the new values file.
```
helm upgrade prometheus prometheus-community/prometheus -n prometheus -f my-subst-values.yaml
```

## Grafana
Now let's set up Amazon Grafana.
![Amazon Grafana](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/f4dtxw61ytxr9k2w5504.png)

I am creating a workspace here, with name `grafana-demo-eks`.
![Create workspace button](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vpy3adsntjx9rw4wch2r.png)

I have selected AWS IAM Identity Center as the authentication method, and created a user with email, first and last name.
![Setup authentication](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6csnwcm09azg6wqo6h2p.png)

A verification link will be sent to this email using which the password could be set.

I am choosing the same VPC as that of the kubernetes cluster. For the AZs I have choosen the private subnet in both. And, default for the security group.
![Network settings](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/cx4azla8kl99h1e13576.png)

Select the data source as AMP.
![AMP](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/niivrwpd2q9k1fe8l959.png)

I have kept rest of the settings to their default and created the workspace. One thing I have noted is there were only two availabe versions of Grafana which are 9.4 and 8.4 for now in Amazon Grafana, where as Grafana cloud had the latest version 10.2.0. Once the workspace is created, you should see a `workspace URL` that can be used to access the Grafana portal.

In th worskspace page, under the authentication tab click `Assign new user or group` and select the correct user that was created earlier. Also make the user admin, as by default it will be given the viewer role.
![Admin role](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bw49d6s0jf5gsq8hjspx.png)

You can login to the workspace URL with the IAM identity email and the password set during email verification.
![Login to Grafana](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k3obh2rr20uyy3dv2hpq.png)

You should see a page like this:
![Amazon grafana portal](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9e9fcl6kydknaqakqbo6.png)

## Visualize on Grafana
Add datasource in Grafana
Go to `Home > Apps > AWS Data Sources > Data sources` and add the AMP datasource like below.
![Add datasource](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/17u6kg5bo7z5ibuuxhi7.png)

Let's try adding a panel:bar_chart:. Go to `Home > Dashboards > New Dashboard` and Add a new panel here. Let's try to see the number of pods in each namespace. The query we use for this purpose is `sum(kube_pod_info) by(namespace)`. Note that the legend at the bottom would show that Last null value as configured in the right side of the screenshot below.
![Pod count per namespace](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yrw2kcyurva9vj1rj7xd.png)
 
So it says the default namespace has 1 pod, the prometheus namespace has 2 pods, and the kube-system has 10 pods. Let's try validating this with kubectl.

```
kubectl get po -n default --no-headers | wc -l; kubectl get po -n prometheus --no-headers | wc -l; kubectl get po -n kube-system --no-headers | wc -l
```
```
       1
       2
      10
```
Awesome, it's matching. I am saving this panel with name `Pod count per namespace`, and given the dashboard the name `grafana-demo-eks`.

Now let's try with one other panel, this time we will see the no. of services by namespace. We can use this query `sum(kube_service_info) by(namespace)`. And instead of the default timeseries visualization, let's try with pie chart. We'll show both value and percent in the pie chart as shown in the screenshot below.
![Pie chart](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7cfyk3tyuea7qyyub41m.png)

We shall validate this too, with kubectl.
```
kubectl get svc -n default --no-headers | wc -l; kubectl get svc -n prometheus --no-headers | wc -l; kubectl get svc -n kube-system --no-headers | wc -l
```
```
       1
       2
       1
```

Cool, the service count per namespace is matching.

Alright, we had some practice with tools like prometheus and grafana in the AWS world with kubernetes. And, we have tried visualizing metrics that are collected by kube-state-metrics. We used prometheus for scraping the metrics from kube-state-metrics, which is ingested to the AMP workspace. We added AMP as a datasource in Grafana to build the panels. So, here is the final look of our 2 panel dashboard.
![Final dashboard](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/l3g3wp42ca64kkbxw45i.png)

So the AWS resources we have created in this exercise are: An EKS cluster, a grafana workspace, and a prometheus workspace. So make sure you are deleting those when you are done, to avoid billing:moneybag:... For EKS cluster jus do it from the cli: `eksctl delete cluster --name grafana-demo-eks`.

Thanks for reading !!!
