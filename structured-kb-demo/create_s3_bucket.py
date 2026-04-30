from logger import logger

import boto3
from botocore.exceptions import ClientError

from vars import BUCKET_NAME, REGION

s3_client = boto3.client('s3', region_name=REGION)

try:
    s3_client.head_bucket(Bucket=BUCKET_NAME)
except ClientError as e:
    logger.error(f"Error accessing bucket {BUCKET_NAME}: {e}")
    s3_client.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
    )
    logger.info(f"Bucket {BUCKET_NAME} created successfully")
