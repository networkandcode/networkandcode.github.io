try:
    client = boto3.client("redshift-serverless", region_name=AWS_REGION)
    response = client.get_workgroup(workgroupName=REDSHIFT_WORKGROUP)
    REDSHIFT_WORKGROUP_ARN = response["workgroup"]["workgroupArn"]
except ClientError as e:
    logger.error(f"Error fetching Redshift workgroup ARN: {e.response["Error"]["Message"]}")
    REDSHIFT_WORKGROUP_ARN = None
