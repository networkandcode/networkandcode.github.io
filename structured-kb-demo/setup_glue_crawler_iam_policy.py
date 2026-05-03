import boto3

import json

from arns import BUCKET_ARN, CRAWLER_IAM_POLICY_ARN, QUEUE_ARN

from logger import logger
from vars import CRAWLER_IAM_POLICY

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
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl",
                "sqs:PurgeQueue",
                "sqs:ReceiveMessage",
                "sqs:SetQueueAttributes"
            ],
            "Resource": QUEUE_ARN
        },
    ]
}

try:
    iam.create_policy(
        PolicyName=CRAWLER_IAM_POLICY,
        PolicyDocument=json.dumps(policy_document),
        Description='Permissions for Glue Crawler to crawl S3 and use SQS Events'
    )
    logger.info(f"Policy created successfully!")
    
except iam.exceptions.EntityAlreadyExistsException:
    logger.info(f"Policy already exists. Updating...")
    try:
        # Create a new policy version
        iam.create_policy_version(
            PolicyArn=CRAWLER_IAM_POLICY_ARN,
            PolicyDocument=json.dumps(policy_document),
            SetAsDefault=True
        )
        logger.info(f"Policy updated successfully!")
    except Exception as e:
        logger.error(f"Error updating policy: {e}")
        
except Exception as e:
    logger.error(f"Error: {e}")