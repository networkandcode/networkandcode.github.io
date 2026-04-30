import boto3

import json

from logger import logger
from vars import BUCKET_ARN, GLUE_CRAWLER_IAM_POLICY

iam = boto3.client('iam')

policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                f"{BUCKET_ARN}/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes"
            ],
            "Resource": "arn:aws:sqs:us-east-1:842960110593:structured-kb-demo-queue"
        },
    ]
}

try:
    iam.create_policy(
        PolicyName=GLUE_CRAWLER_IAM_POLICY,
        PolicyDocument=json.dumps(policy_document),
        Description='Permissions for Glue Crawler to crawl S3 and use SQS Events'
    )
    logger.info(f"Policy created successfully!")
    
except iam.exceptions.EntityAlreadyExistsException:
    logger.error(f"Policy already exists.")
except Exception as e:
    logger.error(f"Error: {e}")