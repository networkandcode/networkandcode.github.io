---
canonical_url: "https://dev.to/aws-builders/otel-demo-with-and-eks-and-newrelic-3j52"
date: "2024-07-18"
title: "OTEL Demo with EKS and New Relic"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fdyvayx3ij8o3cyyg464r.png"
tags: "aws, newrelic, kubernetes, sre"
categories: "aws, newrelic, kubernetes, sre"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/otel-demo-with-and-eks-and-newrelic-3j52)**

Hi:wave:, In this post we shall deploy the OTEL demo app on EKS, and send the metrics, logs and traces to New Relic.

## Prerequisites
It's assumed you know how to install and use tools such as *eksctl, kubectl, helm, helmfile* and know some observability basics.

## Cluster
Create a cluster on EKS with this command.
```
eksctl create cluster --name newrelic-otel-demo --zones=us-east-1a,us-east-1b
```
Once the cluster is created, the kubeconfig's current context will be automatically changed to it.
```
$ kubectl config current-context
nc@newrelic-otel-demo.us-east-1.eksctl.io
```

## License
We need a license key:key: first from New Relic, log in to the New Relic website and headerover to `Administration > API keys` and copy the license key and set it as a variable. Note that the free account is sufficient for this demo.
```
export NEW_RELIC_LICENSE_KEY='<NEW_RELIC_LICENSE_KEY>'
```

We can create a namespace for our demo and keep a secret in it for the license.
```
$ kubectl create ns otel-demo-newrelic
namespace/newrelic-otel-demo created

$ kubectl create secret generic newrelic-license-key --from-literal=license-key="$NEW_RELIC_LICENSE_KEY" -n otel-demo-newrelic
secret/newrelic-license-key created
```

## Helm
We would be using the following helm values. We have disabled extra components that come along with the helm chart which we do not need for this demo.
```
$ cat otel-demo-newrelic-values.yaml
prometheus:
  enabled: false
opensearch:
  enabled: false
grafana:
  enabled: false
jaeger:
  enabled: false
  
opentelemetry-collector:
  config:
    exporters:
      otlphttp/newrelic:
        endpoint: https://otlp.nr-data.net:4317
        headers:
          api-key: ${NEW_RELIC_LICENSE_KEY}
        tls:
          insecure: false
    service:
      pipelines:
        logs:
          exporters: [otlphttp/newrelic, debug]
        metrics:
          exporters: [otlphttp/newrelic, debug]
          receivers: [httpcheck/frontendproxy, redis, otlp]
        traces:
          exporters: [otlphttp/newrelic, debug]
  extraEnvs:
    - name: NEW_RELIC_LICENSE_KEY
      valueFrom:
        secretKeyRef:
          key: license-key
          name: newrelic-license-key
    - name: OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE
      value: delta
```

And the helmfile would refer to the public helm chart and the helm values file we just defined above.
```
$ cat otel-demo-newrelic-helmfile.yaml
repositories:
- name: open-telemetry
  url: https://open-telemetry.github.io/opentelemetry-helm-charts

releases:
- name: otel-demo-newrelic
  chart: open-telemetry/opentelemetry-demo
  namespace: otel-demo-newrelic
  values:
  - otel-demo-newrelic-values.yaml
```

It's time to deploy the helm release.
```
helmfile sync -f otel-demo-newrelic-helmfile.yaml
```

We can check the helm release.
```
$ helm ls -n otel-demo-newrelic
NAME              	NAMESPACE         	REVISION	UPDATED                             	STATUS  	CHART                    	APP VERSION
otel-demo-newrelic	otel-demo-newrelic	1       	2024-07-17 22:02:13.440621 +0530 IST	deployed	opentelemetry-demo-0.32.1	1.11.0     
```

