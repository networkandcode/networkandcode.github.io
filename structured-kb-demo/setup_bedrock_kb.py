import time
import boto3
from botocore.exceptions import ClientError

from arns import BEDROCK_KB_IAM_ROLE_ARN
from get_redshift_wg_arn import REDSHIFT_WORKGROUP_ARN
from logger import logger
from vars import AWS_REGION, BEDROCK_KB, GLUE_DB, S3_FOLDER

GLUE_TABLE_FULL = f"{GLUE_DB}.{S3_FOLDER}"

bedrock = boto3.client("bedrock-agent", region_name=AWS_REGION)

def setup_structured_kb():
    try:
        logger.info(f"Creating Knowledge Base: {BEDROCK_KB}...")
        kb_response = bedrock.create_knowledge_base(
            name=BEDROCK_KB,
            roleArn=BEDROCK_KB_IAM_ROLE_ARN,
            knowledgeBaseConfiguration={
                "type": "SQL",
                "sqlKnowledgeBaseConfiguration": {
                    "type": "REDSHIFT",
                    "redshiftConfiguration": {
                        "queryEngineConfiguration": {
                            "type": "SERVERLESS",
                            "serverlessConfiguration": {
                                "workgroupArn": REDSHIFT_WORKGROUP_ARN,
                                "authConfiguration": {"type": "IAM"}
                            }
                        },
                        "storageConfigurations": [
                            {
                                "type": "AWS_DATA_CATALOG",
                                "awsDataCatalogConfiguration": {
                                    "tableNames": [GLUE_TABLE_FULL]
                                }
                            }
                        ]
                    }
                }
            }
        )
        kb_id = kb_response['knowledgeBase']['knowledgeBaseId']
        logger.info(f"Successfully created KB with ID: {kb_id}")

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConflictException':
            logger.info(f"KB {BEDROCK_KB} already exists. Fetching ID...")
            # Logic to find existing ID
            kbs = bedrock.list_knowledge_bases(maxResults=100)['knowledgeBaseSummaries']
            kb_id = next(kb['knowledgeBaseId'] for kb in kbs if kb['name'] == BEDROCK_KB)
        else:
            raise e

    try:
        logger.info("Connecting Redshift Metadata Data Source...")
        ds_response = bedrock.create_data_source(
            knowledgeBaseId=kb_id,
            name=f"{BEDROCK_KB}-metadata-source",
            dataSourceConfiguration={
                "type": "REDSHIFT_METADATA"
            }
        )
        ds_id = ds_response['dataSource']['dataSourceId']
        logger.info(f"Data Source Created: {ds_id}")

    except ClientError as e:
        if e.response['Error']['Code'] == 'ConflictException':
            logger.info("Data Source already exists. Fetching ID...")
            sources = bedrock.list_data_sources(knowledgeBaseId=kb_id)['dataSourceSummaries']
            ds_id = sources[0]['dataSourceId']
        else:
            raise e

    # TRIGGER SYNC (INGESTION)
    logger.info("Starting Metadata Ingestion Job (Sync)...")
    ingest_response = bedrock.start_ingestion_job(
        knowledgeBaseId=kb_id,
        dataSourceId=ds_id
    )
    job_id = ingest_response['ingestionJob']['ingestionJobId']

    # WAIT FOR SYNC
    while True:
        job = bedrock.get_ingestion_job(
            knowledgeBaseId=kb_id,
            dataSourceId=ds_id,
            ingestionJobId=job_id
        )
        status = job['ingestionJob']['status']
        logger.info(f"Sync Status: {status}")
        
        if status in ['COMPLETE', 'FAILED', 'STOPPED']:
            if status == 'FAILED':
                logger.error(f"Sync failed. Reasons: {job['ingestionJob'].get('failureReasons')}")
            break
        time.sleep(10)

    logger.info("Knowledge Base is now fully ready for SQL queries.")

if __name__ == "__main__":
    setup_structured_kb()