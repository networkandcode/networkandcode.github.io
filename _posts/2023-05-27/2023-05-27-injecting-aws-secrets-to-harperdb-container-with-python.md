---
canonical_url: "https://dev.to/aws-builders/injecting-aws-secrets-to-harperdb-container-with-python-2df6"
date: "2023-05-27"
title: "Injecting AWS secrets to HarperDB container with Python"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fsource.unsplash.com%2Ffeatured%2F%3Ffiles"
tags: "aws, harperdb, kubernetes, python"
categories: "aws, harperdb, kubernetes, python"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/injecting-aws-secrets-to-harperdb-container-with-python-2df6)**

In this post we'll see how we can inject the username and password secrets stored in AWS as environmental variables to the HarperDB container in a few ways. First, we would cover some AWS Secrets manager and IAM procedures. And then we would move on to Docker and Kubernetes.

## Create secret
Login to the AWS console as a user that has enough permissions to create a secret. Access the AWS cloud shell and put your secret in JSON format in a temporary file.
```
$ cat > /tmp/.hdb_creds.json <<EOF
{
    "HDB_ADMIN_USERNAME": "admin",
    "HDB_ADMIN_PASSWORD": "password"
}
EOF
```
It's only a single secret, but has two key-value pairs.

Use this JSON file to create a secret with the aws cli.
```
$ aws secretsmanager create-secret \
    --name HdbCreds \
    --secret-string \
    file:///tmp/.hdb_creds.json
```
Note that the secret gets created in the default region where cloud shell was launched, as we have not explicity mentioned the region above, in my case it's `ap-south-1`.

As the secret is created, we could safely delete the secret file.
```
$ rm /tmp/.hdb_creds.json
```

## Setup user
Ensure the current user has permissions to do the following IAM operations.

Create user.
```
$ aws iam create-user --user-name appuser
```

Create group.
```
$ aws iam create-group --group-name appgroup
```

Add user to group.
```
$ aws iam add-user-to-group --user-name appuser --group-name appgroup
```

## Policy
Get the secret ARN and save it as environment variable.
```
$ export SECRET_ARN=`aws secretsmanager describe-secret --secret-id HdbCreds --output text --query ARN`
```

Write the policy in a json file, that allows getting the secret value from our specific secret ARN.
```
$ cat /tmp/policy.json 
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "secretsmanager:GetSecretValue"
            ],
            "Resource": [
                "$SECRET_ARN"
            ]
        }
    ]
}
```

We have used an env var `SECRET_ARN` in the file above, we can use envsusbst to replace that with the actual value. For which, we have to install gettext.
```
$ sudo yum install gettext -y
$ envsubst < /tmp/policy.json > /tmp/.policy.json
```

So, the actual policy with the secret ARN is now in `/tmp/.policy.json`. We could use that for creating the policy. We can also retrieve the policy ARN as that's required while attaching the policy to group.
```
$ POLICY_ARN=`aws iam create-policy --policy-name apppolicy --policy-document file:///tmp/.policy.json --query Policy.Arn`
```
The policy is now created, we are good to delete the hidden file.
```
$ rm /tmp/.policy.json
```

We can now attach the policy to the group.
```
$ aws iam attach-group-policy --group-name appgroup --policy-arn $POLICY_ARN
```

## Access key
So far we created a user inside a group, and gave that group permission to read the secret value. We can now create an access key and share it with the dev team who would use it in their app, for authentication.
```
$ aws iam create-access-key --user-name appuser > /tmp/.access_key.json

$ cat /tmp/.access_key.json 
{
    "AccessKey": {
        "UserName": "appuser",
        "AccessKeyId": "AKIA4IRCWQQATYRH4XV2",
        "Status": "Active",
        "SecretAccessKey": "<hidden>",
        "CreateDate": "2023-05-25T11:41:20+00:00"
    }
}
```

## Dev user
Let's say the access key created by the devops team is shared to the developer. The developer can test it with the aws cli by retreiving the secret value as follows from their system. Note that appuser doesn't have console access, so it can't access the cloud shell via console. It's meant to be used programmatically. It's possible though to use different accounts from the same machine with profiles in aws cli.

We would follow rest of  the post from the local machine, and not cloud shell.

The [aws](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) cli can be installed, if not present.
```
$ curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
$ unzip awscliv2.zip
$ sudo ./aws/install
```

The developer needs to set the configuration and credentials for aws. Create and new directory and add a `.env` file to it.
```
$ mkdir secret-injection
$ cd secret-injection/
$ cat > .env << EOF
AWS_ACCESS_KEY_ID=AKIA4IRCWQQA25E4Q7OC
AWS_DEFAULT_OUTPUT=text
AWS_DEFAULT_REGION=ap-south-1
AWS_SECRET_ACCESS_KEY=<hidden>
AWS_SECRET_NAME=HdbCreds
EOF
```

Export these to setup env vars in the system.
```
$ export `cat .env | xargs`

