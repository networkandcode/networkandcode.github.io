---
canonical_url: "https://dev.to/networkandcode/grafana-otel-app-observability-demo-552j"
date: "2024-07-12"
title: "Grafana OTEL App Observability Demo"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fz61l81rukn698b056t57.png"
tags: "grafana, otel, observability, kubernetes"
categories: "grafana, otel, observability, kubernetes"
---
**This post first appeared on [dev.to](https://dev.to/networkandcode/grafana-otel-app-observability-demo-552j)**

## Introduction
We are going to explore the built in app observability solution on Grafana cloud, which generates some built in dashboards for us. We would be using OTEL traces for this particular demo. You may check the video version here: {% youtube jw2FXDwEFWg %}

We shall install a sample demo app that simulates a microservices environment. It would generate otel compatible traces which are sent to a local alloy instance. From the local alloy, the traces are sent to Grafana's OTLP gateway(alloy) on the cloud.

The setup would typically look as below.
![Solution diagram](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/aofl5n8twcfhbwdt9ocy.png)



Note that certain metrics will be generated from the traces. So traces will be sent to tempo and the generated metrics from the traces will be sent to Mimir. Both Mimir and Tempo on the cloud are available as datasources in Grafana cloud.

## OTLP endpoint
Go to grafana.com, sign in and access your account, the url of which would be like `https://grafana.com/orgs/<org-name>`. Click on the Stack at the top of the page. In my case, I am using a free account and the organization and stack name are both same. Note that I can only have one organization in the free account.

In the manage stack page, there should be an OTLP section, click on it and copy the gateway URL and instance id from there. Note that the instance id would be our username as well. On this page, you may generate a token with the predefined scope `set:alloy-data-write`. This has the sub scopes `metrics:write, logs:write, traces:write, profiles:write, fleet-management:read`. I have generated a new API token with the predefined options and given it a name `app-observability-demo`. Ensure you copy the token.

## Alloy config
My alloy config would look as below. We need to put the username and password from what we collected in the previous step.
```
$ cat config.alloy 

otelcol.receiver.otlp "otlp_receiver" {
  grpc {
    endpoint = "0.0.0.0:4317"
  }

  output {
    traces = [otelcol.exporter.otlphttp.grafana_cloud.input,]
  }
}

otelcol.exporter.otlphttp "grafana_cloud" {
	client {
		endpoint = "https://otlp-gateway-prod-us-east-0.grafana.net/otlp"
		auth     = otelcol.auth.basic.grafana_cloud.handler
	}
}

otelcol.auth.basic "grafana_cloud" {
  username = "<username>"
  password = "<api-token>"
}
```

Create a namespace and then a configmap with this config.
```
kubectl create ns app-o11y-demo

kubectl create configmap \
    alloy-config \
    --namespace app-o11y-demo \
    "--from-file=config.alloy=config.alloy"
```

## Alloy chart
We can define the helm values for alloy by referring to the configmap as follows.
```
$ cat alloy-values.yaml 
alloy:
  configMap:
    create: false
    name: alloy-config
    key: config.alloy
  extraPorts:
  - name: "grpc"
    port: 4317
    targetPort: 4317
    protocol: "TCP"
```

And call this values file in the helmfile.
```
$ cat helmfile.yaml
repositories:
- name: grafana
  url: https://grafana.github.io/helm-charts

releases:
- name: alloy
  chart: grafana/alloy
  namespace: app-o11y-demo
  values:
  - alloy-values.yaml
  version: 0.5.0
```

We can now install the helm chart with helmfile.
```
$ helmfile sync
```

The alloy pod should be running.
```
$ kubectl get po -n app-o11y-demo
NAME                                  READY   STATUS    RESTARTS   AGE
alloy-cd4zp                           2/2     Running   0          6m10s
```

And the service, endpoints can be validated.
```
$ kubectl get svc -n app-o11y-demo
NAME    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)              AGE
alloy   ClusterIP   10.100.121.96   <none>        12345/TCP,4317/TCP   6m55s

$ kubectl get ep -n app-o11y-demo
NAME    ENDPOINTS                          AGE
alloy   10.1.4.159:12345,10.1.4.159:4317   7m11s

$ kubectl get po -n app-o11y-demo -o wide
NAME                                  READY   STATUS    RESTARTS   AGE     IP           NODE             NOMINATED NODE   READINESS GATES
alloy-cd4zp                           2/2     Running   0          7m27s   10.1.4.159   docker-desktop   <none>           <none>
```

## Demo app
We can now deploy a demo app that would generate traces and send it alloy via grpc. The manifest for which is as follows.
```
$ cat xk6-client-tracing.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: xk6-client-tracing
  namespace: app-o11y-demo
spec:
  minReadySeconds: 10
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app: xk6-client-tracing
      name: xk6-client-tracing
  template:
    metadata:
      labels:
        app: xk6-client-tracing
        name: xk6-client-tracing
    spec:
      containers:
      - env:
        - name: ENDPOINT
          value: alloy.app-o11y-demo.svc.cluster.local:4317
        image: ghcr.io/grafana/xk6-client-tracing:v0.0.2
        imagePullPolicy: IfNotPresent
        name: xk6-client-tracing
```

Note the ENDPOINT variable above is pointing to the alloy service that we deployed earlier. We can now deploy it with kubectl.
```
$ kubectl create -f xk6-client-tracing.yaml
deployment.apps/xk6-client-tracing created
```

The pod status can be checked.
```
$ kubectl get po -n app-o11y-demo | grep k6
xk6-client-tracing-6c49cdfbdb-cm25h   1/1     Running   0          5m44s
```

If everything works as expected, the demo app should have sent traces to alloy and then to tempo backend in Grafana cloud. Likewise it should sent the trace metrics to alloy and then to Mimir on cloud.

## Grafana cloud
We can now headover to Grafana cloud. The url of which would look like `https://<stack-name>.grafana.net/`. You may go to `Home > Application` and click on `Enable Metrics` and activate it. After that add a new a connection and select `OTLP`. Just scroll down and enter the service name as `shop-backend` as that's the root service of our demo app. Test the connection now, it should be successful.
![OTLP connection successful](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k41fek8ea9q202sgfcr2.png)

Once we click on `Go to Application observability` we should be able to see the pre built dashboards based on the traces and the trace metrics, predominantly based on the RED(Rate, Error, Duration method.
![Shop backend dashboard](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pjpwpxp4j2fbas98x6gb.png)

Note that in our case we are only sending traces from our application and the trace metrics were generated at Grafana cloud. We could also have sent direct metrics for ex. if it's a go application we could have sent go metrics, likewise we could also have send logs from our application, all of this to the same gateway(alloy on cloud). With the just the traces we have a handful of data to debug web app issues.

Also, though shop-backend is our root service, we also have other simulated microservices in this application.
![Services page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tdd7qunhgjeffsbim1pk.png)

There are a lot of other options in these built in dashboards to explore. Though we have these built in dashboards, we could also built any custom dashboards. For ex. let's explore what we get in the explore pane keeping tempo as the datasource and build a complete service map for all the services that are part of our demo app. Note that the service map from this is shown in the cover image of the blog.
![Explore trace](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2os6uphastchwsov5j5d.png)

Let's try one more for the trace metrics with mimir as the datasource.
![Explore metrics](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ur4puigobj2q8f2pckyq.png)

## Summary
Alright so we have come to the end of this post, we saw how one of Grafana cloud's solutions around app observability could help us get built in dashboards quite quickly once the data starts flowing to the cloud backend. However note that instrumentation is still necessary on the app side, we were able to get a demo app that already had the OTEL tracing instrumentation for us. As a cleanup check you may run the following commands:
```
helm uninstall alloy -n app-o11y-demo
kubectl delete -f xk6-client-tracing.yaml

# if you also want to delete the ns
kubectl delete ns app-o11y-demo
``` 

Thanks for reading!!!
