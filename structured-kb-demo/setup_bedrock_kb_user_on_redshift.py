import time

import boto3

from logger import logger
from vars import AWS_REGION, BEDROCK_KB_IAM_ROLE, REDSHIFT_WORKGROUP

redshift_user = f"IAMR:{BEDROCK_KB_IAM_ROLE}"

# Initialize Redshift Data Client
client = boto3.client("redshift-data", region_name=AWS_REGION)

# Define the SQL commands
sql_statements = [
    f'CREATE USER "{redshift_user}" WITH PASSWORD DISABLE;',
    'GRANT USAGE ON DATABASE awsdatacatalog TO "IAMR:StructKbIamRole";',
]

try:
    # Execute as a batch
    response = client.batch_execute_statement(
        WorkgroupName=REDSHIFT_WORKGROUP,
        Database="awsdatacatalog",
        Sqls=sql_statements
    )
    
    execution_id = response['Id']
    logger.info(f"Execution started. ID: {execution_id}")

    # (Optional) Wait for completion
    while True:
        status = client.describe_statement(Id=execution_id)
        state = status['Status']
        if state in ['FINISHED', 'FAILED', 'ABORTED']:
            logger.info(f"Final Status: {state}")
            if state == 'FAILED':
                logger.error(f"Error: {status.get('Error')}")
            break
        time.sleep(2)

except Exception as e:
    logger.error(f"Failed to execute: {e}")