$ printenv | grep AWS
AWS_DEFAULT_REGION=ap-south-1
AWS_ACCESS_KEY_ID=AKIA4IRCWQQA25E4Q7OC
AWS_SECRET_ACCESS_KEY=<hidden>
AWS_SECRET_NAME=HdbCreds
AWS_DEFAULT_OUTPUT=text
```

Setting env vars is one way of adding configuration and credentials for aws. Alternatively, you can also use `aws configure` that would rather create files in the `~/.aws` directory.
```
$ aws configure
AWS Access Key ID [None]: AKIA4IRCWQQATYRH4XV2
AWS Secret Access Key [None]: <hidden>
Default region name [None]: ap-south-1
Default output format [None]: text
```

This automatically creates the `.aws` directory and two files inside it.
```
$ cat ~/.aws/config 
[default]
region = ap-south-1
output = text

$ cat ~/.aws/credentials 
[default]
aws_access_key_id = AKIA4IRCWQQATYRH4XV2
aws_secret_access_key = <hidden>
```

We can go with the `.env method` as we anyways have an extra variable for setting the secret name.

## Retreive secret
Let's try retreiving the secret from the developer machine.
```
$ aws secretsmanager get-secret-value --secret-id $AWS_SECRET_NAME --query SecretString
{
    "HDB_ADMIN_USERNAME": "admin",
    "HDB_ADMIN_PASSWORD": "password"
}
```
It's working....

## Docker / AWS CLI
Let's try our first test with Docker. We would retrieve the secrets with aws, set those as env vars on the local system and pass it to docker container as env vars.
```
$ HDB_ADMIN_USERNAME=`aws secretsmanager get-secret-value --secret-id $AWS_SECRET_NAME --query SecretString | jq -r '.HDB_ADMIN_USERNAME'`

$ HDB_ADMIN_PASSWORD=`aws secretsmanager get-secret-value --secret-id $AWS_SECRET_NAME --query SecretString | jq -r '.HDB_ADMIN_PASSWORD'`

$ docker run -d -e HDB_ADMIN_USERNAME=$HDB_ADMIN_USERNAME -e HDB_ADMIN_PASSWORD=$HDB_ADMIN_PASSWORD harperdb/harperdb
```

The HarperDB container should be running and we can check the values of env vars.
```
$ HDB_CTR_ID=`docker run -d -e HDB_ADMIN_USERNAME=$HDB_ADMIN_USERNAME -e HDB_ADMIN_PASSWORD=$HDB_ADMIN_PASSWORD harperdb/harperdb`

$ docker exec $HDB_CTR_ID printenv | grep HDB
HDB_ADMIN_USERNAME=admin
HDB_ADMIN_PASSWORD=password
```

## Python
This time we would try with some python code, samples should be availble from [AWS](https://aws.amazon.com/developer/language/python/).

Let's first run the python code locally and see if it works.
```
$ cat retrieve_secret.py 
'''
This example does some modification on the AWS sample code, visit the AWS docs for samples:
https://aws.amazon.com/developer/language/python/
'''

import json
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()

def get_secret():
    '''
    function to retrieve secret from aws secrets manager
    iterate over its keys and create files, one each for each key
    the name of the file will be the key and it's value is the file content

    pass the following env vars:
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION
    AWS_SECRET_NAME
    '''

    secret_name = os.environ['AWS_SECRET_NAME']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as client_error:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise client_error

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Your code goes here.
    secret_dict = json.loads(secret)

    for key, value in secret_dict.items():
        with open(f'envvars/{key}', 'w', encoding='utf-8') as open_file:
            print(f'writing {key}')
            open_file.write(value)

get_secret()
```

Install boto3 and python-dotenv.
```
$ pip install boto3

