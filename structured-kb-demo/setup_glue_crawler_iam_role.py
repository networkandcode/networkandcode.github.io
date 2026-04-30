import boto3

import json

from logger import logger
from vars import ACCOUNT_ID, GLUE_CRAWLER_IAM_POLICY, GLUE_CRAWLER_IAM_ROLE

iam = boto3.client("iam")

trust_policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "glue.amazonaws.com"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "aws:SourceAccount": ACCOUNT_ID
                }
            }
        }
    ]
}

try:
    iam.create_role(
        RoleName=GLUE_CRAWLER_IAM_ROLE,
        AssumeRolePolicyDocument=json.dumps(trust_policy)
    )
    logger.info(f"Created role")
except iam.exceptions.EntityAlreadyExistsException:
    logger.info(f"Role {GLUE_CRAWLER_IAM_ROLE} already exists.")


# Get existing attached policies
response = iam.list_attached_role_policies(RoleName=GLUE_CRAWLER_IAM_ROLE)
attached_policies = [p['PolicyArn'] for p in response.get('AttachedPolicies', [])]

aws_glue_policy = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
if aws_glue_policy not in attached_policies:
    iam.attach_role_policy(
        RoleName=GLUE_CRAWLER_IAM_ROLE,
        PolicyArn=aws_glue_policy
    )
    logger.info("AWS Glue Service Role policy attached.")
else:
    logger.info("AWS Glue Service Role policy already attached.")

custom_policy = f"arn:aws:iam::{ACCOUNT_ID}:policy/{GLUE_CRAWLER_IAM_POLICY}"
if custom_policy not in attached_policies:
    iam.attach_role_policy(
        RoleName=GLUE_CRAWLER_IAM_ROLE,
        PolicyArn=custom_policy
    )
    logger.info("Custom Glue Crawler policy attached.")
else:
    logger.info("Custom Glue Crawler policy already attached.")

logger.info("Policy attachment check completed.")