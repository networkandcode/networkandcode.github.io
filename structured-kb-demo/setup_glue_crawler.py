import boto3

from arns import CRAWLER_IAM_ROLE_ARN, QUEUE_ARN
from logger import logger
from vars import BUCKET, CRAWLER, DB, FOLDER

S3_PATH = f"s3://{BUCKET}/{FOLDER}"

glue = boto3.client("glue", region_name="us-east-1")

CRAWLER_CONFIG = {
    "Role": CRAWLER_IAM_ROLE_ARN,
    "DatabaseName": DB,
    "Description": "Crawler for inventory data triggered by SQS events",
    "Targets": {
        "S3Targets": [
            {
                "Path": S3_PATH,
                "EventQueueArn": QUEUE_ARN,
            }
        ]
    },
    "SchemaChangePolicy": {
        "UpdateBehavior": "UPDATE_IN_DATABASE",
        "DeleteBehavior": "DELETE_FROM_DATABASE",
    },
    "RecrawlPolicy": {"RecrawlBehavior": "CRAWL_EVENT_MODE"},
}

try:
    glue.create_crawler(Name=CRAWLER, **CRAWLER_CONFIG)
    logger.info("Crawler created successfully.")
except glue.exceptions.AlreadyExistsException:
    glue.update_crawler(Name=CRAWLER, **CRAWLER_CONFIG)
    logger.info("Crawler already exists. Updated configuration successfully.")
except Exception as e:
    logger.error(f"Error creating crawler: {e}")
