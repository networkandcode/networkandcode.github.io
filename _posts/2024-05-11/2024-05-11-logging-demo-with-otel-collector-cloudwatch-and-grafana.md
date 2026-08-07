---
canonical_url: "https://dev.to/aws-builders/logging-demo-with-otel-collector-cloudwatch-and-grafana-53l4"
date: "2024-05-11"
title: "Logging demo with OTEL Collector, CloudWatch and Grafana"
tags: "aws, monitoring, kubernetes, cloudnative"
categories: "aws, monitoring, kubernetes, cloudnative"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/logging-demo-with-otel-collector-cloudwatch-and-grafana-53l4)**

Hello :wave:, in this post, we would be using the OTEL Demo App with OpenTelemetry Collector and export the logs from the microservices in the app to AWS CloudWatch.

Let's get started!!! We can create a separate namespace in the kubernetes cluster with `kubectl create ns otelcol-logs-demo`.

And then create a secret that holds the AWS credentials.
```
kubectl create secret generic aws-credentials \
    --from-literal=AWS_ACCESS_KEY_ID=<access-key-id> \
    --from-literal=AWS_SECRET_ACCESS_KEY=<aws-secret-access-key> \
    -n otelcol-logs-demo
```

We would be deploying open telemetry demo app, otel collector as well as Grafana with a single helm [chart](https://artifacthub.io/packages/helm/opentelemetry-helm/opentelemetry-demo). The chart comes with other components too, we could disable those that we do not need for this lab. Our helm values would like below.
```
$ cat values.yaml 
opentelemetry-collector:
  config:
    exporters:
      awscloudwatchlogs:
        log_group_name: otel-logs-demo
        log_stream_name: otel-demo-app
        region: ap-south-2
    service:
      pipelines:
        logs:
          exporters:
            - awscloudwatchlogs
        metrics: {}
        traces: {}
  extraEnvsFrom:
    - secretRef:
        name: aws-credentials
prometheus:
  enabled: false
jaeger:
  enabled: false
opensearch:
  enabled: false
```
In the values above, we have the cloudwatchlogs exporter section where we specify the region, log group and stream names. We are only setting up logs in the pipeline as we are only dealing with that for this demo. We are then setting the AWS credentials via env vars so that the collector could authenticate and send logs to cloud watch. Then, finally we are disabling certain applications which we do not need for this exercise.

Let's install the chart.
```
helm repo add open-telemetry https://open-telemetry.github.io/opentelemetry-helm-charts

helm install my-otel-demo open-telemetry/opentelemetry-demo -n otelcol-logs-demo -f values.yaml
```
 
Head over to CloudWatch logs in the mentioned region and you should be able to see the log group. And, inside the log group we should have the stream.

We should be able to view the logs, for ex. from cartservice as shown in the screenshot below.
![Logs in console](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lybmwuqzylq4c76grlsv.png)

We can now go to Grafana cloud and add the cloud watch datasource with access credentials.
![CloudWatch datasource in Grafana](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ant4ggluzt0xsp53fgck.png)

And should now be able to see the logs in Grafana for our log group, on the explore tab.
![Logs in Grafana](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/u51cdwvf291792ojdk9q.png)

As a bonus let's try adding a panel that shows the no. of messages per severity.

Add a panel with query as shown in the screenshot below.
![Query in panel for logs](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/d3qa20xo889bzpah1pcj.png)

Go to the transform data tab and apply a transformation to parse the severity_text from the json message.
![JSON transformation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/467gg6pjgpnf0j6gfbgv.png)

And then do a group by transformation to calculate the no. of messages per severity.
![Group by transformation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/raaubd4k51hs43nlv75q.png)

Can choose a visualization type such as pie chart like below.
![Pie chart showing log count by severity](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/84wsbwn6zh65a8oaxxuw.png)

The options I have set in the panel are as follows:
```
Title: Logs by severity
Value options > Show > All values
Legend > Legend values: Value, Percent
```

Ok that's it for this post, we saw how to get logs from the otel demo app via open collector to AWS CloudWatch Logs and explored it on Grafana with a sample visualization. We just need to delete the namespace with `kubectl delete ns otelcol-logs-demo` so that logs are not sent to AWS cloudwatch. Thanks for reading !!!
