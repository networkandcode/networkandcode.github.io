from functools import lru_cache
import os

from dotenv import load_dotenv


@lru_cache(maxsize=1)
def _load_env_once() -> os._Environ[str]:
	load_dotenv()
	return os.environ

# load all env vars at once as a dictionary
env_vars = _load_env_once()

AWS_ACCOUNT_ID = env_vars["AWS_ACCOUNT_ID"]
AWS_REGION = env_vars["AWS_REGION"]

GLUE_CRAWLER_IAM_POLICY = env_vars["GLUE_CRAWLER_IAM_POLICY"]
GLUE_CRAWLER_IAM_ROLE = env_vars["GLUE_CRAWLER_IAM_ROLE"]
GLUE_CRAWLER = env_vars["GLUE_CRAWLER"]
GLUE_DB = env_vars["GLUE_DB"]

S3_BUCKET = env_vars["S3_BUCKET"]
S3_BUCKET_FOLDER = env_vars["S3_BUCKET_FOLDER"]
SQS_QUEUE = env_vars["SQS_QUEUE"]

REDSHIFT_IAM_ROLE = env_vars["REDSHIFT_IAM_ROLE"]
REDSHIFT_NAMESPACE = env_vars["REDSHIFT_NAMESPACE"]
REDSHIFT_WORKGROUP = env_vars["REDSHIFT_WORKGROUP"]
