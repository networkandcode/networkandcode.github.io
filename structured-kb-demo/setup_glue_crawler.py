import boto3

from arns import GLUE_CRAWLER_IAM_ROLE_ARN, SQS_QUEUE_ARN
from logger import logger
from vars import  AWS_REGION, GLUE_CRAWLER, GLUE_DB, S3_BUCKET, S3_FOLDER

S3_PATH = f"s3://{S3_BUCKET}/{S3_FOLDER}"

glue = boto3.client("glue", region_name=AWS_REGION)

CRAWLER_CONFIG = {
    "Role": GLUE_CRAWLER_IAM_ROLE_ARN,
    "DatabaseName": GLUE_DB,
    "Description": "Crawler for inventory data triggered by SQS events",
    "Targets": {
        "S3Targets": [
            {
                "Path": S3_PATH,
                "EventQueueArn": SQS_QUEUE_ARN,
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
    glue.create_crawler(Name=GLUE_CRAWLER, **CRAWLER_CONFIG)
    logger.info("Crawler created successfully.")
except glue.exceptions.AlreadyExistsException:
    glue.update_crawler(Name=GLUE_CRAWLER, **CRAWLER_CONFIG)
    logger.info("Crawler already exists. Updated configuration successfully.")
except Exception as e:
    logger.error(f"Error creating crawler: {e}")
