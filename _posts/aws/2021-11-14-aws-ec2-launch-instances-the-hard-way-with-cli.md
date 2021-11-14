---
categories: aws ec2
title: aws ec2 > launch instances the hard way with cli
---

Hey All :wave:, in this post we shall launch 3 AWS EC2 instances and test SSH connectivity to those...

We are not going to use the GUI / Web console :relaxed: for this purpose, we would be using the CLI :sweat_drops:, and also create individual components along the way, that are required for the instances to function properly, instead of relying on default ones, and thus touch bits of networking and security areas. Hope this approach gives someone a better understanding of the different components(like it gave me) that glue together underhood / behind the scenes, which we don't usually notice when we quickly setup instances with all the default options.

Hence, please ensure you have the following installed and configured: [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) and [jq](https://stedolan.github.io/jq/download/). Note that jq is used to parse JSON content at different places in this post, though you can use the AWS CLI's built in filters.

You would see the naming conventions such as kubeadm or k8s, as these nodes are created for the purpose of creating a kubernetes cluster, and I thought I would keep the instance launching setup as a separate post.

Alright, let's get started...

## Configuration
I have configured us-west-2 as the default region. You can change this as required.
```
$ cat ~/.aws/config 
[default]
region = us-west-2
```

And you should also see a credentials file like this.
```
$cat ~/.aws/credentials 
[default]
aws_access_key_id=<aws_access_key_id>
aws_secret_access_key=<aws_secret_access_key>
```

## Key Pair
Create an [ssh key pair](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-keypairs.html), as we need it to login via SSH, to the instances we are about to launch.
```
$ aws ec2 create-key-pair --key-name kubeadmKeyPair --query 'KeyMaterial' --output text > kubeadmKeyPair.pem

$ ls
kubeadmKeyPair.pem
```

You can set permission 400 so that only you can read it, beneficial if its a shared system.
```
$ chmod 400 kubeadmKeyPair.pem
```

And move it to the .ssh directory, where ssh keys are usually stored.
```
$ mv kubeadmKeyPair.pem ~/.ssh/.
```

## VPC
Let's create a [VPC](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/create-vpc.html) from which we can reserve IPs for the EC2 instances.
```
$ aws ec2 create-vpc --cidr-block 10.0.0.0/28
```

This is a /28 subnet which should give a total of 2 ^ (32-28) = 2 ^ 4 = 16 IPs, including the gateway and broadcast IP. We can not create VPCs with lesser IPs, 16 IPs are minimum, no matter we need it or not.

Let's retreive the VPC ID and save it in a variable.
```
$ export KUBEADM_VPC_ID=$(aws ec2 describe-vpcs | jq -r '.Vpcs[] | select(.CidrBlock == "10.0.0.0/28") | .VpcId')
$ echo $KUBEADM_VPC_ID
<vpc-id>
```

## Internet Gateway
We shall create an [Internet Gateway](https://docs.aws.amazon.com/cli/latest/reference/ec2/create-internet-gateway.html), as we need internet access to our instances, to access them via SSH from the local machine.
```
$ aws ec2 create-internet-gateway --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=kubeadm-k8s-igw}]'
```

Retrieve the gateway id.
```
$ export KUBEADM_IGW_ID=$(aws ec2 describe-internet-gateways --filters Name=tag:Name,Values=kubeadm-k8s-igw --query "InternetGateways[*].InternetGatewayId" --output text)

$ echo $KUBEADM_IGW_ID
<igw-id>
```

Now, let's [attach](https://docs.aws.amazon.com/cli/latest/reference/ec2/attach-internet-gateway.html) this to the VPC.
```
$ aws ec2 attach-internet-gateway --internet-gateway-id $KUBEADM_IGW_ID --vpc-id $KUBEADM_VPC_ID
```

## Route Table

A route table will be associated with the VPC we created. Let' find it.
```
$ KUBEADM_RTB_ID=$(aws ec2 describe-route-tables | jq -r '.RouteTables[] | select(.VpcId == env.KUBEADM_VPC_ID) | .RouteTableId')

$ echo $KUBEADM_RTB_ID
<rtb-id>
```

We can add a default route in this table, that points to our Internet Gateway.
```
$ aws ec2 create-route --route-table-id $KUBEADM_RTB_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $KUBEADM_IGW_ID
{
    "Return": true
}
```

## Subnet
A VPC can have more than one subnet, however the minimum number of IPs in the [EC2 subnet](https://docs.aws.amazon.com/cli/latest/reference/ec2/create-subnet.html?highlight=subnet) is also 16, hence we can only have one subnet in this case, which suits our requirement though. Sixteen IPs in the subnet is more than enough, as we plan to launch only 3 instances in this subnet.
```
$ aws ec2 create-subnet --cidr-block 10.0.0.0/28 --vpc-id $KUBEADM_VPC_ID
```

The subnet is created, let's save the subnet id too.
```
$ export KUBEADM_SUBNET_ID=$(aws ec2 describe-subnets | jq -r '.Subnets[] | select(.CidrBlock == "10.0.0.0/28") | .SubnetId')

$ echo $KUBEADM_SUBNET_ID
<subnet-id>
```

Note that if you have duplicate subnets, then you may also have to add a condition above to check if the subnet belongs to the correct VPC.

We can check the availabilty zone of the subnet.
```
$ export KUBEADM_AVAILABILITY_ZONE=$(aws ec2 describe-subnets | jq -r '.Subnets[] | select(.CidrBlock == "10.0.0.0/28") | .AvailabilityZone')

$ echo $KUBEADM_AVAILABILITY_ZONE
us-west-2b
```

## Security Group
We would need a [security group](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-sg.html), that we can attach to our VPC, so that the instances launched in the subnet of the VPC, would leverage the rules defined in the security group.
```
$ aws ec2 create-security-group --group-name kubeadm-sg --description "kubeadm security group" --vpc-id $KUBEADM_VPC_ID
```

Let's save the security group's id in a variable.
```
$ export KUBEADM_SG_ID=$(aws ec2 describe-security-groups | jq -r '.SecurityGroups[] | select(.GroupName == "kubeadm-sg") | .GroupId')

$ echo $KUBEADM_SG_ID
<sg-id>
```

## Image ID
We need to choose an Image for our instances. I am going to choose Ubuntu 20.04 LTS on amd64 architecture, you can get the ami for Ubuntu from this [link](https://cloud-images.ubuntu.com/locator/ec2/), I am going to pick ami-036d46416a34a611c.

## Instance Type
I am creating these instances to make a kubernetes cluser out of those. Hence, we need to choose an instance type that suffices kubernetes [resource requirements](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/), we need to have a minimum of 2 GB Ram and 2 CPUs. Hence I am going to filter for instance types that have 4 GB Ram, which is 4/1.074, i.e. approximately 3.75 GiB or 3840 MiB.
```
$ aws ec2 describe-instance-types | jq '.InstanceTypes[] | select(.MemoryInfo.SizeInMiB == 3840) | (.InstanceType, .VCpuInfo.DefaultVCpus)'
"c3.large"
2
"c4.large"
2
"m3.medium"
1
```

Let's check for instance types with 4GiB RAM this time, which also has 2 Default CPUs
```
$ aws ec2 describe-instance-types | jq '.InstanceTypes[] | select(.MemoryInfo.SizeInMiB == 4096) | select (.VCpuInfo.DefaultVCpus == 2) | .InstanceType' | sort
"a1.large"
"c5ad.large"
"c5a.large"
"c5d.large"
"c5.large"
"c6gd.large"
"c6g.large"
"c6gn.large"
"c6i.large"
"t2.medium"
"t3a.medium"
"t3.medium"
"t4g.medium"
```

Let's check if t2.medium is available in our subnet's availability zone. Please refer to this [link](https://aws.amazon.com/premiumsupport/knowledge-center/ec2-instance-type-not-supported-az-error/) for more details.
```
$ aws ec2 describe-instance-type-offerings --location-type availability-zone | jq '.InstanceTypeOfferings[] | select(.Location == env.KUBEADM_AVAILABILITY_ZONE) | .InstanceType' | grep t2.medium
"t2.medium"
```
So, let's fix t2.medium.

## Instances
We can now go ahead and create the [EC2 instances](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-instances.html). 
```
$ aws ec2 run-instances --image-id ami-036d46416a34a611c --count 3 --instance-type t2.medium --key-name kubeadmKeyPair --security-group-ids $KUBEADM_SG_ID --subnet-id $KUBEADM_SUBNET_ID --associate-public-ip-address
```

We have also enabled public IP address as we need to SSH in to the instances from our machine.

Great, so our instances are created finally.
```
$ aws ec2 describe-instances | jq -r '.Reservations[0] | .Instances[] | select(.SubnetId==env.KUBEADM_SUBNET_ID) | .InstanceId' 
<i-id1>
<i-id2>
<i-id3>
```

Let's give these instances, some [names](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-instances.html#tagging-instances).
```
$ aws ec2 create-tags --resources <i-id1> --tags Key=Name,Value=k8s-master
$ aws ec2 create-tags --resources <i-id2> --tags Key=Name,Value=k8s-node1
$ aws ec2 create-tags --resources <i-id3> --tags Key=Name,Value=k8s-node2
```

We can get the public IP as follows.
```
$ export K8S_MASTER_IP=$(aws ec2 describe-instances --filter Name=tag:Name,Values=k8s-master --query "Reservations[*].Instances[*].PublicIpAddress" --output text)

$ echo $K8S_MASTER_IP
<master-public-ip>

$ export K8S_NODE1_IP=$(aws ec2 describe-instances --filter Name=tag:Name,Values=k8s-node1 --query "Reservations[*].Instances[*].PublicIpAddress" --output text)

$ echo $K8S_NODE1_IP
<node1-public-ip>

$ export K8S_NODE2_IP=$(aws ec2 describe-instances --filter Name=tag:Name,Values=k8s-node2 --query "Reservations[*].Instances[*].PublicIpAddress" --output text)
 
$ echo $K8S_NODE2_IP
<node2-public-ip>
```

## SSH
We need to access the instances via SSH from the local machine, for which we need allow port 22 on the security group.

Get the local machine's public IP.
```
$ export MY_PUBLIC_IP=$(curl ifconfig.me --silent)
$ echo $MY_PUBLIC_IP
<public-ip>
```

We can now :pencil: [add the rule](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html).
```
$ aws ec2 authorize-security-group-ingress --group-id $KUBEADM_SG_ID --protocol tcp --port 22 --cidr $MY_PUBLIC_IP/32
```

Let's add the node IPs to a file.
```
$ cat > k8s-node-ips.txt <<EOF
$K8S_MASTER_IP
$K8S_NODE1_IP
$K8S_NODE2_IP
EOF
```

And then test the connection.
```
$ for ip in $ips; do ssh ubuntu@$ip -i ~/.ssh/kubeadmKeyPair.pem 'echo -n "Hello World!, my AWS EC2 hostname is "; hostname'; done
Hello World!, my AWS EC2 hostname is ip-10-0-0-5
Hello World!, my AWS EC2 hostname is ip-10-0-0-11
Hello World!, my AWS EC2 hostname is ip-10-0-0-12
```

## Summary
So we have successfully launched 3 EC2 instances using the AWS CLI, you can customize the options in the commands used, to create instances with different configuration as required. Thank you !!! :congratulations:.

--end-of-post--
