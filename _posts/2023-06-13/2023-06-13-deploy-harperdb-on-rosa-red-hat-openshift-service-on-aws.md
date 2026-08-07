---
canonical_url: "https://dev.to/aws-builders/deploy-harperdb-on-rosa-red-hat-openshift-service-on-aws-4jge"
date: "2023-06-13"
title: "Deploy HarperDB on ROSA (Red Hat OpenShift Service on AWS)"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fsource.unsplash.com%2Ffeatured%2F%3Fcontainer"
tags: "aws, harperdb, kubernetes, openshift"
categories: "aws, harperdb, kubernetes, openshift"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/deploy-harperdb-on-rosa-red-hat-openshift-service-on-aws-4jge)**

In this post, we would be deploying HarperDB on ROSA (Red Hat OpenShift Service on AWS). Let's begin with the steps.

Before you begin, ensure you have installed and configured the AWS CLI. Instructions are [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).

## Enable ROSA

ROSA should be enabled on the AWS console as shown in the screenshot below.
![Enable ROSA](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zxw65da7dft3z9uu5l67.png)

And then, click on `Continue to Red Hat` at the bottom of the page.
![Continue to RedHat](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y66k0be98pb52yqw1cnv.png)

This should take you to a page where you can view the terms and conditions and accept, with a RedHat login.

