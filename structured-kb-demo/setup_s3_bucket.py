from logger import logger

import boto3
from botocore.exceptions import ClientError

from vars import S3_BUCKET, AWS_REGION

s3_client = boto3.client('s3', region_name=AWS_REGION)

try:
    s3_client.head_bucket(Bucket=S3_BUCKET)
    logger.info(f"Bucket {S3_BUCKET} already exists")
except ClientError as e:
    logger.error(f"Error accessing bucket {S3_BUCKET}: {e}")
    s3_client.create_bucket(
        Bucket=S3_BUCKET,
        CreateBucketConfiguration={'LocationConstraint': AWS_REGION}
    )
    logger.info(f"Bucket {S3_BUCKET} created successfully")
