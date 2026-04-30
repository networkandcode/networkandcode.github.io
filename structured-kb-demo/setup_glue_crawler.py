import boto3

from vars import ACCOUNT_ID, BUCKET_NAME, DB_NAME, GLUE_CRAWLER_IAM_ROLE, GLUE_CRAWLER_NAME, QUEUE_NAME, REGION

CRAWLER_IAM_ROLE_ARN = f"arn:aws:iam::842960110593:role/service-role/{GLUE_CRAWLER_IAM_ROLE}"
S3_PATH = f"s3://{BUCKET_NAME}/"
SQS_ARN = f"arn:aws:sqs:{REGION}:{ACCOUNT_ID}:{QUEUE_NAME}"

glue = boto3.client("glue", region_name="us-east-1")

try:
    response = glue.create_crawler(
        Name=GLUE_CRAWLER_NAME,
        Role=CRAWLER_IAM_ROLE_ARN,
        DatabaseName=DB_NAME,
        Description="Crawler for inventory data triggered by SQS events",
        Targets={
            "S3Targets": [
                {
                    "Path": S3_PATH,
                    "EventQueueArn": SQS_ARN # Enables S3 event-aware crawling
                }
            ]
        },
        # "On-demand" means we don"t provide a Cron schedule
        SchemaChangePolicy={
            "UpdateBehavior": "UPDATE_IN_DATABASE",
            "DeleteBehavior": "DELETE_FROM_DATABASE"
        },
        RecrawlPolicy={
            "RecrawlBehavior": "CRAWL_EVENT_MODE" # Processes only events from SQS
        }
    )
    print(f"Crawler created successfully.")

except glue.exceptions.AlreadyExistsException:
    print(f"Crawler already exists.")
except Exception as e:
    print(f"Error creating crawler: {e}")