## Pods
In some time, all the pods should be running. I had seen image pull back off for sometime, however it fixed itself in a while.
```
$ kubectl get po -n otel-demo-newrelic
NAME                                                        READY   STATUS    RESTARTS   AGE
otel-demo-newrelic-accountingservice-76fc85f7f9-vxps4       1/1     Running   0          25m
otel-demo-newrelic-adservice-7f8964f98-z2nqd                1/1     Running   0          25m
otel-demo-newrelic-cartservice-bbdfdc59c-w4cqg              1/1     Running   0          25m
otel-demo-newrelic-checkoutservice-f6fd788db-khgq6          1/1     Running   0          25m
otel-demo-newrelic-currencyservice-f9f77f79d-8n946          1/1     Running   0          25m
otel-demo-newrelic-emailservice-66c84d6b64-frs8b            1/1     Running   0          25m
otel-demo-newrelic-flagd-7444ccd98d-cknxl                   1/1     Running   0          25m
otel-demo-newrelic-frauddetectionservice-7c85f7c6bf-mpbw9   1/1     Running   0          25m
otel-demo-newrelic-frontend-c995cfcdd-dsgvc                 1/1     Running   0          25m
otel-demo-newrelic-frontendproxy-76bb8f75cf-kzmn6           1/1     Running   0          25m
otel-demo-newrelic-imageprovider-66db4b77cf-7rg97           1/1     Running   0          25m
otel-demo-newrelic-kafka-74fbd4c749-dspqm                   1/1     Running   0          25m
otel-demo-newrelic-loadgenerator-864475d886-wtnxs           1/1     Running   0          25m
otel-demo-newrelic-otelcol-6b89d8dd84-l5mx4                 1/1     Running   0          25m
otel-demo-newrelic-paymentservice-59677d8c8f-bds4f          1/1     Running   0          25m
otel-demo-newrelic-productcatalogservice-845d79f865-6hs7c   1/1     Running   0          25m
otel-demo-newrelic-quoteservice-76b5f85685-5zz86            1/1     Running   0          25m
otel-demo-newrelic-recommendationservice-8d6bb74c-6zfm4     1/1     Running   0          25m
otel-demo-newrelic-shippingservice-6d44b76489-n4tlw         1/1     Running   0          25m
otel-demo-newrelic-valkey-7f5ffc95ff-wz9zg                  1/1     Running   0          25m
```

## New Relic
We can now go to New Relic and see if the data is flowing. Check `All Entities > Services-OpenTelemetry`, we should start seeing the data for all our services.
![OTEL services in New Relic](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/32cb057vguyztxp16ksp.png)

We could either click on one of the service names on the pic above, or choose a service from the `APM & Services` section to see quite a lot of information about a particular service including built-in dashboards:chart_with_upwards_trend:.
![Service overview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6vx8ybuguc2kslrrcow9.png)

We could also check the traces page for a particular service, as we are sending traces too, based on our otel collector configuration.
![Traces page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dlc7t4hwg7uvvw3o6f0r.png)

Already a lot of information, forget about creating custom panels or alerts :smiley:, understading and managing what we have already given by New Relic is in itself a great administration task:wink:.

Yet we will try to run a simple query using the query builder.
![Query builder](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kiplq8gsx8o0rr8b4wla.png)

We could make custom dashboards with such queries. Alright so that's the end of this post. We just saw how we can use the open telemetry collector to send observability data to newrelic and just explored some of the UI functionalities on New Relic. See below for the housekeeping check.

## Cleanup
Note that free account comes with a data ingestion limit of 100GB per month. I think it ingested around 17GB approximately for about 10 hours(I left my cluster ON and more than 85% of data was coming from traces). So it's a good idea to stop sending traffic once your demo is done, so you can leverage the free limit later when required.

Delete the namespace to delete all the objects we created in the kubernetes cluster for this demo. This would stop sending data to newrelic.
```
kubectl delete ns otel-demo-newrelic
namespace "otel-demo-newrelic" deleted
```

Also you may unset the license key variable.
```
unset NEW_RELIC_LICENSE_KEY
```

Finally delete the cluster.
```
eksctl delete cluster --name newrelic-otel-demo --region=us-east-1
```

Thank you for reading !!!.
