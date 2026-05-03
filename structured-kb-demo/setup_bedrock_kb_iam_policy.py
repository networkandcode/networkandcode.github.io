import boto3
import json

from arns import S3_BUCKET_ARN
from get_redshift_wg_arn import REDSHIFT_WORKGROUP_ARN
from logger import logger
from vars import AWS_ACCOUNT_ID, AWS_REGION, BEDROCK_KB_IAM_POLICY, GLUE_DB, S3_FOLDER

GLUE_TABLE = S3_FOLDER
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
                REDSHIFT_WORKGROUP_ARN
            ]
        },
        {
            "Sid": "RedshiftServerlessGetCredentials",
            "Effect": "Allow",
            "Action": "redshift-serverless:GetCredentials",
            "Resource": [
                REDSHIFT_WORKGROUP_ARN
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
        },
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "glue:GetDatabases",
                "glue:GetDatabase",
                "glue:GetTables",
                "glue:GetTable",
                "glue:GetPartitions",
                "glue:GetPartition",
                "glue:SearchTables"
            ],
            "Resource": [
                f"arn:aws:glue:{AWS_REGION}:{AWS_ACCOUNT_ID}:table/{GLUE_DB}/{GLUE_TABLE}",
                f"arn:aws:glue:{AWS_REGION}:{AWS_ACCOUNT_ID}:database/{GLUE_DB}",
                f"arn:aws:glue:{AWS_REGION}:{AWS_ACCOUNT_ID}:catalog"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                f"{S3_BUCKET_ARN}",
                f"{S3_BUCKET_ARN}/*"
            ]
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
    
    logger.info("Successfully created policy!")

except iam.exceptions.EntityAlreadyExistsException:
    logger.info("Policy already exists, updating it.")
    # Get the policy ARN
    policies = iam.list_policies(Scope='Local')
    policy_arn = next(p['Arn'] for p in policies['Policies'] if p['PolicyName'] == BEDROCK_KB_IAM_POLICY)
    
    # Create a new version and set it as default
    iam.create_policy_version(
        PolicyArn=policy_arn,
        PolicyDocument=json.dumps(policy_document),
        SetAsDefault=True
    )
    logger.info("Successfully updated policy!")
except Exception as e:
    logger.error(f"An error occurred: {e}")
