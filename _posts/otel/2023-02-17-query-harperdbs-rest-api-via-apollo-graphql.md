

---
canonical_url: https://dev.to/aws-builders/tracing-demo-with-aws-x-ray-and-grafana-1pb5
date: 2024-04-26
title: Tracing demo with AWS X-Ray and Grafana
categories: aws, grafana, otel, xray
cover_image: https://source.unsplash.com/featured?trace
tags: aws, grafana, kubernetes, otel
---

**This post first appeared on [dev.to](https://dev.to/aws-builders/tracing-demo-with-aws-x-ray-and-grafana-1pb5)**

## Introduction
Hello :wave:, In this post we'll see about sending traces from a demo app to AWS X-Ray via the ADOT(AWS Distro for OpenTelemetry) collector. We would then visualize this on Grafana. Note that we'd deploy the workloads on a kubernetes cluster.

Here is a picture of what we are trying to accomplish:
![Block diagram for the lab](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/d79dr2bjzdphe7d2w3de.png)

Alright, let's get started!!!

## Namespace
We shall deploy the workloads on a separate namespace. Let's create one.
```
kubectl create ns adot-traces-demo
```

## Credentials
Store the AWS credentials as a kubernetes secret.
```
kubectl create secret generic aws-credentials \
    --from-literal=AWS_ACCESS_KEY_ID=<access-key-id> \
    --from-literal=AWS_SECRET_ACCESS_KEY=<aws-secret-access-key> \
    -n adot-traces-demo
```

## ADOT Config
Set the ADOT config in a file.
```
$ cat adot-config.yaml
exporters:
  awsxray:
    region: ap-south-2
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
service:
  pipelines:
    traces:
      exporters:
        - awsxray
      receivers:
        - otlp
```

And create a config map with this file.
```
kubectl create configmap adot-config --from-file=adot-config.yaml -n adot-traces-demo 
```

## ADOT Deployment
Setup deployment spec in a file, that injects the secret we created earlier as environment variables and the configmap as a volume.
```
$ cat adot-deploy.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: adot-collector
  name: adot-collector
spec:
  replicas: 1
  selector:
    matchLabels:
      app: adot-collector
  template:
    metadata:
      labels:
        app: adot-collector
    spec:
      containers:
        - args:
            - '--config=/etc/adot-config.yaml'
          envFrom:
            - secretRef:
                name: aws-credentials
          image: public.ecr.aws/aws-observability/aws-otel-collector:latest
          name: adot-collector
          volumeMounts:
            - mountPath: /etc/adot-config.yaml
              name: config-volume
              subPath: adot-config.yaml
      volumes:
        - configMap:
            name: adot-config
          name: config-volume
```

Create the deployment.
```
kubectl create -f adot-deploy.yaml -n adot-traces-demo
```

The pod in the deployment should be running.
```
$ kubectl get po -n adot-traces-demo
NAME                              READY   STATUS    RESTARTS   AGE
adot-collector-7cbf849b89-b4bkl   1/1     Running   0          3m26s
```

## ADOT Service
We can expose the ADOT deployment with a service spec that exposes the grpc port 4317 as follows.
```
$ cat adot-svc.yaml 
apiVersion: v1
kind: Service
metadata:
  name: adot-collector-service
spec:
  selector:
    app: adot-collector
  ports:
    - protocol: TCP
      port: 4317
      targetPort: 4317
```

We can now create the service.
```
kubectl create -f adot-svc.yaml -n adot-traces-demo
```

The endpoint IP should match with the pod IP.
```
$ kubectl get ep -n adot-traces-demo
NAME                     ENDPOINTS         AGE
adot-collector-service   10.1.3.187:4317   22s

$ kubectl get po -n adot-traces-demo -o wide
NAME                              READY   STATUS    RESTARTS   AGE     IP           NODE             NOMINATED NODE   READINESS GATES
adot-collector-7cbf849b89-b4bkl   1/1     Running   0          7m11s   10.1.3.187   docker-desktop   <none>           <none>
```

## Demo app
We can now deploy the sample demo app which can send traces to ADOT collector, with the following manifest.
```
$ cat k6-tracing-deploy.yaml 
apiVersion: apps/v1
kind: Deployment
metadata:
  name: xk6-tracing
spec:
  replicas: 1
  selector:
    matchLabels:
      app: xk6-tracing
  template:
    metadata:
      labels:
        app: xk6-tracing
    spec:
      containers:
        - env:
            - name: ENDPOINT
              value: adot-collector-service:4317
          image: ghcr.io/grafana/xk6-client-tracing:v0.0.2
          name: xk6-tracing
```

Let's create the deployment.
```
kubectl create -f k6-tracing-deploy.yaml -n adot-traces-demo
```

Both the ADOT collector and k6-tracing pods should now be running.
```
$ kubectl get po -n adot-traces-demo   
NAME                              READY   STATUS    RESTARTS   AGE
adot-collector-7cbf849b89-b4bkl   1/1     Running   0          14m
xk6-tracing-69b48fcfd9-bjzbd      1/1     Running   0          24s
```

## X-Ray
We can now headover to AWS X-Ray,  in `ap-south-2` region that we mentioned in the adot-config.
![Traces in AWS X-Ray](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lzblt5bwa2ikustn0h6h.png)

The nodes(services) shown in the screenshot belong to our demo application. We could filter for traces that passes through a particular service name for ex. article service, like below.
![Traces ](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/793iwmcy6cl1qweessew.png)

If we click on a single trace we should be able to see a complete service map for that trace, that shows all the services that trace traverses.
![Service map for a trace](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/37vtbbx0fkowsnpxtjty.png)

If we go a further down on this we should be able to see the details for segments/spans with in this trace.
![Spans in trace](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ib655esdlfxoxeyr4cac.png)

## Grafana
So we far we were able to see the traces in AWS X-Ray, we can do a similar exercise on Grafana. I am using a Grafana Cloud Free subscription for this lab.

Go to Connections, Add a new connection and search for X-Ray and install it.
![Install X-Ray](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lvks2wrj6m13x11lpsxx.png)

You can then go to datasources, add a new X-Ray datasource with the access key id, secret access key, and default region(I have chosen ap-south-2 which matches with adot config).

![Add X-Ray datasource](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5z1wgvj4cuvlb28tuzkj.png)

All good, we can try adding a new panel, go to dashboards > new dashboard and a new visualization with table as panel type and a sample query for ex. `service(id(name: "article-service"  ))`
![Traces in tabular format](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/o31cgl9cpatnaw8jnhin.png)

We can click on one of the traces we should take us to the explore view where we can see the node graph(service map)
![Node graph for trace in grafana](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/65b4n0id03356ftff66f.png)

We should also see the trace explorer that shows the individual spans.
![Trace explorer in Grafana](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wikqutl9srogd6t62qm4.png)

Okay so we reached this far, that was some fun exploring traces on AWS and Grafana with Open Telemetry. Thank you for reading !!! 
