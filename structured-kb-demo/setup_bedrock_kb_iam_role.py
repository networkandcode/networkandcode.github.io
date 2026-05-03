import boto3
import json

from arns import BEDROCK_KB_IAM_POLICY_ARN
from logger import logger
from vars import AWS_ACCOUNT_ID, AWS_REGION, BEDROCK_KB_IAM_ROLE

iam = boto3.client("iam", region_name=AWS_REGION)

trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "TrustPolicyStatement",
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": AWS_ACCOUNT_ID
                },
                "ArnLike": {
                    "aws:SourceArn": f"arn:aws:bedrock:{AWS_REGION}:{AWS_ACCOUNT_ID}:knowledge-base/*"
                }
            }
        }
    ]
}

try:
    iam.create_role(
        RoleName=BEDROCK_KB_IAM_ROLE,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description='IAM Role for Bedrock Knowledge Base to access Redshift Serverless'
    )
    logger.info(f"Created role: {BEDROCK_KB_IAM_ROLE}")

    iam.attach_role_policy(
        RoleName=BEDROCK_KB_IAM_ROLE,
        PolicyArn=BEDROCK_KB_IAM_POLICY_ARN
    )
    logger.info(f"Attached IAM policy to BedrockKB IAM role.")

except iam.exceptions.EntityAlreadyExistsException:
    logger.warning(f"Role {BEDROCK_KB_IAM_ROLE} already exists.")
except Exception as e:
    logger.error(f"Error: {e}")
