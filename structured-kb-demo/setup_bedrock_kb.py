import boto3

from arns import BEDROCK_KB_IAM_ROLE_ARN, REDSHIFT_WORKGROUP_ARN
from logger import logger
from vars import AWS_REGION, BEDROCK_KB, GLUE_DB, S3_FOLDER

GLUE_TABLE = S3_FOLDER

bedrock = boto3.client("bedrock-agent", region_name=AWS_REGION)

bedrock.create_knowledge_base(
    name=BEDROCK_KB,
    roleArn=BEDROCK_KB_IAM_ROLE_ARN,
    knowledgeBaseConfiguration={
        "type": "STRUCTURED",
        "sqlKnowledgeBaseConfiguration": {
            "type": "REDSHIFT",
            "redshiftConfiguration": {
                "queryEngineConfiguration": {
                    "type": "SERVERLESS",
                    "serverlessConfiguration": {
                        "workgroupArn": REDSHIFT_WORKGROUP_ARN,
                        "authConfiguration": {
                            "type": "IAM" 
                        }
                    }
                },
                "storageConfigurations": [
                    {
                        "type": "AWS_DATA_CATALOG",
                        "awsDataCatalogConfiguration": {
                            "tableNames": [f"{GLUE_DB}.{GLUE_TABLE}"]
                        }
                    }
                ]
            }
        }
    }
)

logger.info(f"KB Created: {BEDROCK_KB} with Redshift Serverless as data source.")