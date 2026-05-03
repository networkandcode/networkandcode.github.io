import time

import boto3

from logger import logger
from vars import GLUE_CRAWLER, AWS_REGION

def run_glue_crawler(crawler_name):
    glue = boto3.client("glue", region_name=AWS_REGION)

    try:
        glue.start_crawler(Name=crawler_name)
        logger.info(f"Crawler started.")

        while True:
            response = glue.get_crawler(Name=crawler_name)
            status = response["Crawler"]["State"]
            
            if status == "RUNNING":
                logger.info("Crawler is still running...")
                time.sleep(30)  # Wait 30 seconds before checking again
            elif status == "STOPPING":
                logger.info("Crawler is stopping...")
                time.sleep(10)
            else:
                logger.info(f"Crawler finished. Final State: {status}")
                break
                
    except glue.exceptions.CrawlerRunningException:
        logger.warning(f"Crawler is already running.")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

run_glue_crawler(GLUE_CRAWLER)
