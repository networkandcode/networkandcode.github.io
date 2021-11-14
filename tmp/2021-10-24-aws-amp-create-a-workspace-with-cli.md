---
#categories: aws amp
#title: aws amp > create a workspace with cli
---

AWS AMP is a managed prometheus compatible monitoring service. In this post we shall see how to set it up with the aws cli. Please ensure you have installed the [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install), and you have added the credentials for it.

## AWS Configuration

Set the default AWS region, so that we don't have to explicitly call the regiom while issuing certain aws commands. I'm choosing us-west-2.
```
$ aws configure set region us-west-2
```

Verify, you can see the following.
```
$ cat ~/.aws/config 
[default]
region = us-west-2

$ cat ~/.aws/credentials 
[default]
aws_access_key_id=<some_id>
aws_secret_access_key=<some_key>
```

## Cluster OIDC

Let's launch an EKS cluster with the name my-cluster, using [eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html).
```
$ eksctl create cluster  --name my-cluster --with-oidc
```

So while creating the cluster, oidc is also enabled in it, as we would need the OIDC provider URL and ARN while creating service role.

If you already have a running EKS cluster, then you just need to issue the following command to enable OIDC.
```
$ eksctl utils associate-iam-oidc-provider --cluster <cluster-name> --approve
```

The new cluster should appear in the list of clusters.
```
$ aws eks list-clusters
{
    "clusters": [
        "my-cluster",
        "ridiculous-painting-1636073606"
    ]
}
```
I have 2 running clusters as seen above. What we created now is "my-cluster".

Get the OIDC provider URL of the kubernetes cluster as we need it while creating the role. We can either use jq, as the output is in JSON format, or we can use the query flag.
```
$ aws eks describe-cluster --name my-cluster | jq -r '.cluster.identity.oidc.issuer'
https://oidc.eks.us-west-2.amazonaws.com/id/<oidc-id>

$ aws eks describe-cluster --name my-cluster --query cluster.identity.oidc.issuer --output text
https://oidc.eks.us-west-2.amazonaws.com/id/<oidc-id>
```

We can remove https from the URL above and save it in a variable, as we would need it while creating IAM policy.
```
$ aws eks describe-cluster --name my-cluster --query cluster.identity.oidc.issuer --output text | sed -e 's~https://~~g'
oidc.eks.us-west-2.amazonaws.com/id/<oidc-id>

$ export OIDC_PROVIDER=$(aws eks describe-cluster --name my-cluster --query cluster.identity.oidc.issuer --output text | sed -e 's~https://~~g')

$ echo $OIDC_PROVIDER
oidc.eks.us-west-2.amazonaws.com/id/<oidc-id>
```

Get the ARN of the OIDC provider, and save it in a variable.
```
$ export OIDC_ARN=$(aws iam list-open-id-connect-providers | jq '.OpenIDConnectProviderList[] | select(.Arn | contains(env.OIDC_PROVIDER)) | .Arn')

$ echo $OIDC_ARN
"arn:aws:iam::<account-id>:oidc-provider/oidc.eks.us-west-2.amazonaws.com/id/<oidc-id>"
```

## Kubeconfig
Update kubeconfig appropriately so as to access the cluster.
```
$ aws eks update-kubeconfig --name my-cluster 
Added new context arn:aws:eks:us-west-2:<account-id>:cluster/my-cluster to /home/nc/.kube/config
```

We should be in the correct context now in [kubectl](https://kubernetes.io/docs/reference/kubectl/).
```
$ kubectl config current-context
arn:aws:eks:us-west-2:<account-id>:cluster/my-cluster
```

The status of kubernetes nodes should be ready.
```
$ kubectl get no
NAME                                           STATUS   ROLES    AGE   VERSION
ip-192-168-20-82.us-west-2.compute.internal    Ready    <none>   17m   v1.20.10-eks-3bcdcd
ip-192-168-86-161.us-west-2.compute.internal   Ready    <none>   17m   v1.20.10-eks-3bcdcd
```

## Workspace
Let's create an AMP workspace, with alias my-workspace.
```
$ aws amp create-workspace --alias my-workspace
{
    "arn": "arn:aws:aps:us-west-2:<account-id>:workspace/<ws-id>",
    "status": {
        "statusCode": "CREATING"
    },
    "tags": {},
    "workspaceId": "<ws-id>"
}
```

We can find the workspace id from the alias. Note that its possible to have the same alias for more than one workspace. So, make sure you get the correct workspace id :). Note that it's also possible to get the workspace id while creating the workspace, using the query flag. 
```
$ AMP_WS_ID=$(aws amp list-workspaces | jq -r '.workspaces[] | select(.alias | contains("my-workspace") ) | .workspaceId')

$ echo $AMP_WS_ID
ws-2f36580b-6c55-49ce-ab78-d42bf9ac56b7
```