$ pip install python-dotenv
```

Create a directory by the name envvars.
```
$ mkdir envvars
```

Run the code.
```
$ python3 retrieve_secret.py 
writing HDB_ADMIN_USERNAME
writing HDB_ADMIN_PASSWORD
```

This should have created two files in the envvars directory.
```
$ ls envvars/
HDB_ADMIN_PASSWORD  HDB_ADMIN_USERNAME

$ cat envvars/HDB_ADMIN_USERNAME; echo
admin

$ cat envvars/HDB_ADMIN_PASSWORD; echo
password
```

## Python container
We would now test the previous scenario with a container, for which we need to containerize our code first. Let's write the dockerfile.
```
$ cat dockerfile 
FROM python
RUN pip install boto3
RUN pip install python-dotenv
WORKDIR /app
COPY retrieve_secret.py ./
CMD [ "python", "retrieve_secret.py" ]
```

We can build the image now.
```
$ docker build -t retrieve_secret .
```

Remove the contents inside envvars directory.
```
$ rm envvars/*
```

Run the container and see if it works.
```
$ docker run --env-file .env -v $PWD/envvars:/app/envvars retrieve_secret
writing HDB_ADMIN_USERNAME
writing HDB_ADMIN_PASSWORD
```

There should be files again in the envvars directory.
```
$ ls envvars/
HDB_ADMIN_PASSWORD  HDB_ADMIN_USERNAME
```

## Kubernetes
Since we have tested the creation of envvars as files with a docker container, we could use that as an init container in a Pod. The envvars files it creates could be used by the harperdb container through a shared volume.

First I am going to tag the local image, and push it to docker hub. So that I can pull that in the pod's container. I would be using my docker id here, and I am already logged in.
```
$ docker tag retrieve_secret s1405/retrieve_secret
$ docker push s1405/retrieve_secret
```

Let's create a secret object with our `.env` file.
```
$ kubectl create secret generic aws-vars --from-env-file=.env
secret/aws-vars created

$ kubectl get secret aws-vars -o jsonpath={.data} | jq
{
  "AWS_ACCESS_KEY_ID": "QUtJQTRJUkNXUVFBMjVFNFE3T0M=",
  "AWS_DEFAULT_OUTPUT": "dGV4dA==",
  "AWS_DEFAULT_REGION": "YXAtc291dGgtMQ==",
  "AWS_SECRET_ACCESS_KEY": <hidden>,
  "AWS_SECRET_NAME": "SGRiQ3JlZHM="
}
```

We can attach these as env vars in our init container.

Here is our pod manifest:
```
$ cat harperdb.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: harperdb
spec:
  initContainers:
  - name: fetch-secrets
    image: s1405/retrieve_secret
    envFrom:
    - secretRef:
        name: aws-vars
    volumeMounts:
    - name: envvars
      mountPath: /app/envvars
  containers:
  - name: harperdb
    image: harperdb/harperdb
    volumeMounts:
    - name: envvars
      mountPath: /app/envvars
  volumes:
  - name: envvars
    emptyDir: {}
```

I am on a docker desktop based kubernetes cluster, the pod manifest can be applied on it.
```
$ kubectl config current-context 
docker-desktop

$ kubectl apply -f harperdb-pod.yaml

$ kubectl get po -w
NAME       READY   STATUS     RESTARTS   AGE
harperdb   0/1     Init:0/1   0          5s
harperdb   0/1     PodInitializing   0          5s
harperdb   1/1     Running           0          8s
^C
```

The pod is running. Let's check the pod for the variables
```
$ kubectl exec -it -c harperdb harperdb -- printenv | grep HDB
HDB_ADMIN_USERNAME=HDB_ADMIN
HDB_ADMIN_PASSWORD=password
```

All good. So, we have reached the end of the post, let's finish it off with a summary.
 
## Summary
So we have seen the procedure involved in storing the HarperDB secrets in AWS, assigning the required IAM, retrieving those secrets via the aws cli and then with python locally. We then containerized our python code, tried the exerices with both docker and kubernetes. Here, we have used the built in env vars of HarperDB to setup the credentials, you may check this [link](https://www.harperdb.io/post/harperdb-authentication-with-aws-cognito) if you are looking to integrate AWS cognito with HarperDB for authentication. Thank you for reading :)
