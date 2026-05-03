import json

import boto3

from arns import S3_BUCKET_ARN, SQS_QUEUE_ARN
from logger import logger
from vars import SQS_QUEUE, AWS_REGION

sqs = boto3.client('sqs', region_name=AWS_REGION)

access_policy = {
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "s3.amazonaws.com"
            },
            "Action": "sqs:SendMessage",
            "Resource": SQS_QUEUE_ARN,
            "Condition": {
                "ArnLike": {
                    "aws:SourceArn": S3_BUCKET_ARN
                }
            }
        }
    ]
}

try:
    # Check if queue exists
    sqs.get_queue_url(QueueName=SQS_QUEUE)
    logger.info("Queue already exists.")
except sqs.exceptions.QueueDoesNotExist:
    # Create queue if it doesn't exist
    sqs.create_queue(
        QueueName=SQS_QUEUE,
        Attributes={
            'Policy': json.dumps(access_policy)
        }
    )
    logger.info("Queue created successfully.")
except Exception as e:
    logger.error(f"Error: {e}")