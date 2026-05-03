import sys

import boto3
from botocore.exceptions import NoCredentialsError

from vars import S3_BUCKET, S3_FOLDER

def upload_to_s3(local_file, bucket, s3_file):
    s3 = boto3.client("s3")

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print(f"Upload Successful: {s3_file}")
    except FileNotFoundError:
        print("The file was not found")
    except NoCredentialsError:
        print("Credentials not available")

# Usage
if len(sys.argv) < 2:
    print("Usage: python upload_csv_to_s3.py <local_file>")
    sys.exit(1)

local_file = sys.argv[1]
upload_to_s3(local_file, S3_BUCKET, f"{S3_FOLDER}/{local_file}")
