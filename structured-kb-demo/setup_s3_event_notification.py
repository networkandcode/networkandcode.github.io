import boto3

from arns import QUEUE_ARN
from logger import logger
from vars import BUCKET

s3 = boto3.client("s3")

notification_configuration = {
    "QueueConfigurations": [
        {
            "QueueArn": QUEUE_ARN,
            "Events": [
                "s3:ObjectCreated:*", 
                "s3:ObjectRemoved:*"
            ]
        }
    ]
}

try:
    s3.put_bucket_notification_configuration(
        Bucket=BUCKET,
        NotificationConfiguration=notification_configuration
    )
    print(f"Successfully added event notifications")
except Exception as e:
    print(f"Error: {e}")