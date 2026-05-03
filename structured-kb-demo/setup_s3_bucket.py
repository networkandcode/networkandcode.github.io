from logger import logger

import boto3
from botocore.exceptions import ClientError

from vars import BUCKET, REGION

s3_client = boto3.client('s3', region_name=REGION)

try:
    s3_client.head_bucket(Bucket=BUCKET)
    logger.info(f"Bucket already exists")
except ClientError as e:
    logger.error(f"Error accessing bucket {BUCKET}: {e}")
    s3_client.create_bucket(
        Bucket=BUCKET
    )
    logger.info(f"Bucket created successfully")
