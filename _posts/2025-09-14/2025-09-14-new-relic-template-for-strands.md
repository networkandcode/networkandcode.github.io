---
canonical_url: "https://dev.to/aws-builders/new-relic-template-for-strands-33p"
date: "2025-09-14"
title: "New Relic Template for Strands"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fi9xbqvhh5v0fdymwl5cp.png"
tags: "aws, newrelic, mcp, kubernetes"
categories: "aws, newrelic, mcp, kubernetes"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/new-relic-template-for-strands-33p)**

Hi :wave:, we’ll see about observability with New Relic / OTEL, for Strands Agents that shows some quick insights such as tokens used, cost for the tokens(based on a static cost set as variable), request duration, errors etc.

## Before you begin
You can check this [video](https://www.youtube.com/watch?v=aIEpu5o4fPU) for explanantion of the poc app used here, basically we would be using kubernetes mcp to interact with a k3s cluster and opentelemetry will be enabled to generate observability, the observability part for strands was discussed in this [post](https://dev.to/aws-builders/otel-observability-with-langfuse-for-strands-agents-3eon) and this [video](https://www.youtube.com/watch?v=iidTHzkXB8k). Optionally, if you'd like to know how to collect data on New Relic through otel collector, please check this [post](https://dev.to/aws-builders/otel-demo-with-and-eks-and-newrelic-3j52).

Ok, so what's new :thinking:, we have to just set the OTLP variables and modify the code a bit so that telemetry is sent to NewRelic endpoint. And a newrelic template was built to visualize the telemetry data. 

## Code
The code for the lab and the dashboard configuration is present [here](https://github.com/networkandcode/networkandcode.github.io/tree/b886650457ef0d0ae5c88aceb93eb510a3640201). You can clone and checkout as follows.
```bash
git clone https://github.com/networkandcode/networkandcode.github.io/tree/1014fbcffeda3b61d331421d2cc67d11ca98c597

cd networkandcode.github.io/strands-examples/strands-newrelic-demo/

git switch 1014fbc --detach

$ ls -a
.   .env.example     README.md         k8s_mcp_app.py  pyproject.toml    strands-agent-dashboard.json
..  .python-version  k8s_mcp_agent.py  main.py         set_telemetry.py  uv.lock
```

## ENV
You have to first get the API key of type *Ingest License* and set it  as `OTEL_EXPORTER_OTLP_HEADERS=api-key=<the-copied-value>`. So the env file would now be as follows.
```bash
$ cat .env
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-west-2

OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp.nr-data.net"
OTEL_EXPORTER_OTLP_HEADERS=api-key=
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
```

The set_telemetry file is modified.
```bash
$ cat set_telemetry.py
```
```python
from dotenv import load_dotenv
from strands.telemetry import StrandsTelemetry

def set_telemetry():
    load_dotenv()
    strands_telemetry = StrandsTelemetry()
    strands_telemetry.setup_otlp_exporter()
```

## Run 
We can now run the app, send some prompts.
```bash
$ uv run streamlit run k8s_mcp_app.py
```
![Streamlit screenshot](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/h15z2kwqfbbc4u5e3s8m.png)

## Newrelic
Telemetry data should now flow to newrelic, we can visualize data :bar_chart: and here is a screenshot from the dashboard.
![Newrelic dashboard screenshot](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8358gcxok1kbwvukha26.png)

It's a single dashboard with 3 pages :card_index_dividers: to show App level, Request(Trace) level and Operation(Span) level data. The dashboard is available as json here:
```bash
$ ls strands-agent-dashboard.json 
strands-agent-dashboard.json
```
And this can be imported to newrelic as new dashboard. You may have a look and inform if they are any errors in the dashboard. Ok so that's it for the post, thank you :handshake: for reading.