Let's verify if the workspace is active.
```
$ aws amp describe-workspace --workspace-id $AMP_WS_ID --query workspace.status.statusCode
"ACTIVE"
```

And also capture the ARN.
```
$ export AMP_WS_ARN=$(aws amp list-workspaces | jq -r '.workspaces[] | select(.alias | contains("my-workspace") ) | .arn')

$ echo $AMP_WS_ARN
arn:aws:aps:us-west-2:<account-id>:workspace/<ws-id>
```

## AMP write endpoint
We can now find the prometheus endpoint from the workspace id, though its possible to makeup the endpoint URL from the workspace id, as there is a predefined format for the endpoint, its better to get it from the cli. This time I am using [jq](https://stedolan.github.io/jq/download/) to parse the output, instead of the query flag.
```
$ AMP_URL=$(aws amp describe-workspace --workspace-id $AMP_WS_ID | jq -r '.workspace.prometheusEndpoint')
$ echo $AMP_URL
https://aps-workspaces.us-west-2.amazonaws.com/workspaces/<ws-id>/
```

This is the prometheus endpoint, from which we can form the remote write endpoint. I couldn't find a way to directly to get the remote write endpoint, hence had to append the api path below. You can see the write endpoint in the AWS Web GUI console though.
```
$ export AMP_WRITE_URL=${AMP_URL}api/v1/remote_write
$ echo $AMP_WRITE_URL
https://aps-workspaces.us-west-2.amazonaws.com/workspaces/<ws-id>/api/v1/remote_write
```

## IAM Role
We need to create a service account role, that lets the prometheus server container interact with AWS AMP using that role.

Write the trust policy for the role that we are about to create.
```
$ cat /tmp/trust-policy.json 
{
 "Version": "2012-10-17",
 "Statement": [
 {
 "Effect": "Allow",
 "Principal": {
 "Federated": ${OIDC_ARN}
 },
 "Action": "sts:AssumeRoleWithWebIdentity",
 "Condition": {
 "StringEquals": {
 "${OIDC_PROVIDER}:sub": "system:serviceaccount:prometheus:amp-sa"
 }
 }
 }
 ]
}
```
In this file we have mentioned prometheus as the namespace, and amp-sa as the service account.

There are two variables OIDC_ARN and OIDC_PROVIDER which we know already, we just need to substitute, and save it as different variable.
```
$ TRUST_POLICY=$(cat /tmp/trust-policy.json | envsubst)

```

The actual trust policy after substitution can now be used to create our role.
```
$ aws iam create-role  --role-name my-cluster-amp-role --assume-role-policy-document "${TRUST_POLICY}"

```

The role is now created with a trust policy.

Save the Role ARN, as we need it for the Helm values file.
```
$ export ROLE_ARN=$(aws iam list-roles | jq '.Roles[] | select(.RoleName=="my-cluster-amp-role") | .Arn')

$ echo $ROLE_ARN
"arn:aws:iam::<account-id>:role/my-cluster-amp-role"
```

## IAM Policy
Let's create an IAM policy, that would have list of permissions to allow interaction with the AMP. Let's write the contents of our policy in a file.
```
$ cat /tmp/iam-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "aps:QueryMetrics",
        "aps:GetSeries",
        "aps:GetLabels",
        "aps:GetMetricMetadata"
      ],
      "Resource": "${AMP_WS_ARN}"
    }
  ]
}
```

And then create the policy with this file after env substitution.
```
$ IAM_POLICY=$(cat /tmp/iam-policy.json | envsubst)

$ aws iam create-policy --policy-name my-cluster-amp-policy --policy-document "${IAM_POLICY}"
```

## Attach Role with Policy
We have created the role and policy, which could be mapped now.

Get the ARN of the policy and assign it to a variable.
```
$ POLICY_ARN=$(aws iam list-policies | jq '.Policies[] | select(.PolicyName=="my-cluster-amp-policy")' | jq -r '.Arn')
aws iam attach-role-policy --role-name my-cluster-amp-role --policy-arn $POLICY_ARN
$ echo $POLICY_ARN
arn:aws:iam::<account-id>:policy/my-cluster-amp-policy
```

Note that I have used -r above for [raw text](https://stackoverflow.com/questions/44656515/how-to-remove-double-quotes-in-jq-output-for-parsing-json-files-in-bash), so that it doesn't have quotes in the output.

Attach this policy to the role.
```
$ aws iam attach-role-policy --role-name my-cluster-amp-role --policy-arn $POLICY_ARN
```

The IAM stuff can be created using the script given at [AMP guide](https://docs.aws.amazon.com/prometheus/latest/userguide/user-guide.pdf.pdf), however I thought we could break down those steps to better understand the flow.

## Helm

We know the AMP write endpoint to which we can ingest metrics from the prometheus server in our Kubernetes cluster. Hence, we have to install prometheus in our cluster, and I am going use Helm for that purpose.

Install helm.
```
$ curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
$ chmod 700 get_helm.sh 
$ ./get_helm.sh 
$ rm get_helm.sh 

$ helm version
version.BuildInfo{Version:"v3.7.1", GitCommit:"1d11fcb5d3f3bf00dbe6fe31b8412839a96b3dc4", GitTreeState:"clean", GoVersion:"go1.16.9"
```

I searched for a publicly available prometheus helm chart now by visiting [artifact hub](https://artifacthub.io/packages/helm/prometheus-community/prometheus), and followed the instructions there.
```
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo update
```

So we have added the helm repo for prometheus. 
```
$ helm repo list
NAME                    URL                                               
prometheus-community    https://prometheus-community.github.io/helm-charts

```

If we search for prometheus charts in the repo we added, it should give some results.
```
$ helm search repo prometheus
```

There should be chart by the name ```prometheus-community/prometheus```. We shall be using it to install prometheus.

## Prometheus

Let's create a separate namespace for prometheus.
```
$ kubectl create ns prometheus
namespace/prometheus created
```

We would be deploying a helm release with the following values.
```
$ cat /tmp/values.yaml 
server:
 remoteWrite:
 - url: ${AMP_WRITE_URL}
 sigv4:
 region: us-west-2
 queue_config:
 max_samples_per_send: 1000
 max_shards: 200
 capacity: 2500
serviceAccounts:
  server:
    name: amp-sa
    annotations:
      eks.amazonaws.com/role-arn: ${ROLE_ARN}
```

There are two variables in the file above, we know what those are, and hence we can substitute. We are at the final installation step of prometheus, thats ready to send data to Amazon Managed Prometheus Workspace.
```
$ cat /tmp/values.yaml | envsubst | helm install prometheus prometheus-community/prometheus -n prometheus -f -
```

The release is deployed as shown below.
```
$ helm list -n prometheus
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
prometheus      prometheus      1               2021-11-05 09:09:54.216063371 +0530 IST deployed        prometheus-14.11.0      2.26.0
```

Let's check the status of pods installed as part of the release.
```
$ kubectl get po -n prometheus
NAME                                             READY   STATUS    RESTARTS   AGE
prometheus-alertmanager-8784c78d9-m9nf2          2/2     Running   0          47s
prometheus-kube-state-metrics-569d7854c4-w5p9q   1/1     Running   0          47s
prometheus-node-exporter-48cpx                   1/1     Running   0          47s
prometheus-node-exporter-kv694                   1/1     Running   0          47s
prometheus-pushgateway-5c79b789d9-8qfd7          1/1     Running   0          47s
prometheus-server-c854cddf-q7hfg                 2/2     Running   0          47s
```

For more information on the values, you may refer to the prometheus page at [artifact hub](https://artifacthub.io/packages/helm/prometheus-community/prometheus) and the [kube-state-metrics chart repo](https://github.com/helm/charts/blob/master/stable/kube-state-metrics/templates/deployment.yaml). The prometheus chart contains the kube-state-metrics sub chart.

We can now upgrade our helm release with these overridden values for tolerations.
```
$ helm upgrade prometheus prometheus-community/prometheus -n prometheus -f /tmp/values.yaml 
```


Note that kube state metrics is an agent that listens to the kubernetes API server and generates relevant metrics about the state of the kubernetes objects. These metrics could then consumed by the prometheus server.

And their associated services are here.
```
$ kubectl get svc | grep prometheus
prometheus-alertmanager         ClusterIP   10.96.7.128     <none>        80/TCP     2m26s
prometheus-kube-state-metrics   ClusterIP   10.96.81.227    <none>        8080/TCP   2m26s
prometheus-node-exporter        ClusterIP   None            <none>        9100/TCP   2m27s
prometheus-pushgateway          ClusterIP   10.96.251.246   <none>        9091/TCP   2m27s
prometheus-server               ClusterIP   10.96.55.40     <none>        80/TCP     2m27s
```

Prometheus is now ready, and its time to send data from it to AMP using the remote_write configuration. Let's inspect the configurable values of the helm chart.
```
$ helm show values prometheus-community/prometheus
```

The content should show that there is a configurable array for the remote write option, under the server section, which would be .Values.server.remoWrite.
```
$ helm show values prometheus-community/prometheus | grep -i remote
  ## https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_write
  remoteWrite: []
  ## https://prometheus.io/docs/prometheus/latest/configuration/configuration/#remote_read
  remoteRead: []
$ 
```

# Values.yaml parsing
We could also use [yq](https://kislyuk.github.io/yq/) to parse yaml for which we need to install it using [pip](https://pypi.org/project/pip/).
```
$ pip install yq
```

Let's see what the base keys are for the entire values.yaml.
```
$ helm show values prometheus-community/prometheus | yq 'keys'
[
  "alertRelabelConfigs",
  "alertmanager",
  "alertmanagerFiles",
  "configmapReload",
  "extraScrapeConfigs",
  "forceNamespace",
  "imagePullSecrets",
  "kubeStateMetrics",
  "networkPolicy",
  "nodeExporter",
  "podSecurityPolicy",
  "pushgateway",
  "rbac",
  "server",
  "serverFiles",
  "serviceAccounts"
]
```

We are interested in the prometheus server configuration. So, let's find the sub keys in the server section, and subsequently filter for the string 'remote'.
```
$ helm show values prometheus-community/prometheus | yq '.server' | yq 'keys' | grep remote
  "remoteRead",
  "remoteWrite",
```

Let's now what's configured in remoteWrite.
```
$ helm show values prometheus-community/prometheus | yq '.server.remoteWrite'
[]
```

So, remoteWrite is any array, which by default is empty.


Since we found where remoteWrite is, we can now upgrade our helm release with the remoteWrite configuration, and we should be speciying our AMP workspace's prometheus endpoint followed by the path 'api/v1/remote_write'.
```
$ helm upgrade prometheus prometheus-community/prometheus --install --set .Values.server.remoteWrite={https://aps-workspaces.us-west-2.amazonaws.com/workspaces/<ws-id>/api/v1/remote_write}
```

The helm release's revision should now be 2, as we upgraded it.
```
$ helm list
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
prometheus      default         2               2021-10-24 19:48:41.324927793 +0530 IST deployed        prometheus-14.11.0      2.26.0
```

Let's validate if our configuration is effective, by checking the configmap.
```
$ kubectl get cm | grep prometheus
prometheus-alertmanager   1      28m
prometheus-server         5      28m
```

$ helm show values prometheus-community/prometheus > /tmp/values.yaml

$ cat /tmp/values.yaml | grep remoteWrite
  remoteWrite: [ "https://aps-workspaces.us-west-2.amazonaws.com/workspaces/ws-9a2cc232-7538-4556-b1c9-5f29318e448d/api/v1/remote_write"]

$ helm upgrade prometheus prometheus-community/prometheus --install -f /tmp/values.yaml


$ kubectl get cm prometheus-server -o yaml | grep remote
    remote_write:
    - 'https://aps-workspaces.us-west-2.amazonaws.com/workspaces/ws-9a2cc232-7538-4556-b1c9-5f29318e448d/api/v1/remote_write'

Note that according to the AWS documentation, metrics ingested into an AMP workspace are stored for 150 days and then automatically deleted.


