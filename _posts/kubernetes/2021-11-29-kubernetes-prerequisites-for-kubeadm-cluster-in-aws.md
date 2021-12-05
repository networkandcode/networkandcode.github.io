---
categories: kubernetes
title: kubernetes > prerequisites for kubeadm cluster in aws
---

[kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/) is one of the popular tools used for bootstrapping kubernetes, here we would be setting up the [prerequisites](https://theithollow.com/2020/01/13/deploy-kubernetes-on-aws/) on AWS that are essential before launching the cluster.

This is a continuation to this [blog](https://networkandcode.github.io/aws/ec2/2021/11/14/aws-ec2-launch-instances-the-hard-way-with-cli.html) where we have launched the instances via CLI, if you followed that, you should have a file k8s-node-ips.txt with the list of instance IPs.

```
$ cat k8s-node-ips.txt
<K8S_MASTER_IP>
<K8S_NODE1_IP>
<K8S_NODE2_IP>

$ ips=$(<k8s-node-ips.txt)
```

Let's proceed with setting up the prerequisites...

## Hostname
Ensure the hostname matches with the private DNS name of the instance. Let's first check the present hostname.
```
$ for ip in $ips; do ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip hostname; done                                                                        
ip-10-0-0-9
ip-10-0-0-6
ip-10-0-0-4
```

And then check the private DNS.
```
$ for ip in $ips; do ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip "curl http://169.254.169.254/latest/meta-data/local-hostname --silent; echo"; done                                                          
ip-10-0-0-9.us-east-2.compute.internal
ip-10-0-0-6.us-east-2.compute.internal
ip-10-0-0-4.us-east-2.compute.internal
```
Note that the AWS region in this blog is different from the one in the instances launching [blog](https://networkandcode.github.io/aws/ec2/2021/11/14/aws-ec2-launch-instances-the-hard-way-with-cli.html), however most of the concepts are still the same.

Ok, so we need to set the hostname to match with the private dns, so that the region and compute.internal domain get appended to the hostname.
```
$ for ip in $ips; do ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip "curl http://169.254.169.254/latest/meta-data/local-hostname --silent | xargs sudo hostnamectl set-hostname"; done
```

Let's verify.
```
$ for ip in $ips; do ssh -i ~/.ssh/kubeadmKeyPair.pem ubuntu@$ip hostname; done
ip-10-0-0-9.us-east-2.compute.internal
ip-10-0-0-6.us-east-2.compute.internal
ip-10-0-0-4.us-east-2.compute.internal
```

So hostname is now as expected, note that you could also enable DNS hostnames at the VPC level.
```
$ aws ec2 modify-vpc-attribute --vpc-id $KUBEADM_VPC_ID --enable-dns-hostname
```


## IAM policies
We have to setup different [policies](https://itnext.io/kubernetes-part-2-a-cluster-set-up-on-aws-with-aws-cloud-provider-and-aws-loadbalancer-f02c3509f2c2) for the control plane and worker nodes. Let's begin with the control plane.

Define the control plane policy.
```
$ cat k8s-control-plane-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:DescribeLaunchConfigurations",
                "autoscaling:DescribeTags",
                "ec2:DescribeInstances",
                "ec2:DescribeRegions",
                "ec2:DescribeRouteTables",
                "ec2:DescribeSecurityGroups",
                "ec2:DescribeSubnets",
                "ec2:DescribeVolumes",
                "ec2:CreateSecurityGroup",
                "ec2:CreateTags",
                "ec2:CreateVolume",
                "ec2:ModifyInstanceAttribute",
                "ec2:ModifyVolume",
                "ec2:AttachVolume",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:CreateRoute",
                "ec2:DeleteRoute",
                "ec2:DeleteSecurityGroup",
                "ec2:DeleteVolume",
                "ec2:DetachVolume",
                "ec2:RevokeSecurityGroupIngress",
                "ec2:DescribeVpcs",
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:AttachLoadBalancerToSubnets",
                "elasticloadbalancing:ApplySecurityGroupsToLoadBalancer",
                "elasticloadbalancing:CreateLoadBalancer",
                "elasticloadbalancing:CreateLoadBalancerPolicy",
                "elasticloadbalancing:CreateLoadBalancerListeners",
                "elasticloadbalancing:ConfigureHealthCheck",
                "elasticloadbalancing:DeleteLoadBalancer",
                "elasticloadbalancing:DeleteLoadBalancerListeners",
                "elasticloadbalancing:DescribeLoadBalancers",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DetachLoadBalancerFromSubnets",
                "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
                "elasticloadbalancing:ModifyLoadBalancerAttributes",
                "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
                "elasticloadbalancing:SetLoadBalancerPoliciesForBackendServer",
                "elasticloadbalancing:AddTags",
                "elasticloadbalancing:CreateListener",
                "elasticloadbalancing:CreateTargetGroup",
                "elasticloadbalancing:DeleteListener",
                "elasticloadbalancing:DeleteTargetGroup",
                "elasticloadbalancing:DescribeListeners",
                "elasticloadbalancing:DescribeLoadBalancerPolicies",
                "elasticloadbalancing:DescribeTargetGroups",
                "elasticloadbalancing:DescribeTargetHealth",
                "elasticloadbalancing:ModifyListener",
                "elasticloadbalancing:ModifyTargetGroup",
                "elasticloadbalancing:RegisterTargets",
                "elasticloadbalancing:SetLoadBalancerPoliciesOfListener",
                "iam:CreateServiceLinkedRole",
                "kms:DescribeKey"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
EOF
```

Create the control plane policy.
```
$ aws iam create-policy --policy-name k8s-control-plane-policy --policy-document file://
```

Likewise repeat the steps for worker nodes.

Define the worker node policy.
```
$ cat k8s-worker-nodes-policy.json <<EOF
{
      "Version": "2012-10-17",
      "Statement": [
          {
              "Effect": "Allow",
              "Action": [
                  "ec2:DescribeInstances",
                  "ec2:DescribeRegions",
                  "ecr:GetAuthorizationToken",
                  "ecr:BatchCheckLayerAvailability",
                  "ecr:GetDownloadUrlForLayer",
                  "ecr:GetRepositoryPolicy",
                  "ecr:DescribeRepositories",
                  "ecr:ListImages",
                  "ecr:BatchGetImage"
              ],
              "Resource": "*"
          } 
      ]
  }
EOF
```

Create the worker nodes policy.
```
$ aws iam create-policy --policy-name k8s-worker-nodes-policy --policy-document file://k8s-worker-nodes-policy.json
```

## Trust policy
We shall define a trust policy with EC2 as the trust identity, so that we can attach that trust policy to roles we are about to create.
```
$ cat ec2-trust-policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
```

## Roles
It's time to create roles, one for the control plane, and other for the worker nodes.
```
$ aws iam create-role --role-name k8s-control-plane-role --assume-role-policy-document file://ec2-trust-policy.json

$ aws iam create-role --role-name k8s-worker-nodes-role --assume-role-policy-document file://ec2-trust-policy.json
```

Find the policy ARNs.
```
$ export K8S_CONTROL_PLANE_POLICY_ARN=$(aws iam list-policies | jq -r '.Policies[] | select(.PolicyName=="k8s-control-plane-policy") | .Arn')

$ echo $K8S_CONTROL_PLANE_POLICY_ARN                                                                                     
arn:aws:iam::<account-id>:policy/k8s-control-plane-policy

$ export K8S_WORKER_NODES_POLICY_ARN=$(aws iam list-policies | jq -r '.Policies[] | select(.PolicyName=="k8s-worker-nodes-policy") | .Arn') 

$ echo $K8S_WORKER_NODES_POLICY_ARN
arn:aws:iam::<account-id>:policy/k8s-worker-nodes-policy
```

Attach the policies to roles.
```
$ aws iam attach-role-policy --role-name k8s-control-plane-role --policy-arn $K8S_CONTROL_PLANE_POLICY_ARN

$ aws iam attach-role-policy --role-name k8s-worker-nodes-role --policy-arn $K8S_WORKER_NODES_POLICY_ARN
```

## Instance Profiles
Create [instance profiles](https://aws.amazon.com/blogs/security/new-attach-an-aws-iam-role-to-an-existing-amazon-ec2-instance-by-using-the-aws-cli/) for the EC2 instances.
```
$ aws iam create-instance-profile --instance-profile-name k8s-control-plane-instance-profile

$ aws iam create-instance-profile --instance-profile-name k8s-worker-nodes-instance-profile
```

And add roles to these instance profiles.
```
$ aws iam add-role-to-instance-profile --role-name k8s-control-plane-role --instance-profile-name k8s-control-plane-instance-profile

$ aws iam add-role-to-instance-profile --role-name k8s-worker-nodes-role --instance-profile-name k8s-worker-nodes-instance-profile
```

## Tags
We have to add [tags](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ec2/create-tags.html) to the AWS resources with the format kubernetes.io/cluster/<cluster-name>: owned, if we keep kubernetes as the cluster name also, then it would be kubernetes.io/cluster/kubernetes: owned.

Add tags to VPC, Subnet, Internet gateway and Route table.
```
$ aws ec2 create-tags --tags  "Key=kubernetes.io/cluster/kubernetes,Value=owned" --resources $KUBEADM_VPC_ID

$ aws ec2 create-tags --tags  "Key=kubernetes.io/cluster/kubernetes,Value=owned" --resources $KUBEADM_SUBNET_ID

$ aws ec2 create-tags --tags  "Key=kubernetes.io/cluster/kubernetes,Value=owned" --resources $KUBEADM_IGW_ID

$ aws ec2 create-tags --tags  "Key=kubernetes.io/cluster/kubernetes,Value=owned" --resources $KUBEADM_RTB_ID
```

Add tags to EC2 instances.
```
$ aws ec2 describe-instances | jq -r '.Reservations[] | .Instances[] | select(.SubnetId==env.KUBEADM_SUBNET_ID) | .InstanceId' 
<i-id1>
<i-id2>
<i-id3>

$ ids=$(<instance-ids.txt)

$ for id in $ids; do aws ec2 create-tags --tags "Key=kubernetes.io/cluster/kubernetes,Value=owned" --resources $id; done
```

Alright, so I think we are done with the prerequisites, we may have to revisit though, if we face an issue while launching the cluster. Thank you for reading !!!

--end-of-post--