---
canonical_url: "https://dev.to/aws-builders/aws-bedrock-kb-with-glue-data-catalog-1j9g"
date: "2026-05-03"
title: "Query DB with Natural Language using AWS Bedrock structured KB, Glue, and Redshift"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fftf9swslpsu8qscuqilh.png"
tags: "aws, sql, claude, ai"
categories: "aws, sql, claude, ai"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/aws-bedrock-kb-with-glue-data-catalog-1j9g)**

Hi :wave:, In this post we shall explore Bedrock's structured KB with this architecture: `Upload CSVs to S3 > SNS Queue > Crawl data with Glue > Query with Redshift > Bedrock KB > Query with LLM`.

## Setup
Let's do some of this with code. Let's get started.

Clone the repo and switch to the project directory.
```bash
git clone git@github.com:networkandcode/networkandcode.github.io.git
cd structured-kb-demo/
```

Do a [uv](https://docs.astral.sh/uv/getting-started/installation/) sync.
```bash
uv sync
```

Setup [environment](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/.env.example) variables.
```bash
$ cat .env
AWS_ACCOUNT_ID=
AWS_ACCESS_KEY_ID=
AWS_REGION=ap-south-1
AWS_SECRET_ACCESS_KEY=

BEDROCK_KB=StructKb
BEDROCK_KB_IAM_POLICY=StructKbIamPolicy
BEDROCK_KB_IAM_ROLE=StructKbIamRole

GLUE_CRAWLER=struct-kb-glue-crawler
GLUE_CRAWLER_IAM_POLICY=StructKbGlueCrawlerIamPolicy
GLUE_CRAWLER_IAM_ROLE=StructKbGlueCrawlerIamRole
GLUE_DB=struct-kb-glue-db

REDSHIFT_IAM_ROLE=StructKbRedshiftIamRole
REDSHIFT_NAMESPACE=struct-kb-rs-ns
REDSHIFT_WORKGROUP=struct-kb-rs-wg

S3_BUCKET=struct-kb-bucket
S3_FOLDER=inventory

SQS_QUEUE=struct-kb-queue
```

## Common files
The [vars](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/vars.py) file will load all the env vars once. The [arns](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/arns.py) file is used to form some of the arns we need. And the logger file is used to setup a common [logger](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/logger.py) for rest of the code.

## Bucket
Setup an S3 [bucket](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_s3_bucket.py).
```bash
uv run setup_s3_bucket.py 
```
```bash
INFO:logger:Bucket struct-kb-s3-bucket created successfully
```

## Queue
Setup an SQS [queue](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_sqs_queue.py) with an access policy that allows the S3 bucket to send message to it.
```bash
uv run setup_sqs_queue.py
```
```bash
INFO:logger:Queue created successfully.
```

## Event notification
Update S3 bucket to [notify](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_s3_event_notification.py) SQS queue on events.
```bash
uv run setup_s3_event_notification.py
```
```plaintext
INFO:logger:Successfully added event notifications
```

## Database
Setup a glue [database](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_glue_db.py).
```bash
uv run setup_glue_db.py
```
```bash
INFO:logger:Glue database created successfully.
```

## Crawler
Setup an IAM [policy](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_glue_crawler_iam_policy.py) that allows access to the S3 bucket and SQS queue.
```bash
uv run setup_glue_crawler_iam_policy.py
```
```bash
INFO:logger:Policy created successfully!
```

Setup an IAM [role](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_glue_crawler_iam_role.py) which attaches the policy we just defined as well as the AWS managed glue policy.
```bash
uv run setup_glue_crawler_iam_role.py
```
```bash
INFO:logger:Created role
INFO:logger:AWS Glue Service Role policy attached.
INFO:logger:Custom Glue Crawler policy attached.
```

We can now provision a glue [crawler](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_glue_crawler.py) and attach the role above to it.
```bash
uv run setup_glue_crawler.py
```
```bash
INFO:logger:Crawler created successfully.
```

## Redshift
We shall setup a RedShift IAM [role](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_redshift_iam_role.py) by attaching the AWS managed policy to it.
```bash
uv run setup_redshift_iam_role.py
```
```bash
INFO:logger:Created role: StructKbRedshiftIamRole
INFO:logger:Attached AmazonRedshiftAllCommandsFullAccess to StructKbRedshiftIamRole
```
Provision a namespace, attach the role above to it, and also provision a [workgroup](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_redshift_workgroup.py) to run the namespace workloads on it.
```bash
uv run setup_redshift_workgroup.py 
```
```bash
INFO:logger:Namespace creation initiated.
INFO:logger:Workgroup creation initiated.
```

## See the data
There are two small files with sample inventory data: [inventory1](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/inventory_day_1.csv), [inventory2](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/inventory_day_2.csv).
Let's [upload](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/upload_csv_to_s3.py) the first one.
```bash
uv run upload_csv_to_s3.py inventory_day_1.csv 
```
```bash
Upload Successful: inventory/inventory_day_1.csv
```

[Run](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/run_glue_crawler.py) the crawler so that it fetches data from S3 and adds a table on glue database.
```bash
uv run run_glue_crawler.py
```
```bash
INFO:logger:Crawler started.
INFO:logger:Crawler is still running...
INFO:logger:Crawler is still running...
INFO:logger:Crawler is stopping...
INFO:logger:Crawler is stopping...
INFO:logger:Crawler is stopping...
INFO:logger:Crawler is stopping...
INFO:logger:Crawler is stopping...
INFO:logger:Crawler is stopping...
INFO:logger:Crawler is stopping...
INFO:logger:Crawler finished. Final State: READY
```

We did a lot with the cli, let's do some verification from the gui, on the web console. We can see the table on the glue db in the hirerarchy `AWS Glue > Data Catalog > Tables`.
![Table on glue db](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nahmbdtn7si7ub8qbug1.png)

Now, go to `Amazon Redshift > Serveless > Query editor v2` Click on the workspace, and use the default settings to connect. Run this command on the editor:
```sql
SELECT * FROM "awsdatacatalog"."struct-kb-glue-db"."inventory"
```
In my case the table name is inventory which is same as the s3 folder name. I got results like below.
![Redshift query result for 1 day](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/v9d9514msscvnwdt2mod.png)
Note that there are 10 records.

## Incremental data
Now, let's add another csv file for [day 2](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/inventory_day_2.csv).
```bash
uv run upload_csv_to_s3.py inventory_day_2.csv 
```
The SQS queue shoud show there is one message available.
![SQS queue status before crawler run](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9n0yebymrq0ehmxb6wr2.png)

We can run the crawler to fetch the change.
```bash
uv run run_glue_crawler.py 
```
The SQS messages available should become 0.
![SQS status after crawler run](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nrz227ew4asna6tys4cd.png) 

The same query in redshift should now give 20 records.
![Redshift query result for 2 days](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n1afel59aym0y0hqjg25.png)

## Bedrock KB
We got the results in redshift editor through the command. We can try to retrieve results via Bedrock KB through natural language.

Setup IAM [policy](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_bedrock_kb_iam_policy.py) for bedrock kb.
```bash
uv run setup_bedrock_kb_iam_policy.py 
```

Setup IAM [role](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_bedrock_kb_iam_role.py) and attach this policy.
```bash
uv run setup_bedrock_kb_iam_role.py
```
```bash
INFO:logger:Created role: StructKbBedrockKbIamRole
INFO:logger:Attached IAM policy to BedrockKB IAM role.
```

Create and sync the [knowlege base](https://github.com/networkandcode/networkandcode.github.io/blob/main/structured-kb-demo/setup_bedrock_kb.py).
```shell
uv run setup_bedrock_kb.py
```
We can go to `Amazon Bedrock > Knowledge Bases` on the web console and click on the knowledge base that was created. And test the knowledge base, I've used the following settings with a test prompt.
![Test knowledge base](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/55e1y3zwcxjl84gpnych.png)

Alright, so that's it for this post, it was somewhat a heavy exercice overall, but I think it would help us really when we have large data, than the simple data examples we have used. So far we tested with the test prompt option in the bedrock kb, we could expand this logic and use this KB with agents made using frameworks like strands, langgraph...Thank you for reading!
