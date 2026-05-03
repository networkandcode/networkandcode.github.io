from vars import (
    ACCOUNT_ID,
    BUCKET,
    CRAWLER_IAM_POLICY,
    CRAWLER_IAM_ROLE,
    REDSHIFT_IAM_ROLE,
    REGION,
    QUEUE,
)

AWS_MANAGED_GLUE_IAM_POLICY_ARN = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
AWS_MANAGED_REDSHIFT_IAM_POLICY_ARN = "arn:aws:iam::aws:policy/AmazonRedshiftAllCommandsFullAccess"
BUCKET_ARN = f"arn:aws:s3:::{BUCKET}"
CRAWLER_IAM_POLICY_ARN = f"arn:aws:iam::{ACCOUNT_ID}:policy/{CRAWLER_IAM_POLICY}"
CRAWLER_IAM_ROLE_ARN = f"arn:aws:iam::{ACCOUNT_ID}:role/{CRAWLER_IAM_ROLE}"
QUEUE_ARN = f"arn:aws:sqs:{REGION}:{ACCOUNT_ID}:{QUEUE}"
REDSHIFT_IAM_ROLE_ARN = f"arn:aws:iam::{ACCOUNT_ID}:role/{REDSHIFT_IAM_ROLE}"
