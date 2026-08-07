---
canonical_url: "https://dev.to/aws-builders/aws-albingress-access-logs-on-grafana-25em"
date: "2024-10-01"
title: "AWS ALB(Ingress) access logs on Grafana"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F235bq6gkozgamld01qhn.jpeg"
tags: "aws, kubernetes, lambda, monitoring"
categories: "aws, kubernetes, lambda, monitoring"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/aws-albingress-access-logs-on-grafana-25em)**

Hi :wave:, we shall explore the following use case in this post: Let's say you have an EKS cluster, and you have deployed an application there and exposed it via the AWS ALB controller as ingress(instead of other options like nginx ingress, istio virtual service etc.). We'll see how to check the access logs for this scenario, by forwarding the access logs from the application load balancer to a bucket on S3. And then use an event trigger when new logs are added to S3, to invoke a Lambda function that would write those logs to a Cloud watch log group and stream. We could then use Cloud watch as a datasource on Grafana to visualize/monitor the logs.

So the setup is going to look like this:
![Blog diagram](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/cad2ma436joy2vk5ph07.png)
Note that though the arrow on the diagram is one sided, it's only referring to who initiates the traffic(request) first, in most cases there is going to be some response back.

## EKS cluster
We need to first create a cluster and associate oidc provider with it.
```
eksctl create cluster --name ingress-logs-demo --zones=us-east-1a,us-east-1b

eksctl utils associate-iam-oidc-provider --region=us-east-1 --cluster=ingress-logs-demo --approve
```

## Ingress
First create a service account with the built in load balancer controller role.
```
eksctl create iamserviceaccount \
  --cluster=ingress-logs-demo \
  --namespace=kube-system \
  --name=aws-load-balancer-controller \
  --role-name AmazonEKSLoadBalancerControllerRole \
  --attach-policy-arn=arn:aws:iam::$AWS_ACCOUNT_ID:policy/AWSLoadBalancerControllerIAMPolicy \
  --approve
```

Replace $AWS_ACCOUNT_ID with your account id.

We can now install the [AWS Loadbalancer Controller](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html), and map it with the service account we just created.
```
helm repo add eks https://aws.github.io/eks-charts

helm install aws-load-balancer-controller eks/aws-load-balancer-controller \ 
-n kube-system \ 
--set clusterName=$CLUSTER \ 
--set serviceAccount.create=false \ 
--set serviceAccount.name=aws-load-balancer-controller
```

