---
canonical_url: https://dev.to/aws-builders/aws-cloudtrail-log-file-validation-1ehl
categories: aws, cloudtrail, logging, s3
date: 2022-08-29
tags: aws, cloudtrail, logging, s3
title: AWS CloudTrail log file validation
---

This post first appeared on [dev.to](https://dev.to/aws-builders/aws-cloudtrail-log-file-validation-1ehl)

## Introduction
CloudTrail lets us log all API calls in our AWS cloud. In this post, we shall see how to create a CloudTrail, see where the logs are stored 
in S3, delete log, digest files and perform log file validation.

## Create a CloudTrail
Search for CloudTrail on the AWS console and create a trail.
![Create cloud trail](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5ojcn1fxyhmdz2bvzvzi.png) 

## S3 bucket
A bucket should be automatically created and associated with the CloudTrail. A folder with the name CloudTrail should appear on the bucket 
where all the cloud trail logs should get saved. 
![S3 bucket for cloud trail](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yw5zei5v3ouuie7f0mbn.png) 

## Generate logs
Now let's do an activity and see if it gets logged. Create a lambda function with name helloWorld and all other settings as default. You can 
do any other activity on AWS cloud as well, instead of creating a function.
![Lambda function](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ntkzldnsrkx2xenqdsb9.png)
 
We should see some files on S3  for this activity.
![Log files on S3](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/x5oayy9diyj1w6kui5kf.png)
  
## Delete log file
I am deleting one of  the log files.
![Deleting log file](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zle3jv7vq8m0eedykz19.png)

Log files are not suppose to be modified/deleted, as they can hold important auditing information, so now we need to find if our log files 
are modified or deleted(as in this case). 

We try to validate now from the [AWS CLI](https://aws.amazon.com/cli/), it should say the digest file doesn't exit.
```
$ aws cloudtrail validate-logs --trail-arn arn:aws:cloudtrail:ap-south-1:<accoount-id>:trail/management-events --start-time 2022-08-29
Validating log files for trail arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events between 2022-08-29T00:00:00Z and 
2022-08-29T06:26:38Z

Results requested for 2022-08-29T00:00:00Z to 2022-08-29T06:26:38Z
No digests found  
```

This is because we have not enabled log file validation for the cloud trail.

## Enable Log file validation
We can enable log file validation, by editing the cloud trail.
![Enable log file validation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1s7p6e0r18dpgjs11as3.png)
 
 
## Digest
As the log file validation is enabled, we should see a new folder CloudTrail-Digest in S3.
![CloudTrail-Digest folder in S3](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ixq3invj5kug2y1m5hfj.png)
 
And digest files should get added each hour.
![Digest file in S3](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/36mc4wdwlsucq7a12n26.png)
 

## Validate
As we enabled Log file validation, we can now check the integirty of the logs.
```
$ aws cloudtrail validate-logs --trail-arn arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events --start-time 2022-08-29
Validating log files for trail arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events between 2022-08-29T00:00:00Z and 
2022-08-29T07:00:20Z

Results requested for 2022-08-29T00:00:00Z to 2022-08-29T07:00:20Z
Results found for 2022-08-29T05:55:08Z to 2022-08-29T06:55:08Z:

1/1 digest files valid
```
Though we deleted a log file earlier, it shows the digest is valid, because we did not enable log file validation then.

After an hour, we should see two digest files.
![Digest files](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vsot6bvy7kzsq632poii.png)

The log file validation seems good for now.
```
$ aws cloudtrail validate-logs --trail-arn arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events --start-time 2022-08-29
Validating log files for trail arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events between 2022-08-29T00:00:00Z and 
2022-08-29T08:17:57Z

Results requested for 2022-08-29T00:00:00Z to 2022-08-29T08:17:57Z
Results found for 2022-08-29T05:55:08Z to 2022-08-29T07:55:08Z:

2/2 digest files valid
10/10 log files valid
```

## Delete log file with validation check
We can try deleting  log file that was created after enabling log file validation.
![Delete another log file](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rmkawn7l1s5hw91o8vmb.png)

As expected the log file validations fails for one file. However the digests are still valid.
```
$ aws cloudtrail validate-logs --trail-arn arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events --start-time 2022-08-29
Validating log files for trail arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events between 2022-08-29T00:00:00Z and 
2022-08-29T08:22:42Z

Log file        
s3://aws-cloudtrail-logs-<account-id>-4a8dcb98/AWSLogs/<account-id>/CloudTrail/ap-south-1/2022/08/29/<account-id>_CloudTrail_ap-south-1_20220829T0755Z_7rDSVFC6Icgi9Z8V.json.gz     
INVALID: not found

Results requested for 2022-08-29T00:00:00Z to 2022-08-29T08:22:42Z
Results found for 2022-08-29T05:55:08Z to 2022-08-29T07:55:08Z:

2/2 digest files valid
9/10 log files valid, 1/10 log files INVALID
```
It also clearly says the validation failed because it can't find a file that we deleted.

## Delete digest
This time we can try deleting a digest file.
![Delete digest](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vzzw970xszdwllgpqqdp.png)

Hence digest validation should also fail.
```
$ aws cloudtrail validate-logs --trail-arn arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events --start-time 2022-08-29
Validating log files for trail arn:aws:cloudtrail:ap-south-1:<account-id>:trail/management-events between 2022-08-29T00:00:00Z and 
2022-08-29T10:09:35Z

Digest file     
s3://aws-cloudtrail-logs-<account-id>-4a8dcb98/AWSLogs/<account-id>/CloudTrail-Digest/ap-south-1/2022/08/29/<account-id>_CloudTrail-Digest_ap-south-1_management-events_ap-south-1_20220829T085508Z.json.gz 
INVALID: not found

Log file        
s3://aws-cloudtrail-logs-<account-id>-4a8dcb98/AWSLogs/<account-id>/CloudTrail/ap-south-1/2022/08/29/<account-id>_CloudTrail_ap-south-1_20220829T0755Z_7rDSVFC6Icgi9Z8V.json.gz     
INVALID: not found

Results requested for 2022-08-29T00:00:00Z to 2022-08-29T10:09:35Z
Results found for 2022-08-29T05:55:08Z to 2022-08-29T09:55:08Z:

3/4 digest files valid, 1/4 digest files INVALID
20/21 log files valid, 1/21 log files INVALID
```

Note that we can enable versioning on S3 buckets to restore files.
 
## Summary
So we saw how the log file validation feature in CloudTrail helps us find if there were any manual modifications to the log files or digest 
files. Thank you for reading !!!
