import boto3
from botocore.exceptions import ClientError

from arns import REDSHIFT_IAM_ROLE_ARN
from logger import logger
from vars import REDSHIFT_NAMESPACE, REDSHIFT_WORKGROUP, AWS_REGION

redshift_client = boto3.client(
    "redshift-serverless",
    region_name=AWS_REGION
)

try:
    redshift_client.create_namespace(
        namespaceName=REDSHIFT_NAMESPACE,
        dbName="dev",
        iamRoles=[REDSHIFT_IAM_ROLE_ARN],
        defaultIamRoleArn=REDSHIFT_IAM_ROLE_ARN
    )

    logger.info("Namespace creation initiated.")

    redshift_client.create_workgroup(
        workgroupName=REDSHIFT_WORKGROUP,
        namespaceName=REDSHIFT_NAMESPACE
    )

    logger.info("Workgroup creation initiated.")
except ClientError as e:
    if e.response['Error']['Code'] == 'ConflictException':
        logger.warning(f"Resource already exists: {e}")
    else:
        logger.error(f"Error creating Redshift namespace or workgroup: {e}")
except Exception as e:
    logger.error(f"Error creating Redshift namespace or workgroup: {e}")
