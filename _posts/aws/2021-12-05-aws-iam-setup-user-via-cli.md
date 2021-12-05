---
title: aws iam > setup user via cli
categories: aws
---

Hey all, :wave: we shall see the following in this post: :scroll:
- Create a group
- Attach a policy :writing_hand: to the group
- Create user
- Add the user to the group
- Generate access key for the user

## AWS CLI
Ensure you have installed the [aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). Once installed, set up the credentials and configuration similar to the ones below.

Credentials.
```
$ cat ~/.aws/credentials 
[default]
aws_access_key_id=<aws_access_key_id>
aws_secret_access_key=<aws_secret_access_key>
```

Configuration.
```
$ cat ~/.aws/config 
[default]
region = us-east-2
```

## Create group
Let's create a group with the name developers-group.
```
$ aws iam create-group --group-name developers-group
{
    "Group": {
        "Path": "/", 
        "CreateDate": "2021-12-05T09:40:24Z", 
        "GroupId": "<GroupId>", 
        "Arn": "arn:aws:iam::<AccountId>:group/developers-group", 
        "GroupName": "developers-group"
    }
}
```

## List polices
There are several built in policies in AWS, that avoids the need of creating custom polcies in most cases, let's try to retrieve policies associated with EC2. Note that I have used [jq](https://stedolan.github.io/jq/download/) for parsing JSON.

```
$ aws iam list-policies | jq '.Policies[] | select(.PolicyName | contains ("EC2")) | .Arn'                                                                              
"arn:aws:iam::aws:policy/AmazonEC2FullAccess"
"arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
"arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforAWSCodeDeploy"
"arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess"
"arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
"arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role"
"arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
"arn:aws:iam::aws:policy/aws-service-role/AWSEC2SpotFleetServiceRolePolicy"
"arn:aws:iam::aws:policy/service-role/AmazonEC2SpotFleetAutoscaleRole"
"arn:aws:iam::aws:policy/CloudWatchActionsEC2Access"
"arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceEventsRole"
"arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceAutoscaleRole"
"arn:aws:iam::aws:policy/aws-service-role/AWSAutoScalingPlansEC2AutoScalingPolicy"
"arn:aws:iam::aws:policy/aws-service-role/AWSEC2SpotServiceRolePolicy"
"arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforDataPipelineRole"
"arn:aws:iam::aws:policy/service-role/AmazonEC2SpotFleetTaggingRole"
"arn:aws:iam::aws:policy/aws-service-role/AWSServiceRoleForEC2ScheduledInstances"
"arn:aws:iam::aws:policy/aws-service-role/AWSEC2FleetServiceRolePolicy"
"arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser"
"arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
"arn:aws:iam::aws:policy/aws-service-role/AWSApplicationAutoscalingEC2SpotFleetRequestPolicy"
"arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole"
"arn:aws:iam::aws:policy/AWSElasticBeanstalkCustomPlatformforEC2Role"
"arn:aws:iam::aws:policy/EC2InstanceProfileForImageBuilderECRContainerBuilds"
"arn:aws:iam::aws:policy/AmazonEC2RolePolicyForLaunchWizard"
"arn:aws:iam::aws:policy/EC2InstanceProfileForImageBuilder"
"arn:aws:iam::aws:policy/aws-service-role/AWSEC2CapacityReservationFleetRolePolicy"
"arn:aws:iam::aws:policy/aws-service-role/EC2FleetTimeShiftableServiceRolePolicy"
"arn:aws:iam::aws:policy/AWSOpsWorksRegisterCLI_EC2"
"arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforAWSCodeDeployLimited"
"arn:aws:iam::aws:policy/AWSApplicationMigrationEC2Access"
"arn:aws:iam::aws:policy/EC2InstanceConnect"
```

Now let's try to find policies related to S3. :bucket:
```
$ aws iam list-policies | jq '.Policies[] | select(.PolicyName | contains ("S3")) | .Arn'
"arn:aws:iam::aws:policy/service-role/AmazonDMSRedshiftS3Role"
"arn:aws:iam::aws:policy/AmazonS3FullAccess"
"arn:aws:iam::aws:policy/service-role/QuickSightAccessForS3StorageManagementAnalyticsReadOnly"
"arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
"arn:aws:iam::aws:policy/AmazonS3OutpostsFullAccess"
"arn:aws:iam::aws:policy/aws-service-role/S3StorageLensServiceRolePolicy"
"arn:aws:iam::aws:policy/aws-service-role/IVSRecordToS3"
"arn:aws:iam::aws:policy/service-role/AmazonS3ObjectLambdaExecutionRolePolicy"
"arn:aws:iam::aws:policy/AmazonS3OutpostsReadOnlyAccess"
```

## Attach policy
Attach a relevant EC2 policy to the group.
```
$ aws iam attach-group-policy --group-name developers-group --policy-arn "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
```

Now let's add a second policy to the group, this time related to S3.
```
$ aws iam attach-group-policy --group-name developers-group --policy-arn "arn:aws:iam::aws:policy/AmazonS3FullAccess"
```

So, the group now has read only access to EC2 and full access to S3.

## Create user
Create a user with the name developer1.
```
$ aws iam create-user --user-name developer1
{
    "User": {
        "Path": "/",
        "UserName": "developer1",
        "UserId": "<UserId>",
        "Arn": "arn:aws:iam::<AccountId>:user/developer1",
        "CreateDate": "2021-12-05T10:02:02+00:00"
    }
}
```

## Add user
Add the developer1 user to developers-group, so that the user inherits the policies attached to the group.
```
$ aws iam add-user-to-group --group-name developers-group --user-name developer1 
```

Nice they are asking for group name and user name here, unlike ARNs in cases where the names are not unique.

## Access key
Generate access key for the user, and share it with the user, so that they can setup the credentials for AWS CLI, just like you did.
```
$ aws iam create-access-key --user-name developer1
{
    "AccessKey": {
        "UserName": "developer1",
        "AccessKeyId": "<AccessKeyId>",
        "Status": "Active",
        "SecretAccessKey": "<SecretAccessKey>",
        "CreateDate": "2021-12-05T10:14:20+00:00"
    }
}
```

## Verify
List the groups, the user belongs to.
```
$ aws iam list-groups-for-user --user-name developer1  
{
    "Groups": [
        {
            "Path": "/",
            "GroupName": "developers-group",
            "GroupId": "<GroupId>",
            "Arn": "arn:aws:iam::<AccountId>:group/developers-group",
            "CreateDate": "2021-12-05T09:40:24+00:00"
        }
    ]
}
```

List the polices, the group is attached to.
```
{
    "AttachedPolicies": [
        {
            "PolicyName": "AmazonS3FullAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonS3FullAccess"
        },
        {
            "PolicyName": "AmazonEC2ReadOnlyAccess",
            "PolicyArn": "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
        }
    ]
}
```

This way you can create different groups as required, attach relevant policies to the group, and add appropriate users to each group. And finally don't forget to generate the access key for each user, and share it with them, with out which they will not be able to login via the AWS CLI. Thank you !!! :thumbsup:

--end-of-post--