## Download the binaries
Go to the OpenShift [downloads](https://console.redhat.com/openshift/downloads) page and download the [rosa](https://docs.openshift.com/rosa/rosa_cli/rosa-get-started-cli.html#rosa-setting-up-cli_rosa-getting-started-cli) cli.
![Download rosa cli](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/h8rl77r47a8t9wspg864.png)

Extract the contents from the archive, and remove the archive.

```bash
$ cd Downloads 
$ tar xvf rosa-macosx.tar.gz
$ rm rosa-macosx.tar.gz
```

Move the extracted binary to one of the directories in PATH. I am using /usr/local/bin.

```bash
$ sudo mv rosa /usr/local/bin/.
```

Check if it's installed properly.

```bash
$ rosa version
1.2.22
I: Your ROSA CLI is up to date.
```

Similarly, download the oc CLI.
![Download oc CLI](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/w5x7ksnkkcagfku8up4m.png)

```bash
$ cd ~/Downloads

$ tar xvf openshift-client-mac.tar.gz 
x README.md
x oc
x kubectl
```

I already have kubectl in my system, so I would only move the oc binary.

```bash
$ rm README.md 
$ rm kubectl 
$ rm openshift-client-mac.tar.gz 
$ sudo mv oc /usr/local/bin/.
```

If it's a Mac, go to Security settings and allow oc to be run.
![Allow oc cli on mac](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6wea7uhkfept2iwyle70.png)

Check the version to see if it's installed properly.
```bash
$ oc version
Client Version: 4.13.1
Kustomize Version: v4.5.7
Kubernetes Version: v1.25.2
```

## API token

Go to the URL https://console.redhat.com/openshift/token/aws and load the token.
![Load API token for rosa](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rgnweu1gwffo66es5388.png)

Copy the token from the next step, and set it as a variable. Note that you need to paste the token in the next line after the read command.
```bash
$ read -s ROSA_TOKEN
$
```

Login with this token. 
```bash
$ rosa login --token $ROSA_TOKEN
```
Note that it didn't work for me with just setting the variable ROSA_TOKEN, hence I had to login with the --token option

## Validate
Verify permissions and quota in AWS.
```bash
$ rosa verify permissions
I: Verifying permissions for non-STS clusters
I: Validating SCP policies...
I: AWS SCP policies ok

$ rosa verify quota
I: Validating AWS quota...
E: Insufficient AWS quotas
E: Service quota is insufficient for the following service quota codes:
- Service ec2 quota code L-1216C47A Running On-Demand Standard (A, C, D, H, I, M, R, T, Z) instances not valid, expected quota of at least 100, but got 64
```

The quota is insufficient, so we can increase it. Go to Service Quotas &gt; AWS services &gt; EC2 and select Running On-Demand Standard instances as shown below.
![Search for EC2 quotas](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1r20x1kwot9rk53i4oz8.png)

On the next page, change the quota to 100 and request an increase.
![Increase EC2 quota](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ii9hkq9f00y1e2pnnk43.png)

A support case should be automatically created, and it might take up to 30 minutes for the new quota to reflect as per the message below.
![Confirmation message for EC2 quota increase](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/10t2v1npw9zszlzw8kdl.png)

Once the quota is granted, `rosa verify quota` should be successful.
```bash
$ rosa verify quota
I: Validating AWS quota...
I: AWS quota ok. If cluster installation fails, validate actual AWS resource usage against https://docs.openshift.com/rosa/rosa_getting_started/rosa-required-aws-service-quotas.html
```

## Provision the cluster
Do an init first, for the validation.
```bash
$ rosa create cluster --cluster-name='hdb-rosa-clstr'
E: Failed to create cluster: The maximum number of VPCs has been reached
```

I first got an error that the maximum number of VPCs has been reached, there were 5, so I deleted the unwanted VPCs, and ran the command again.
```bash
$ rosa create cluster --cluster-name='hdb-rosa-clstr'
Details Page:               https://console.redhat.com/openshift/details/s/2R2oUbagDXdMV1pWbSftXIzclea
```

Also, note that the cluster name must not contain more than 15 characters.

Fine, our cluster is ready. We can add the admin user.
```
$ rosa create admin -c hdb-rosa-clstr
```

Copy and run the oc login command from the output.
```
$ oc login https://api.hdb-rosa-clstr.0h87.p1.openshiftapps.com:6443 --username cluster-admin --password Uzrkx-IJE3a-xky3s-SodfM
Login successful.

You have access to 103 projects, the list has been suppressed. You can list all projects with 'oc projects'

Using project "default".
```

You can see the list of nodes with oc.
```
$ oc get nodes
NAME                                          STATUS   ROLES                  AGE     VERSION
ip-10-0-135-59.ap-south-1.compute.internal    Ready    worker                 7h22m   v1.26.3+b404935
ip-10-0-143-8.ap-south-1.compute.internal     Ready    infra,worker           7h9m    v1.26.3+b404935
ip-10-0-164-209.ap-south-1.compute.internal   Ready    infra,worker           7h9m    v1.26.3+b404935
ip-10-0-213-140.ap-south-1.compute.internal   Ready    worker                 7h25m   v1.26.3+b404935
ip-10-0-221-178.ap-south-1.compute.internal   Ready    control-plane,master   7h32m   v1.26.3+b404935
ip-10-0-228-159.ap-south-1.compute.internal   Ready    control-plane,master   7h32m   v1.26.3+b404935
ip-10-0-251-121.ap-south-1.compute.internal   Ready    control-plane,master   7h32m   v1.26.3+b404935
```

You can check this on the EC2 console too, where it gives the names.
![List of EC2 rosa instances](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/79aoxelqm0np561jfdgj.png)


## Deploy HarperDB
We will first add a new project.
```bash
$ oc new-project harperdb
```

We can use kubernetes native manifests to deploy with oc. For which we can clone the manifests repo.
```bash
$ git clone https://github.com/HarperDB-Add-Ons/harperdb-deployments.git
```

In OpenShift, by default the user set on Dockerfile, is not considered, it would run with a different project default userid which is somewhat bigger like 1000610000 . In the case of HarperDB image it uses the notroot user harperdb with userid 1000 in docker.
```bash
$ docker run -it harperdb/harperdb bash
harperdb@6b19c2abbebc:~$ id
uid=1000(harperdb) gid=1000(harperdb) groups=1000(harperdb)
```

So we can let the container in OpenShift also use the same uid as set in Dockerfile.
```bash
$ oc adm policy add-scc-to-group anyuid system:authenticated
```

We can now apply the Kubernetes manifests with oc.
```bash
$ cd harperdb-deployments/kubernetes-manifests
$ oc apply -f .
```

The pod should be running.
```bash

$ oc get po
NAME                        READY   STATUS    RESTARTS   AGE
harperdb-5597447d8b-fqzg7   1/1     Running   0          2m58s
```

Retrieve the HarperDB API endpoint.
```bash
$ HDB_SVC_HOSTNAME=$(oc get svc harperdb -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

$ HDB_SVC_PORT=$(oc get svc harperdb -o jsonpath='{.spec.ports[0].port}')

$ HDB_API_ENDPOINT=$HDB_SVC_HOSTNAME:$HDB_SVC_PORT
```

We can now test schema creation with curl.
```bash
$ curl --location --request POST $HDB_API_ENDPOINT \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM0NQ==' \
--data-raw '{
    "operation": "create_schema",
    "schema": "hdb_rosa_schema" 
}'

{"message":"schema 'hdb_rosa_schema' successfully created"}
```

## Persistence
Let's test persistence, we shall delete the pod and when the new pod comes, we'd see if the schema we created exists.
```bash
$ oc delete po --all
pod "harperdb-5597447d8b-fqzg7" deleted

$ oc get po
NAME                        READY   STATUS    RESTARTS   AGE
harperdb-5597447d8b-cc4jt   1/1     Running   0          54s
```

A new pod is now running, we can check the list of schemas with curl.
```bash
$ curl --location $HDB_API_ENDPOINT \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM0NQ==' \
--data '{
    "operation": "describe_all"
}'
{"hdb_rosa_schema":{}}
```

## OpenShift Image
So far we tested HarperDB deployment on OpenShift with the [harperdb/harperdb](https://hub.docker.com/r/harperdb/harperdb) image on the docker hub. We can now try with the [harperdb/harperdb-openshift](https://hub.docker.com/r/harperdb/harperdb-openshift) image. This [link](https://catalog.redhat.com/software/containers/harperdb/harperdb-openshift/6467f6a2cb06b902b80aac37?container-tabs=gti) also has details about the image.

Just change the image section of the deployment manifest and apply it again with oc.
```bash
$ cat deploy.yaml | grep image:     
        image: harperdb/harperdb-openshift:4.1.0

$ oc apply -f .
```

The new harperdb pod with openshift image should be running.
```bash
$ oc get pods   
NAME                        READY   STATUS    RESTARTS      AGE
harperdb-757579fb58-l46sc   1/1     Running   2 (39s ago)   88s
```

This image has a slightly different user than the previous image.
```bash
$ oc rsh harperdb-757579fb58-l46sc     
sh-5.1$ id
uid=1001(default) gid=0(root) groups=0(root),1000
```

The schema should still be existing here.
```bash
$ curl --location $HDB_API_ENDPOINT \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM0NQ==' \
--data '{
    "operation": "describe_all"
}'
{"hdb_rosa_schema":{}}
```

We can add a table in this schema.
```bash
$ curl --location $HDB_API_ENDPOINT \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM0NQ==' \
--data '{ "operation": "create_table", "schema": "hdb_rosa_schema", "table": "hdb_schema_table", "hash_attribute": "id" }'
{"message":"table 'hdb_rosa_schema.hdb_schema_table' successfully created."}
```

Delete the pod and test persistence, this time describe all.
```bash
$ curl --location $HDB_API_ENDPOINT \
--header 'Content-Type: application/json' \
--header 'Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM0NQ==' \
--data '{
    "operation": "describe_all"
}'
{"hdb_rosa_schema":{"hdb_schema_table":{"__createdtime__":1686484996114.1133,"__updatedtime__":1686484996114.1133,"hash_attribute":"id","id":"a71a415d-199b-41ce-86a8-3c336850ea67","name":"hdb_schema_table","residence":null,"schema":"hdb_rosa_schema","attributes":[{"attribute":"__createdtime__"},{"attribute":"__updatedtime__"},{"attribute":"id"}],"clustering_stream_name":"1e79fdbec80f4ab386755f827fb8863b","record_count":0}}}
```

## Clean up
Delete the cluster with rosa cli.
```bash
$ rosa delete cluster -c hdb-rosa-clstr
? Are you sure you want to delete cluster hdb-rosa-clstr? Yes
I: Cluster 'hdb-rosa-clstr' will start uninstalling now
I: To watch your cluster uninstallation logs, run 'rosa logs uninstall -c hdb-rosa-clstr --watch'
```

## Summary
So we saw some information about the rosa, oc CLIs, setting them up and getting the prerequisites ready before launching the cluster. We then launched the cluster and deployed HarperDB on it with both the usual HarperDB image and the OpenShift specific one and tested the endpoints. Thank you for reading !!!
