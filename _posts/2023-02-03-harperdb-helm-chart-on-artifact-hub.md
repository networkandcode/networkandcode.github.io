---
canonical_url: https://dev.to/networkandcode/harperdb-helm-chart-on-artifact-hub-3066
categories: eks, harperdb, helm, kubernetes
date: 2023-02-03
tags: eks, harperdb, helm, kubernetes
title: HarperDB Helm chart on Artifact Hub
---

This post first appeared on [dev.to](https://dev.to/networkandcode/harperdb-helm-chart-on-artifact-hub-3066)

## Introduction
Hey :wave:, in this post, we shall see how to create a helm chart for HarperDB based on the boilerplate helm chart with the helm cli, 
lint/dry run it and push it to the artifact [hub](https://artifacthub.io), and then reuse it to install a helm release on a Kubernetes 
cluster. You can get the helm chart used in this post from this 
[link](https://github.com/networkandcode/harperdb-deployments/tree/main/helm-charts/standard/harperdb).

You may check this [post](https://dev.to/aws-builders/harperdb-with-helm-on-eks-3fb9) if you are looking to install harperdb with a custom, 
minimal helm chart.

## Search
As of this writing, there is no chart available on artifact hub for harperdb, the screenshot below should validate that.
![HarperDB chart not found in artifact hub](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/idysqmfnelkdj60fe0ii.png)

So our goal is to push the harpderdb chart to artifact hub, so that the search result shows an entry.

Let's give a try on ChatGPT.
![Search for harperdb helm chart on ChatGPT](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2gd3nvxzwcgdgbut9h0y.png)

We could also search from the helm cli, to see if there exists a chart for harperdb. For which you have to first install 
[helm](https://helm.sh/docs/intro/install/) in your system.

On Mac, it could be installed as follows.
```
$ brew install helm
```

Now, we can search for the chart.
```
$ helm search hub harperdb
No results found
```

This result matches with the search we did on website.

## Chart
Ok, we can create our chart. Let's first create a boilerplate chart with the name harperdb.
```
$ helm create harperdb
Creating harperdb
```

A chart is created for us, it's nothing but a directory with a specific layout.
```
$ ls -R harperdb  
Chart.yaml	charts		templates	values.yaml

harperdb/charts:

harperdb/templates:
NOTES.txt		deployment.yaml		ingress.yaml		serviceaccount.yaml
_helpers.tpl		hpa.yaml		service.yaml		tests

harperdb/templates/tests:
test-connection.yaml
```

Let's make a few changes.

Change the appVersion, I am going to use the latest version of harperdb found in the [tags](https://hub.docker.com/r/harperdb/harperdb/tags) 
section at docker hub.
```
$ cat harperdb/Chart.yaml| grep appVersion
appVersion: "1.16.0"

$ sed -i 's/appVersion: "1.16.0"/appVersion: "4.0.4"/g' harperdb/Chart.yaml

$ cat harperdb/Chart.yaml| grep appVersion
appVersion: "4.0.4"
```

We don't need any sub charts for now, so we can remove that directory.
```
$ rm  -r harperdb/charts
```

We can also remove the tests directory.
```
$ rm -r harperdb/templates/tests
```

## Values
We need to make a few modifications in the values file.

### Image
Let's set the image.
```
$ cat harperdb/templates/deployment.yaml | grep image:
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
```

The tag can come from the appVersion, we just need to set the image repository in values. By default, it would have nginx.
```
$ grep repository: harperdb/values.yaml 
  repository: nginx
```

Edit values by replacing nginx with harperdb/harperdb.
```
$ sed -i 's#repository: nginx#repository: harperdb/harperdb#g' harperdb/values.yaml

$ grep repository: harperdb/values.yaml 
  repository: harperdb/harperdb
```

### Service
HarperDB uses the port 9925 for the rest API, we would be exposing only this here, though there are other ports like 9926, 9932 for custom 
functions, clustering etc.

In our chart they are setting the service port in `.Values.service.port` and the same port is used as port the container port too, we can 
stick with that for simplicity.
```
$ grep -ir service.port harperdb
harperdb/templates/NOTES.txt:  echo http://$SERVICE_IP:{{ .Values.service.port }}
harperdb/templates/ingress.yaml:{{- $svcPort := .Values.service.port -}}
harperdb/templates/service.yaml:    - port: {{ .Values.service.port }}
harperdb/templates/deployment.yaml:              containerPort: {{ .Values.service.port }}
```

Let' change the service port in values.
```
$ grep port: harperdb/values.yaml
  port: 80

$ sed -i 's/port: 80/port: 9925/g' harperdb/values.yaml 

$ grep port: harperdb/values.yaml
  port: 9925
```

Also set the service type to LoadBlancer
```

$ sed -i 's/type: ClusterIP/type: LoadBalancer/g' harperdb/values.yaml

$ cat harperdb/values.yaml
--TRUNCATED--
service:
  type: LoadBalancer
  port: 9925
--TRUNCATED
```

### Security context
Modify the pod security context, you may check this [post](https://dev.to/aws-builders/harperdb-on-eks-1bcb) to know why we used 1000 as the 
fsGroup.
```
$ grep -i -A 2 podSecurityContext harperdb/values.yaml
podSecurityContext:
  fsGroup: 1000
```

### Resources
Similary set the cpu and memory requirements in values.
```
$ grep -A 6 resources harperdb/values.yaml
resources:
  limits:
    cpu: 500m
    memory: 1Gi
  requests:
    cpu: 100m
    memory: 128Mi
```

## Secret
The chart we created doesn't have a secret manifest, we can create it. This manifest follows standards similar to the service account 
manifest.
```
$ cat <<EOF > harperdb/templates/secret.yaml 
{{- if .Values.secret.create }}
apiVersion: v1
kind: Secret
metadata:
  name: {{ include "harperdb.secretName" . }}
  labels:
    {{- include "harperdb.labels" . | nindent 4 }}
stringData:
  {{- toYaml .Values.secret.entries | nindent 2 }}
{{- end }}
EOF
```

We can set the appropriate values for the secret manifest.
```
$ cat <<EOF >>  harperdb/values.yaml

secret:
  entries:
    HDB_ADMIN_USERNAME: admin
    HDB_ADMIN_PASSWORD: password12345
  create: true
  name: harperdb
EOF
```

We can then modify the helpers file.
```
$ cat <<EOF >> harperdb/templates/_helpers.tpl 

{{/*
Create the name of the secret to use
*/}}
{{- define "harperdb.secretName" -}}
{{- default "default" .Values.secret.name }}
{{- end }}
EOF
```

## PVC
Likewise, there is no pvc template in the chart. So we can add that.
```
$ cat <<EOF > harperdb/templates/pvc.yaml 
{{- if .Values.pvc.create }}
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {{ include "harperdb.pvcName" . }}
  labels:
    {{- include "harperdb.labels" . | nindent 4 }}
spec:
  accessModes:
  - {{ .Values.pvc.accessMode }}
  resources:
    requests:
      storage: {{ .Values.pvc.storage }}
{{- end }}
EOF
```

Set the appropriate values for pvc.
```
$ cat <<EOF >> harperdb/values.yaml                                                                                                                                                       

pvc:
  accessMode: ReadWriteOnce
  create: true
  mountPath: /opt/harperdb/hdb
  name: harperdb
  storage: 5Gi
EOF
```

We can then modify the helpers file.
```
$ cat <<EOF >> harperdb/templates/_helpers.tpl 

{{/*
Create the name of the pvc to use
*/}}
{{- define "harperdb.pvcName" -}}
{{- default "default" .Values.pvc.name }}
{{- end }}
EOF
```

## Deployment
We are going to make a few changes to the deployment manifest. So that it looks like below.
```
$ cat <<EOF > harperdb/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "harperdb.fullname" . }}
  labels:
    {{- include "harperdb.labels" . | nindent 4 }}
spec:
  {{- if not .Values.autoscaling.enabled }}
  replicas: {{ .Values.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "harperdb.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      {{- with .Values.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      labels:
        {{- include "harperdb.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "harperdb.serviceAccountName" . }}
      securityContext:
        {{- toYaml .Values.podSecurityContext | nindent 8 }}
      {{- if .Values.pvc.create }}
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: {{ include "harperdb.pvcName" . }}
      {{- end }}
      containers:
        - name: {{ .Chart.Name }}
          {{- if .Values.pvc.create }}
          volumeMounts:
          - name: data
            mountPath: {{ .Values.pvc.mountPath }}
          {{- end }}
          {{- if .Values.secret.create }}
          envFrom:
          - secretRef:
              name: {{ include "harperdb.secretName" . }}
          {{- end }}
          securityContext:
            {{- toYaml .Values.securityContext | nindent 12 }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.service.port }}
              protocol: TCP
          resources:
            {{- toYaml .Values.resources | nindent 12 }}
      {{- with .Values.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
EOF
```

In the template above, we have injected the secrets as env vars in the envFrom section of the container. And made changes related to the 
volume by defining the volume in the pod and mount it in the container.

## Lint
Our chart is kinda ready... 

Ok so now let's do the linting to see if it's proper.
```
$ helm lint harperdb
==> Linting harperdb
[INFO] Chart.yaml: icon is recommended

1 chart(s) linted, 0 chart(s) failed
```

Seems good.

We can now try generating the kubernetes manifests, it won't deploy yet. You can try `helm template harperdb` or `helm template harperdb 
--debug`, the debug flag helps debugging issues.

## Kubeconfig
Make sure you have a running kubernetes cluster. I have an EKS cluster, and I would be using the [aws](https://aws.amazon.com/cli/) cli to 
update the kubeconfig.
```
$ aws eks update-kubeconfig --name k8s-cluster-01 --region us-east-1
```

There are two nodes in my cluster.
```
$ kubectl get nodes
NAME                             STATUS   ROLES    AGE   VERSION
ip-192-168-22-158.ec2.internal   Ready    <none>   24d   v1.23.13-eks-fb459a0
ip-192-168-38-226.ec2.internal   Ready    <none>   24d   v1.23.13-eks-fb459a0
```

Create a namespace with kubectl.
```
$ kubectl create ns harperdb
```

## Dry run
As the cluster is ready we can try to do a dry run installation with helm.
```
$ helm install harperdb harperdb -n harperdb --dry-run --debug
```

If there are no errors, we can proceed to the packaging.

## Package
Our chart seems good so we can package it.
```
$ helm package harperdb
```

This should create a compressed file.
```
$ ls | grep tgz
harperdb-0.1.0.tgz
```

Here 0.1.0 refers to the chart version.
```
$ cat harperdb/Chart.yaml | grep version:
version: 0.1.0
```

## Repo
We should need a repo where we can keep this package. I am using this [repo](https://github.com/networkandcode/networkandcode.github.io) for 
this purpose. And this repo is also setup with GitHub pages and the website is accessible on this [URL](https://networkandcode.github.io). 
So you may create a github repo with [pages](https://pages.github.com) setup.

Alright I am cloning my repo.
```
git clone git@github.com:networkandcode/networkandcode.github.io.git
```

Create a directory there for helm packages.
```
$ cd networkandcode.github.io/
$ mkdir helm-packages
```

We can move the package we created earlier in to this directory.
```
$ mv ~/harperdb-0.1.0.tgz helm-packages/

$ ls helm-packages/
harperdb-0.1.0.tgz
```

We need to now create an index file.
```
$ helm repo index helm-packages/

$ ls helm-packages/
harperdb-0.1.0.tgz  index.yaml
```

The index file is populated automatically with these details.
```
$ cat helm-packages/index.yaml
apiVersion: v1
entries:
  harperdb:
  - apiVersion: v2
    appVersion: 4.0.1
    created: "2023-02-02T05:58:37.022518464Z"
    description: A Helm chart for Kubernetes
    digest: 1282e5919f2d6889f1e3dd849f27f2992d8288087502e1872ec736240dfd6ebf
    name: harperdb
    type: application
    urls:
    - harperdb-0.1.0.tgz
    version: 0.1.0
generated: "2023-02-02T05:58:37.020383374Z"
```

You can also add the artifacthub repo [file](https://github.com/artifacthub/hub/blob/master/docs/metadata/artifacthub-repo.yml
), to claim ownership, it's optional though.

Ok we can now push the changes to GitHub, note that I am directly pushing to the master branch.
```
$ git add --all
$ git commit -m 'add helm package for harperdb'

$ git push
```

## Add repository
Our repository is ready with the package, we need to add it to artifact hub. Login to artifact hub, and go to control panel and click add 
repository.

![Add repository in artifactory](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jwzw8x9l60ret2bxg8nl.png)

The repository is added, but it takes some to process. You need to wait until there is a green tick in the Last processed section.

## Search again
Once the repo is processed, we can repeat the searching process we did while starting this post.

![harperdb on artifact hub](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1mg0nct55jbye0tpmqft.png)

Well, worth to know that ChatGPT's knowledge is cut off in 2021.
![harperdb on chatgpt](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4feefqyfini6m7ynudrb.png)

Now let's do the cli way.
```
$ helm search hub harperdb --max-col-width 1000
URL                                                             CHART VERSION   APP VERSION     DESCRIPTION
https://artifacthub.io/packages/helm/networkandcode/harperdb    0.1.0           4.0.1           A Helm chart for Kubernetes
```

Wow our chart is showing up…

## Install
We can open the URL shown above and see the installation instructions.

![Installation instructions](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/sbxr87siobilam20v9k4.png)

Let's run those commands, I am going to use -n for installing it in a separate namespace.
```
$ helm repo add networkandcode https://networkandcode.github.io/helm-packages
"networkandcode" has been added to your repositories

$ helm install my-harperdb networkandcode/harperdb --version 0.1.0 -n harperdb
```

## Validate
Alright, so the release is installed, it's time to validate. First let's check the helm release status.
```
$ helm list -n harperdb
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART           APP VERSION
my-harperdb     harperdb        1               2023-02-02 07:14:59.586892384 +0000 UTC deployed        harperdb-0.1.0  4.0.1
```

Check the Kubernetes workloads.
```
$ kubectl get all -n harperdb
NAME                               READY   STATUS    RESTARTS   AGE
pod/my-harperdb-7b66d4f7c5-xtpvw   1/1     Running   0          2m7s

NAME                  TYPE           CLUSTER-IP       EXTERNAL-IP                                                               PORT(S)          
AGE
service/my-harperdb   LoadBalancer   10.100.127.117   a6e762ccc1e2d482a8528a7760544761-2140283724.us-east-1.elb.amazonaws.com   
9925:30478/TCP   2m9s

NAME                          READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/my-harperdb   1/1     1            1           2m8s

NAME                                     DESIRED   CURRENT   READY   AGE
replicaset.apps/my-harperdb-7b66d4f7c5   1         1         1       2m9s
```

## API
We can test schema creation with an API call.
```
$ HDB_API_ENDPOINT_HOSTNAME=$(kubectl get svc my-harperdb -n harperdb -o jsonpath={.status.loadBalancer.ingress[0].hostname})

$ curl --location --request POST http://${HDB_API_ENDPOINT_HOSTNAME}:9925 --header 'Content-Type: application/json' --header 'Authorization: 
Basic YWRtaW46cGFzc3dvcmQxMjM0NQ==' --data-raw '{
    "operation": "create_schema",
    "schema": "my-schema"
}'
{"message":"schema 'my-schema' successfully created"}
```
Note that I have parsed the hostname as it gives a hostname for the external IP in EKS. Well, so the API call was successful. Nice, we were 
able to accomplish the goal !!!

## Clean up
I am going to just clean up the helm and Kubernetes objects.
```
$ helm uninstall my-harperdb -n harperdb
release "my-harperdb" uninstalled

$ kubectl delete ns harperdb
namespace "harperdb" deleted
```

## Summary
So we have seen some constructs of helm, and understood how we can make a chart for harperdb, push it to artifact hub and subsequently use 
it to install a harperdb release. Note that you can customise the chart with more options such as adding readme, enabling tests, claiming 
ownership for the chart, adding more harperdb specific variables w.r.t clustering, custom functions etc. 

Thank you for reading!!!
