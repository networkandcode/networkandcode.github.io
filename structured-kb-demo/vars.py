from functools import lru_cache
import os

from dotenv import load_dotenv

@lru_cache(maxsize=1)
def _load_env_once() -> os._Environ[str]:
	load_dotenv()
	return os.environ

# load all env vars at once as a dictionary
env_vars = _load_env_once()

ACCOUNT_ID = env_vars["ACCOUNT_ID"]
BUCKET = env_vars["BUCKET"]
CRAWLER_IAM_POLICY = env_vars["CRAWLER_IAM_POLICY"]
CRAWLER_IAM_ROLE = env_vars["CRAWLER_IAM_ROLE"]
CRAWLER = env_vars["CRAWLER"]
DB = env_vars["DB"]
FOLDER = env_vars["FOLDER"]
QUEUE = env_vars["QUEUE"]
REDSHIFT_IAM_ROLE = env_vars["REDSHIFT_IAM_ROLE"]
REDSHIFT_NAMESPACE = env_vars["REDSHIFT_NAMESPACE"]
REDSHIFT_WORKGROUP = env_vars["REDSHIFT_WORKGROUP"]
REGION = env_vars["REGION"]
