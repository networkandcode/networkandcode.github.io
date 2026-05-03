import boto3
import json

from arns import AWS_MANAGED_REDSHIFT_IAM_POLICY_ARN
from logger import logger
from vars import REDSHIFT_IAM_ROLE, AWS_REGION

iam = boto3.client("iam", region_name=AWS_REGION)

trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": [
                    "redshift-serverless.amazonaws.com",
                    "redshift.amazonaws.com",
                    "sagemaker.amazonaws.com"
                ]
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

try:
    iam.create_role(
        RoleName=REDSHIFT_IAM_ROLE,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description="Role for Redshift Serverless to access Glue and S3"
    )
    logger.info(f"Created role: {REDSHIFT_IAM_ROLE}")

    iam.attach_role_policy(
        RoleName=REDSHIFT_IAM_ROLE,
        PolicyArn=AWS_MANAGED_REDSHIFT_IAM_POLICY_ARN
    )
    logger.info(f"Attached AmazonRedshiftAllCommandsFullAccess to {REDSHIFT_IAM_ROLE}")

except iam.exceptions.EntityAlreadyExistsException:
    logger.warning(f"Role {REDSHIFT_IAM_ROLE} already exists.")
except Exception as e:
    logger.error(f"Error: {e}")