## Demo app
We can install a [demo app - 2048 game](https://docs.aws.amazon.com/eks/latest/userguide/lbc-helm.html) that comes with ingress as well.
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v2.7.2/docs/examples/2048/2048_full.yaml
```

This should have created an ingress resource for us.
```
kubectl get ing -n game-2048
NAME           CLASS   HOSTS   ADDRESS                                                                  PORTS   AGE
ingress-2048   alb     *       k8s-game2048-ingress2-cfcea01af4-806164108.us-east-1.elb.amazonaws.com   80      3d3h
```

We could access the URL with the URL above(it would change in your case).
![2048 game on browser](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6nhmwrks4fl3sbhenomw.png)

## Access logs
Let's say we want to monitor our app, like how many requests are coming in, how many are errors, what's the response time etc. In that case we can catch the access logs that are going to our app. For this we need to go the application loadbalancer that was created when we installed the aws load balancer controller via helm. And update it to forward the acces logs to S3. Which means we first need to create the S3 bucket.

## S3
I have created an S3 bucket with the name `ingress-logs-demo` in the us-east-2 region with the following policy:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::127311923021:root"
            },
            "Action": "s3:PutObject",
            "Resource": "arn:aws:s3:::ingress-logs-demo/AWSLogs/<AWS_ACCOUNT_ID>/*"
        }
    ]
}
```
Note that `127311923021` refers to the AWS account for loadbalancers in the us-east-2 region. Check this [link](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/enable-access-logging.html) for more info. Also, replace `<AWS_ACCOUNT_ID>` with your account id. The policy above means any loadblancer created in the us-east-2 region should be able to put objects in this bucket in the defined path.

We can now modify the application loadbalancer to forward logs to S3.
![Send access logs to S3](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/py03zedkctde9so8i0k5.png)

If we start using the app ui now via browser and do a few hits, we should be able to see the access logs for those on S3 in compressed format.
![Access logs on S3](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ncd1fe2fdcn8ntl68a4h.png)

## Cloudwatch Logs
We can create a log watch group(`/aws/lambda/ingress-logs-demo`) and stream(`access-logs`) where we can forward the access logs from S3. Note that I am going to use the same log group for both the access logs(alb to s3 to cloud watch) and for any logs coming from the lambda function itself. That is why I have named the logwatch group with that format, as any logs from a function with name (ingress-logs-demo) would be stored in (/aws/lambda/ingress-logs-demo)

## Lambda
We should need a way to retreive these logs and forward those to Cloudwatch, for which I would be using a Lambda function in Python with the same name `ingress-logs-demo`(for simplicity) with the following code.
```
import boto3
import gzip
import io
from datetime import datetime

s3_client = boto3.client('s3')
logs_client = boto3.client('logs')

log_group_name = '/aws/lambda/ingress-logs-demo'
log_stream_name = 'access-logs'

def lambda_handler(event, context):
    # Get S3 bucket and log file details from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Download the log file from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)

    # Read the gzipped file
    with gzip.GzipFile(fileobj=io.BytesIO(response['Body'].read())) as file:
        logs = file.read().decode('utf-8').splitlines()

    # Send each log line as an event to CloudWatch
    log_events = []
    for line in logs:
        timestamp = int(datetime.now().timestamp() * 1000)
        
      
        log_events.append({
            'timestamp': timestamp,
            'message': line
        })

    if log_events:
        logs_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )

    return {
        'statusCode': 200,
        'body': f'Successfully processed {len(log_events)} log events from {key}'
    }
```

Note the we are passing the logs as is but we could use some logic in our code, to parse the content and restructure it as desired. Please check this [link](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html#log-processing-tools) for the log format.

Also we need a trigger to invoke this function when any objects are added to S3.
![Lambda trigger for S3](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/59pxllxi506zow59sp7s.png)

## Role
We need an IAM role that lets the lambda function read from S3 and write to Cloudwatch Logs. We can create a new one with name `ingress-logs-demo`, trusted entity type as `AWS service`, Service or use case  as `Lambda` and in the permission policies, select `AWSLambdaBasicExecutionRole` and `AmazonS3ReadOnlyAccess`.

## All set
All set now, we can now hit the 2048 game url on browser a couple of times, and  try playing the game. This should run our workflow and store logs in cloud watch.
![Access logs on cloud watch](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/es4uwgbkt5vipnn4d7vg.png)

## Grafana
We can now go to Grafana, add cloudwatch as a [datasource](AWS Community Builders 
Logging demo with OTEL Collector, CloudWatch and Grafana) and play with the data and do some visualization, display the logs etc.
Let's try a couple of exercises with panels.

Just filter for logs that has "200" typically meaning we wan't to see  logs that have response code 200.
![Logs on Grafana](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xi07itlgnygtwphlek9f.png)

Let's check 404 this time. And create a stat panel with it.
![Stat panel for 404](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dyfl0siacvvjj3erz6j6.png)

I have used this query:
```
fields @timestamp, @message
| filter @logStream = "access-logs"
| filter @message like /"404"/
| sort @timestamp desc
```
and the calculation was set to count for the field `@message`

Alright, so that's end the post, we were finally able to get our access logs on cloudwatch and see those on Grafana. This should help us monitoring any urls thats accessed through the ingress.

## Cleanup
Checklist:
- Delete the function
- Delete the IAM role
- Empty the S3 bucket and delete it
- Delete the cloudwatch log group
- Delete the load balancer controller and remove the helm repo
```
helm uninstall aws-load-balancer-controller -n kube-system
helm repo remove eks
```
- Delete the eks cluster: `eksctl delete cluster --name ingress-logs-demo`

Thank you for reading :)
