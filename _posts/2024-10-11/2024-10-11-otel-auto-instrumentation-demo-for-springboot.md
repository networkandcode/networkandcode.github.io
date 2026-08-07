---
canonical_url: "https://dev.to/aws-builders/otel-auto-instrumentation-demo-for-springboot-gmk"
date: "2024-10-11"
title: "OTEL Auto Instrumentation Demo for SpringBoot"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fn7bpdgsjgcmqipfbcgb1.png"
tags: "monitoring, springboot, aws, kubernetes"
categories: "monitoring, springboot, aws, kubernetes"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/otel-auto-instrumentation-demo-for-springboot-gmk)**

Hello :wave:, this post is about auto instrumenting a spring boot app with the [otel agent](https://opentelemetry.io/docs/zero-code/java/agent/getting-started/) running on EKS, forward the telemetry signals(metrics, logs, traces) to backends such as prometheus, loki, tempo via the open telemetry collector, and visualize those in Grafana. The setup is as in the diagram below:
![Setup](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9njwlqldhpacf50hm8dl.png)
Note that the datasources are added on Grafana, which means Grafana sends them API requests to fetch the data.

Alright, let's get started!

## Prerequisites
Ensure you have installed tools such as the aws cli, eksctl, git, docker, kubectl, helm and that you have authenticated to aws from cli.

## Setup the demo app
Let's clone a simple spring boot app from github, and switch to complete directory, where the application code is present.
```
git clone https://github.com/spring-guides/gs-rest-service.git

cd gs-rest-service/complete
```

We can add a logger to the application in the controller class.
```java
cat > src/main/java/com/example/restservice/GreetingController.java <<EOF 
package com.example.restservice;

import java.util.concurrent.atomic.AtomicLong;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class GreetingController {

        private static final String template = "Hello, %s!";
        private final AtomicLong counter = new AtomicLong();

        private final Logger logger = LoggerFactory.getLogger(GreetingController.class);

        @GetMapping("/greeting")
        public Greeting greeting(@RequestParam(value = "name", defaultValue = "World") String name) {
                logger.info("Received GET greeting request for {}", name);
                return new Greeting(counter.incrementAndGet(), String.format(template, name));
        }
} 
EOF
```

## Build the Docker image
Add a dockerfile to containerize this application, also include the otel agent in it with the curl command.  Note that I'm using maven for the build, however the app has both maven and gradle specs, so you can build it with gradle too just by changing the line in dockerfile from `./mvnw clean package` to `./gradlew clean build`.
```
cat > Dockerfile <<EOF
# Build
FROM eclipse-temurin:17-jdk-jammy AS build
WORKDIR /usr/app
COPY . .
RUN ./mvnw clean package

# Run
FROM eclipse-temurin:17-jre-jammy
WORKDIR /usr/app
COPY --from=build /usr/app/target/*.jar ./app.jar
RUN curl -O -L https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/latest/download/opentelemetry-javaagent.jar
RUN useradd appuser && chown -R appuser /usr/app
USER appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3   CMD curl -f http://localhost:8080/ || exit 1 
ENTRYPOINT ["java", "-javaagent:/usr/app/opentelemetry-javaagent.jar", "-jar", "/usr/app/app.jar"]
EOF
```

We have added the healthcheck command and a nonroot user in the dockerfile above, so that it passes security checks. We can lint/scan it with trivy as follows.
```
docker run --rm -v ./Dockerfile:/tmp/Dockerfile aquasec/trivy config /tmp/Dockerfile
```

Add the dockerignore file so that we are not copying unwanted files to the image.
```
cat > .dockerignore <<EOF
Dockerfile
manifest.yml
build
target
EOF
```

We can build the image now.
```
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

export REGION=us-east-1

docker build -t $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/otel-auto-java-demo .
```

## Push the image to ECR
The image we built can be pushed to ECR, for which we have to first create a repo there.
```
aws ecr create-repository --repository-name otel-auto-java-demo --region $REGION
```

Then, get the ecr password and login with it from docker.
```
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
```
You should get `Login Succeeded`.

The image can now be pushed to ECR with the docker cli.
```
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/otel-auto-java-demo 
```

## Create EKS cluster
I'm going to create an EKS cluster with the eksctl cli.
```
eksctl create cluster --name otel-auto-java-demo --zones=us-east-1a,us-east-1b
```
When this is done, your kubeconfig should have got updated and you should have scoped to the new cluster. However you can keep this command handy to switch to the correct context `aws eks update-kubeconfig --region $REGION --name otel-auto-java-demo`.

## Setup helmfile
We can deploy our tool stack with [helmfile](https://github.com/helmfile/helmfile/releases). First check the architecture, for ex. with a command like `uname -m` and then install helmfile with the correct package. In my case the architecture was `x86_64` and hence, I am installing the `linux_amd64` package.
```
uname -m
wget https://github.com/helmfile/helmfile/releases/download/v1.0.0-rc.5/helmfile_1.0.0-rc.5_linux_amd64.tar.gz

tar -xvf helmfile_1.0.0-rc.5_linux_amd64.tar.gz 

rm LICENSE README.md README-zh_CN.md 

sudo mv helmfile /usr/bin/helmfile
```

Note that you would also need [helm](https://helm.sh/docs/intro/install/) as helmfile is a wrapper around helm.

Our helmfile should look as follows.
```
cat > helmfile.yaml <<EOF
repositories:
- name: open-telemetry
  url: https://open-telemetry.github.io/opentelemetry-helm-charts
- name: prometheus-community
  url: https://prometheus-community.github.io/helm-charts
- name: grafana
  url: https://grafana.github.io/helm-charts

releases:
- name: otel-collector
  chart: open-telemetry/opentelemetry-collector
  namespace: otel-auto-java-demo
  values:
  - otel-collector-values.yaml
- name: prometheus
  chart: prometheus-community/prometheus
  namespace: otel-auto-java-demo
  values:
  - prometheus-values.yaml
- name: loki
  chart: grafana/loki
  namespace: otel-auto-java-demo
  values:
  - loki-values.yaml
- name: tempo
  chart: grafana/tempo-distributed
  namespace: otel-auto-java-demo
  values:
  - tempo-values.yaml
- name: grafana
  chart: grafana/grafana
  namespace: otel-auto-java-demo
  values:
  - grafana-values.yaml
EOF
```

## Setup Helm values
This section shows the different values files, that we are using in the helmfile.

### OTEL collector
Let's begin with the otel collector values. Some of the sections such as receivers are omitted, as anyway they will come from the default [values](https://artifacthub.io/packages/helm/opentelemetry-helm/opentelemetry-collector?modal=values) file.
```
cat > otel-collector-values.yaml <<EOF
image:
  repository: "otel/opentelemetry-collector-contrib"
mode: deployment
resources:
  limits:
    cpu: 250m
    memory: 512Mi
config:
  processors:
    batch:
      send_batch_max_size: 500
      send_batch_size: 50
      timeout: 5s
  exporters:
    otlphttp/prometheus:
      endpoint: "http://prometheus-server/api/v1/otlp"
    loki:
      endpoint: "http://loki-write:3100/loki/api/v1/push"
    otlp:
      endpoint: "http://tempo-distributor:4317"
      tls:
        insecure: true
  service:
    pipelines:
      metrics:
        receivers: [otlp]
        exporters: [otlphttp/prometheus]
      logs:
        exporters: [loki]
      traces:
        receivers: [otlp]
        exporters: [otlp]
EOF
```

### Prometheus
We are disabling components that we do not need for this exercise, from the prometheus chart, and we are enabling otlp write receiver, as we are sending metric from the otel collector to prometheus via otlp/http.
```
cat > prometheus-values.yaml <<EOF
alertmanager:
  enabled: false
prometheus-pushgateway:
  enabled: false
prometheus-node-exporter:
  enabled: false
kube-state-metrics:
  enabled: false
server:
  extraFlags:
  - "enable-feature=exemplar-storage"
  - "enable-feature=otlp-write-receiver"
EOF
```

### Loki
We are installing loki in the [simple scalable](https://grafana.com/docs/loki/latest/setup/install/helm/install-scalable/) mode. And have disabled some of the components such as chunks cache, results cache, gateway to keep it simple.
```
cat > loki-values.yaml <<EOF
# https://grafana.com/docs/loki/latest/operations/caching/
chunksCache:
  enabled: false
resultsCache:
  enabled: false
gateway:
  enabled: false

limits_config:
  allow_structured_metadata: true

loki:
  auth_enabled: false
  schemaConfig:
    configs:
      - from: 2024-04-01
        store: tsdb
        object_store: s3
        schema: v13
        index:
          prefix: loki_index_
          period: 24h
  ingester:
    chunk_encoding: snappy
  tracing:
    enabled: true
  querier:
    # Default is 4, if you have enough memory and CPU you can increase, reduce if OOMing
    max_concurrent: 4

deploymentMode: SimpleScalable

backend:
  replicas: 3
read:
  replicas: 3
write:
  replicas: 3

# Enable minio for storage
minio:
  enabled: true

# Zero out replica counts of other deployment modes
singleBinary:
  replicas: 0

ingester:
  replicas: 0
querier:
  replicas: 0
queryFrontend:
  replicas: 0
queryScheduler:
  replicas: 0
distributor:
  replicas: 0
compactor:
  replicas: 0
indexGateway:
  replicas: 0
bloomCompactor:
  replicas: 0
bloomGateway:
  replicas: 0
EOF
```

### Tempo
This is our tempo values. Note that we are using the tempo distributed chart, i.e. the microservices mode.
```
cat > tempo-values.yaml <<EOF 
gateway:
  enabled: true
traces:
  otlp:
    grpc:
      enabled: true
EOF
```

### Grafana
And finally grafana, with datasources provisioned.
```
cat > grafana-values.yaml <<EOF
service:
  type: LoadBalancer
datasources:
  datasources.yaml:
    apiVersion: 1
    datasources:
    - name: Prometheus
      type: prometheus
      url: http://prometheus-server
    - name: Loki
      type: loki
      url: http://loki-read:3100
    - name: Tempo
      type: tempo
      url: http://tempo-gateway
EOF
```

## Setup prerequisites for provisioning volumes
We need to setup a few things on AWS so that we are able to provision volumes that are needed for some of our tools. First we have to install the CSI driver on the cluster.
```
eksctl create addon --name aws-ebs-csi-driver --cluster otel-auto-java-demo --region $REGION
```

We have to then the modify the nodegroup's IAM role with appropriate permissions, for which we have to first find the role. Note that the role suffix could be different in your case.
```
$ aws iam list-roles | jq -r '.Roles[].RoleName' | grep  otel-auto-java | grep node
eksctl-otel-auto-java-demo-nodegr-NodeInstanceRole-tUmFVlpwtUfc
```

We can then attach the appropriate policy to the role.
```
$ aws iam attach-role-policy   --role-name eksctl-otel-auto-java-demo-nodegr-NodeInstanceRole-tUmFVlpwtUfc   --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy
```

And then we can set the gp2 storage class as default. This is because the volumes we install would look for the default storage class.
```
$ kubectl patch storageclass gp2 -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
storageclass.storage.k8s.io/gp2 patched
```

The word `default` should now appear in the storage class.
```
$ kubectl get storageclass
NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
gp2 (default)   kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   false                  20h
```

## Deploy the tool stack
Alright, done some heavy lifting, we can install our tool stack now.
```
helmfile sync
```

Once the installation is complete you can check the release and pods status with commands such as `helm ls -A`, `kubectl get po -A`.

## Deploy the demo app
We should now deploy the demo app with the following manifest, which has both deployment and service configuration.
```
cat > demoapp.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: otel-auto-java-demo
  labels:
    app: otel-auto-java-demo
  namespace: otel-auto-java-demo
spec:
  selector:
    matchLabels:
      app: otel-auto-java-demo
  template:
    metadata:
      labels:
        app: otel-auto-java-demo
    spec:
      containers:
        - name: otel-auto-java-demo
          image: $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/otel-auto-java-demo:latest
          # https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/
          env:
          - name: OTEL_EXPORTER_OTLP_ENDPOINT
            value: "http://otel-collector-opentelemetry-collector:4317"
          - name: OTEL_EXPORTER_OTLP_PROTOCOL
            value: grpc
          imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: otel-auto-java-demo
  namespace: otel-auto-java-demo
spec:
  type: ClusterIP
  selector:
    app: otel-auto-java-demo
  ports:
    - port: 80
      targetPort: 8080
EOF
```

Note that the above file has env vars for account id and region, hence we can use envsubst before applying the manifest.
```
envsubst < demoapp.yaml | kubectl apply -f -
```

## Make some api calls to the app
We can expose the service, so that we can send some calls on the localhost.
```
kubectl port-forward svc/otel-java-demo -n otel-java-demo 8080:80
```

Make a few api calls with curl, from a different terminal.
```
$ curl localhost:8080/greeting; echo
{"id":8,"content":"Hello, World!"}

$ curl localhost:8080/greeting?name=Earth; echo
{"id":13,"content":"Hello, Earth!"}

$ curl localhost:8080/greeting?name=Universe; echo
{"id":14,"content":"Hello, Universe!"}
```

When done, you may stop the port fowarding with Ctrl C.

## Monitor the app
We can now monitor our app from Grafana with the LoadBalancer URL of Grafana.
```
kubectl get svc grafana -n otel-auto-java-demo
NAME      TYPE           CLUSTER-IP     EXTERNAL-IP                                                               PORT(S)        AGE
grafana   LoadBalancer   10.100.69.33   acdbcf3ef71674a0b9a8be554d62db7c-2016095508.us-east-1.elb.amazonaws.com   80:32283/TCP   73m
```
Just access the URL above with `http://` on the browser, the URL would be different in your case. The username is admin, and the password can be obtained from the secret as shown below. The password would be different in your case.
```
$ kubectl get secret grafana -n otel-auto-java-demo -o jsonpath={.data.admin-password} | base64 -d ; echo
3cOFbY8Q5H5Qz4CHHJvJZ2a2UDvSeQnmRrFIQlsv
```

Go to explore tab on let's try one query each for metrics, logs and traces.

Metrics preview:
![Metrics preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8ib0xn0ezd45c75ca87z.png)

Logs preview:
![Logs preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2gxj6l04dyx30c4f5ek1.png)

Traces preview:
![Traces preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k5821qbx2nxxda2nk2uc.png)

Note that we only added two [env vars](https://opentelemetry.io/docs/specs/otel/configuration/sdk-environment-variables/) in our demo app, we haven't added any extra vars such as resource attributes, service name etc. Just to show that  it would pick it from the artifact id if not provided. As shown in the image previews above, for metrics(prometheus) the it would become the `job` label, and for logs(loki) it would become the `job` and `service_name` label and for traces(tempo) it would be the `resource.service.name` tag. 
```
$ cat pom.xml
--TRUNCATED--
<groupId>com.example</groupId>
	<artifactId>rest-service-complete</artifactId>
--TRUNCATED--
```

So, we were able to get the telemetry data successfully from our SpringBoot Java App all the way down to Grafana. With this as base, we could now build custom dashboards as we like, do some correlation by modifying datasource config, etc. 

## Cleanup checklist
- Delete the helm releases: `helmfile destroy`
- Delete the PVCs: `kubectl delete pvc --all -n otel-auto-java-demo`
- Delete the demo app (optional): `kubectl delete -f demoapp.yaml`
- Delete the cluster: `eksctl delete cluster --name otel-auto-java-demo --region $REGION`
- Delete the ECR repo: `aws ecr delete-repository --repository-name otel-auto-java-demo --region $REGION --force`

Thank you for reading :)
