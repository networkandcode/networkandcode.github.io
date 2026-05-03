import boto3

from arns import SQS_QUEUE_ARN
from logger import logger
from vars import S3_BUCKET

s3 = boto3.client("s3")

notification_configuration = {
    "QueueConfigurations": [
        {
            "QueueArn": SQS_QUEUE_ARN,
            "Events": [
                "s3:ObjectCreated:*", 
                "s3:ObjectRemoved:*"
            ]
        }
    ]
}

try:
    s3.put_bucket_notification_configuration(
        Bucket=S3_BUCKET,
        NotificationConfiguration=notification_configuration
    )
    logger.info("Successfully added event notifications")
except Exception as e:
    logger.error(f"Error: {e}")