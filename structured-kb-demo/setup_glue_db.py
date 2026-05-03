import boto3

from logger import logger
from vars import DB_NAME, REGION

glue = boto3.client('glue', region_name=REGION)

try:
    response = glue.create_database(
        DatabaseInput={
            'Name': DB_NAME,
            'Description': 'Database for Bedrock structured knowledge base demo',
        }
    )
    logger.info(f"Glue database created successfully.")
    
except glue.exceptions.AlreadyExistsException:
    logger.error(f"Database already exists.")
except Exception as e:
    logger.error(f"Error creating Glue database: {e}")
