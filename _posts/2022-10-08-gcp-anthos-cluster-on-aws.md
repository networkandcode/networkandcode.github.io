---
canonical_url: https://dev.to/aws-builders/gcp-anthos-cluster-on-aws-19p8
categories: anthos, aws, gcp, kubernetes
date: 2022-10-08
tags: anthos, aws, gcp, kubernetes
title: GCP Anthos Cluster on AWS
---

This post first appeared on [dev.to](https://dev.to/aws-builders/gcp-anthos-cluster-on-aws-19p8)


Anthos is a software offering from Google, using which we can build kubernetes clusters on nodes both on and off cloud. In this post, we 
would launch an EC2 instance in AWS and build a single node kubernetes cluster on it with Anthos.

Let's get started. 

## AWS cloud shell
Login to the AWS console, and access the cloud shell from the top bar. You should see a prompt like below.
```
[cloudshell-user@ip-10-0-89-211 ~]$ 
```

## EC2
Create an EC2 instance with other relevant components with these commands. Please refer to this 
[post](https://dev.to/aws-builders/aws-ec2-launch-instances-the-hard-way-with-cli-2ga3) for explanation on what each of these commands does.
```
$ mkdir ~/.aws

$ cat ~/.aws/config <<EOF
[default]
region=ap-south-1
EOF

$ export CIDR_BLOCK="10.10.10.0/28"
$ aws ec2 create-vpc --cidr-block $CIDR_BLOCK

$ export ANTHOS_VPC_ID=$(aws ec2 describe-vpcs | jq -r '.Vpcs[] | select(.CidrBlock == env.CIDR_BLOCK) | .VpcId')

$ aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=anthos-igw}]'

$ export ANTHOS_IGW_ID=$(aws ec2 describe-internet-gateways --filters Name=tag:Name,Values=anthos-igw --query 
"InternetGateways[*].InternetGatewayId" --output text)

$ aws ec2 attach-internet-gateway --internet-gateway-id $ANTHOS_IGW_ID --vpc-id $ANTHOS_VPC_ID

$ export ANTHOS_RTB_ID=$(aws ec2 describe-route-tables | jq -r '.RouteTables[] | select(.VpcId == env.ANTHOS_VPC_ID) | .RouteTableId')

$ aws ec2 create-route --route-table-id $ANTHOS_RTB_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $ANTHOS_IGW_ID

$ aws ec2 create-subnet --cidr-block $CIDR_BLOCK --vpc-id $ANTHOS_VPC_ID

$ export ANTHOS_SUBNET_ID=$(aws ec2 describe-subnets | jq -r '.Subnets[] | select(.CidrBlock == env.CIDR_BLOCK) | .SubnetId')

$ export ANTHOS_AVAILABILITY_ZONE=$(aws ec2 describe-subnets | jq -r '.Subnets[] | select(.CidrBlock == env.CIDR_BLOCK) | 
.AvailabilityZone')

$ aws ec2 create-security-group --group-name anthos-sg --description "anthos security group" --vpc-id $ANTHOS_VPC_ID

$ export ANTHOS_SG_ID=$(aws ec2 describe-security-groups | jq -r '.SecurityGroups[] | select(.GroupName == "anthos-sg") | .GroupId')

$ aws ec2 describe-instance-types | jq '.InstanceTypes[] | select(.MemoryInfo.SizeInMiB == 7680) | (.InstanceType, .VCpuInfo.DefaultVCpus)'
"c4.xlarge"
4

$ aws ec2 describe-instance-types | jq '.InstanceTypes[] | select(.MemoryInfo.SizeInMiB == 8192) | select (.VCpuInfo.DefaultVCpus == 2) | 
.InstanceType' | sort
"m4.large"
"m5ad.large"
"m5a.large"
"m5d.large"
"m5.large"
"m6a.large"
"m6gd.large"
"m6g.large"
"m6i.large"
"t2.large"
"t3a.large"
"t3.large"
"t4g.large"

$ aws ec2 describe-instance-type-offerings --location-type availability-zone | jq '.InstanceTypeOfferings[] | select(.Location == 
env.ANTHOS_AVAILABILITY_ZONE) | .InstanceType' | grep t2.large
"t2.large"

$ aws ec2 create-key-pair --key-name anthosKeyPair --query 'KeyMaterial' --output text > anthosKeyPair.pem
$ mkdir .ssh
$ mv anthosKeyPair.pem ~/.ssh/

$ aws ec2 run-instances --image-id ami-0bba4b75264ecbfbd --count 1 --instance-type t2.large --key-name anthosKeyPair --security-group-ids 
$ANTHOS_SG_ID --subnet-id $ANTHOS_SUBNET_ID --associate-public-ip-address --block-device-mappings 
'DeviceName=/dev/sda1,Ebs={VolumeSize=200}'
```

The instance is now created. We can give it a  name.
```
$ ANTHOS_INSTANCE_ID=$(aws ec2 describe-instances | jq -r '.Reservations[] | .Instances[] | select(.SubnetId==env.ANTHOS_SUBNET_ID) | 
.InstanceId')

$ aws ec2 create-tags --resources  $ANTHOS_INSTANCE_ID --tags Key=Name,Value=anthos-node
```

## SSH
In order to SSH from the cloud shell to the Anthos instance, we first need to obtain the public IP of the cloudshell and add a rule in the 
security group to allow SSH access from that.
```
$ export MY_PUBLIC_IP=$(curl ifconfig.me --silent)
$ aws ec2 authorize-security-group-ingress --group-id $ANTHOS_SG_ID --protocol tcp --port 22 --cidr $MY_PUBLIC_IP/32
```

Copy the SSH key pair to the instance as it's needed in the Anthos cluster config.
```
$ export ANTHOS_INSTANCE_IP=$(aws ec2 describe-instances --filter Name=tag:Name,Values=anthos-node --query 
"Reservations[*].Instances[*].PublicIpAddress" --output text)

$ scp -i ~/.ssh/anthosKeyPair.pem ~/.ssh/anthosKeyPair.pem ubuntu@$ANTHOS_INSTANCE_IP:~/.ssh/anthosKeyPair.pem
```

SSH into the instance.
```
$ ssh -i ~/.ssh/anthosKeyPair.pem ubuntu@$ANTHOS_INSTANCE_IP
```

## Install gcloud
Install the gcloud cli on the Anthos instance.
```
sudo apt-get install apt-transport-https ca-certificates gnupg -y

echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a 
/etc/apt/sources.list.d/google-cloud-sdk.list

curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

sudo apt-get update -y && sudo apt-get install google-cloud-cli -y
```

## Login  to gcloud
This step is optional. Login to the gcloud cli with your account if you are going to create a service account yourself from the CLI.
```
gcloud auth login
```

## Authenticaion
Create a [service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) in GCP and give it the following roles.
```
roles/gkehub.connect
roles/gkehub.admin
roles/logging.logWriter
roles/monitoring.metricWriter
roles/monitoring.dashboardEditor
roles/stackdriver.resourceMetadata.writer
roles/opsconfigmonitoring.resourceMetadata.writer
```

If you are using the gcloud CLI, you  can create a service account and bind the roles with  the following command.
```
gcloud iam service-accounts create <service-account-name>

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member=<service-account-client-email> \
  --role=<role> \
  --no-user-output-enabled
```

Create a key for the service account and copy it's credentials.
```
gcloud iam service-accounts keys create <key-file-path> \
    --iam-account=${service-account-name}@${PROJECT_ID}.iam.gserviceaccount.com
```

Setup the credentials in the instance, activate the service account and set the project id.
```
$ mkdir .gcloud
$ export PROJECT_ID=<project_id>

$ cat > .gcloud/keyfile.json << EOF 
{
   "type": "service_account",
   "project_id": $PROJECT_ID,
   "private_key_id": "<private_key_id>",
   "private_key": <private_key>,
   "client_email": <client_email>,
   "client_id": <client_id>,
   "auth_uri": "https://accounts.google.com/o/oauth2/auth",
   "token_uri": "https://oauth2.googleapis.com/token",
   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
   "client_x509_cert_url": <client_x509_cert_url>
}
EOF

$ gcloud auth activate-service-account <client_email> --key-file .gcloud/keyfile.json

$ export GOOGLE_APPLICATION_CREDENTIALS='/home/ubuntu/.gcloud/keyfile.json'

$ gloud config set project $PROJECT_ID
```

## APIs
Enable the services.
```
gcloud services enable \
    anthos.googleapis.com \
    anthosaudit.googleapis.com \
    anthosgke.googleapis.com \
    cloudresourcemanager.googleapis.com \
    container.googleapis.com \
    gkeconnect.googleapis.com \
    gkehub.googleapis.com \
    serviceusage.googleapis.com \
    stackdriver.googleapis.com \
    monitoring.googleapis.com \
    logging.googleapis.com \
    opsconfigmonitoring.googleapis.com
```

## Other tools
Install kubectl, bmctl and docker.
```
curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s 
https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl
sudo mv kubectl /usr/local/sbin/

gsutil cp gs://anthos-baremetal-release/bmctl/1.13.0/linux-amd64/bmctl .
chmod a+x bmctl
sudo mv bmctl /usr/local/sbin/

curl -O https://download.docker.com/linux/static/stable/x86_64/docker-20.10.9.tgz
tar xzvf docker-20.10.9.tgz
sudo cp docker/* /usr/bin/
rm -rf docker*
sudo groupadd docker
sudo usermod -aG docker $USER
sudo dockerd&
newgrp docker
```

## VxLAN
Set up vxlan with the IP 10.200.2/24.
```
sudo ip link add vxlan0 type vxlan id 42 dev eth0 dstport 0
sudo ip addr add 10.200.0.2/24 dev vxlan0
sudo ip link set up dev vxlan0
```

## Cluster config
Create the Anthos cluster config with bmctl.
```
export CLUSTER_ID=anthos-aws
bmctl create config -c $CLUSTER_ID
```

Change the config.
```
$ cat > bmctl-workspace/${CLUSTER_ID}/${CLUSTER_ID}.yaml << EOF
---
gcrKeyPath: /home/ubuntu/.gcloud/keyfile.json
sshPrivateKeyPath: /home/ubuntu/.ssh/anthosKeyPair.pem
gkeConnectAgentServiceAccountKeyPath: /home/ubuntu/.gcloud/keyfile.json
gkeConnectRegisterServiceAccountKeyPath: /home/ubuntu/.gcloud/keyfile.json
cloudOperationsServiceAccountKeyPath: /home/ubuntu/.gcloud/keyfile.json
---
apiVersion: v1
kind: Namespace
metadata:
  name: cluster-${CLUSTER_ID}
---
apiVersion: baremetal.cluster.gke.io/v1
kind: Cluster
metadata:
  name: ${CLUSTER_ID}
  namespace: cluster-${CLUSTER_ID}
spec:
  profile: edge
  type: standalone
  anthosBareMetalVersion: 1.13.0
  gkeConnect:
    projectID: $PROJECT_ID
  controlPlane:
    nodePoolSpec:
      clusterName: ${CLUSTER_ID}
      nodes:
      - address: 10.200.0.2
  clusterNetwork:
    pods:
      cidrBlocks:
      - 192.168.0.0/16
    services:
      cidrBlocks:
      - 172.26.232.0/24
  loadBalancer:
    mode: bundled
    ports:
      controlPlaneLBPort: 443
    vips:
      controlPlaneVIP: 10.200.0.49
      ingressVIP: 10.200.0.50
    addressPools:
    - name: pool1
      addresses:
      - 10.200.0.50-10.200.0.70
  clusterOperations:
    location: asia-south1
    projectID: $PROJECT_ID
  storage:
    lvpNodeMounts:
      path: /mnt/localpv-disk
      storageClassName: node-disk
    lvpShare:
      numPVUnderSharedPath: 5
      path: /mnt/localpv-share
      storageClassName: local-shared
  nodeConfig:
    podDensity:
      maxPodsPerNode: 64
  nodeAccess:
    loginUser: ubuntu
EOF
```

## Cluster creation
Create the cluster.
```
$ bmctl create cluster -c ${CLUSTER_ID}
```

The above command should take some time and once it's successful, the kubernetes cluster should be ready.
```
$ export KUBECONFIG=bmctl-workspace/${CLUSTER_ID}/${CLUSTER_ID}-kubeconfig

$ kubectl get nodes
NAME          STATUS   ROLES                  AGE    VERSION
ip-10-0-0-9   Ready    control-plane,master   153m   v1.24.2-gke.1900
```
The cluster should appear on the Anthos clusters plage on GCP.

## Run workloads
Test with a sample nginx deployment.
```
$ cat > deploy.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
  selector:
    matchLabels:
      app: nginx
EOF

$ kubectl create -f deploy.yaml

$ kubectl get deploy
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   1/1     1            1           65s

$ kubectl get pod
NAME                    READY   STATUS    RESTARTS   AGE
nginx-8f458dc5b-jvrbb   1/1     Running   0          68s
```    

Expose this deployment with a service.
```
$ cat > svc.yaml <<EOF
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  selector:
    app: nginx
  ports:
  - port: 8080
    targetPort: 80
    name: web-server
EOF

$ kubectl create -f svc.yaml

$ kubectl get svc nginx
NAME    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
nginx   ClusterIP   172.26.232.21   <none>        8080/TCP   106s

$ kubectl get ep nginx
NAME    ENDPOINTS         AGE
nginx   192.168.0.48:80   2m3s
```

Try to curl the service IP  and see if it works.
```
$ curl 172.26.232.21:8080
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

## Reset the cluster
Finally reset the cluster when you no longer need it.
```
bmctl reset cluster -c ${CLUSTER_ID}
```
 
Thus, we have launched a single node kubernetes cluster with Anthos on AWS, and tested it by running an nginx service.

Thanks for reading!!!
