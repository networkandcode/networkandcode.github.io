import boto3

from vars import AWS_REGION, BEDROCK_KB

bedrock_agent = boto3.client("bedrock-agent", region_name=AWS_REGION)

def get_kb_id_by_name(kb_name):
    response = bedrock_agent.list_knowledge_bases(maxResults=10)
    for kb in response.get('knowledgeBaseSummaries', []):
        if kb['name'] == kb_name:
            return kb['knowledgeBaseId']
    return None

BEDROCK_KB_ID = get_kb_id_by_name(BEDROCK_KB)
