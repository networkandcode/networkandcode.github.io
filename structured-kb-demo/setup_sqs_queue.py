import json

import boto3

from arns import BUCKET_ARN, QUEUE_ARN
from logger import logger
from vars import QUEUE, REGION

sqs = boto3.client('sqs', region_name=REGION)

access_policy = {
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "s3.amazonaws.com"
            },
            "Action": "sqs:SendMessage",
            "Resource": QUEUE_ARN,
            "Condition": {
                "ArnLike": {
                    "aws:SourceArn": BUCKET_ARN
                }
            }
        }
    ]
}

try:
    # Check if queue exists
    sqs.get_queue_url(QueueName=QUEUE)
    logger.info(f"Queue already exists.")
except sqs.exceptions.QueueDoesNotExist:
    # Create queue if it doesn't exist
    sqs.create_queue(
        QueueName=QUEUE,
        Attributes={
            'Policy': json.dumps(access_policy)
        }
    )
    logger.info(f"Queue created successfully.")
except Exception as e:
    logger.error(f"Error: {e}")