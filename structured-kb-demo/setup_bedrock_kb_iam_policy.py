import boto3
import json

from logger import logger
from vars import AWS_ACCOUNT_ID, BEDROCK_KB_IAM_POLICY

iam = boto3.client("iam")

# Define the policy document
policy_document = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RedshiftDataAPIStatementPermissions",
            "Effect": "Allow",
            "Action": [
                "redshift-data:GetStatementResult",
                "redshift-data:DescribeStatement",
                "redshift-data:CancelStatement"
            ],
            "Resource": ["*"],
            "Condition": {
                "StringEquals": {
                    "redshift-data:statement-owner-iam-userid": "${aws:userid}"
                }
            }
        },
        {
            "Sid": "RedshiftDataAPIExecutePermissions",
            "Effect": "Allow",
            "Action": [
                "redshift-data:ExecuteStatement"
            ],
            "Resource": [
                f"arn:aws:redshift-serverless:us-east-1:{AWS_ACCOUNT_ID}:workgroup/*"
            ]
        },
        {
            "Sid": "RedshiftServerlessGetCredentials",
            "Effect": "Allow",
            "Action": "redshift-serverless:GetCredentials",
            "Resource": [
                f"arn:aws:redshift-serverless:us-east-1:{AWS_ACCOUNT_ID}:workgroup/*"
            ]
        },
        {
            "Sid": "SqlWorkbenchAccess",
            "Effect": "Allow",
            "Action": [
                "sqlworkbench:GetSqlRecommendations",
                "sqlworkbench:PutSqlGenerationContext",
                "sqlworkbench:GetSqlGenerationContext",
                "sqlworkbench:DeleteSqlGenerationContext"
            ],
            "Resource": "*"
        },
        {
            "Sid": "KbAccess",
            "Effect": "Allow",
            "Action": [
                "bedrock:GenerateQuery"
            ],
            "Resource": "*"
        }
    ]
}

try:
    # Create the policy
    response = iam.create_policy(
        PolicyName=BEDROCK_KB_IAM_POLICY,
        PolicyDocument=json.dumps(policy_document),
        Description="Permissions for Bedrock Structured KB to query Redshift Serverless."
    )
    
    logger.info(f"Successfully created policy!")

except iam.exceptions.EntityAlreadyExistsException:
    logger.info(f"Policy already exists.")
except Exception as e:
    logger.error(f"An error occurred: {e}")
