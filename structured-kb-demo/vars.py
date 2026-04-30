import os

from dotenv import load_dotenv

load_dotenv()

ACCOUNT_ID = os.getenv("ACCOUNT_ID")
BUCKET_NAME = os.getenv("BUCKET_NAME")
DB_NAME = os.getenv("DB_NAME")
GLUE_CRAWLER_IAM_POLICY=os.getenv("GLUE_CRAWLER_IAM_POLICY")
GLUE_CRAWLER_IAM_ROLE = os.getenv("GLUE_CRAWLER_IAM_ROLE")
GLUE_CRAWLER_NAME = os.getenv("GLUE_CRAWLER_NAME")
QUEUE_NAME = os.getenv("QUEUE_NAME")
REGION = os.getenv("REGION")

# derived vars
BUCKET_ARN = f"arn:aws:s3:::{BUCKET_NAME}"
QUEUE_ARN = f"arn:aws:sqs:{REGION}:{ACCOUNT_ID}:{QUEUE_NAME}"
