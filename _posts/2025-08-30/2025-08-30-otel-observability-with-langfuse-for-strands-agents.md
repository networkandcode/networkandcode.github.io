---
canonical_url: "https://dev.to/aws-builders/otel-observability-with-langfuse-for-strands-agents-3eon"
date: "2025-08-30"
title: "OTEL Observability with Langfuse for Strands Agents"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fgc8douesqa70bbzs0d8l.png"
tags: "aws, llm, mcp, monitoring"
categories: "aws, llm, mcp, monitoring"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/otel-observability-with-langfuse-for-strands-agents-3eon)**

Hi :wave:, in this post we shall see how to use Open Telemetry and Langfuse cloud to observe LLM calls made via Strands Agents.

## UV
Let's initialize our project with [uv](https://docs.astral.sh/uv/).
```bash
uv init strands-langfuse-demo
```

Copy the code shown in this [video](https://www.youtube.com/watch?v=aIEpu5o4fPU) to the project, so that the content looks like below. The final code for this lab is anyway [here](https://github.com/networkandcode/networkandcode.github.io/tree/e8c3871d779440cf0b324db564087d5109b3ac09/strands-examples/strands-langfuse-demo).
```bash
$ cd strands-langfuse-demo/

$ ls -a
.  ..  .env  .python-version  README.md  k8s_mcp_agent.py  k8s_mcp_app.py  main.py  pyproject.toml
```

Let's activate the virtual environment.
```bash
uv venv

source .venv/bin/activate
```

We can now install these dependencies: [streamlit](https://pypi.org/project/streamlit/), [strands-agents](https://pypi.org/project/strands-agents/)
```bash
uv add streamlit==1.49.1
uv add strands-agents[otel]==1.6.0
```
We are adding the extra otel here, as we need to enable telemetry.

## K3S
I am using [K3S](https://k3s.io/) for launching a single node kubernetes cluster.
```bash
curl -sfL https://get.k3s.io | sh - 
```

Let's copy the kubeconfig as we will be referring to this in our agent configuration.
```bash
sudo cp /etc/rancher/k3s/k3s.yaml .
```

## Langfuse
Go to [Langfuse cloud](https://cloud.langfuse.com/) and create a new organization(for ex. my-org), inside that you can create a new project(for ex. my-llm-org). And generate api keys for the project.
![Generate API keys for Langfuse project](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/fic4nljne7f4v2t3ozsd.png)

We need to add these variables in our env file. So it looks like below.
```bash
$ cat .env
AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
AWS_DEFAULT_REGION=us-west-2
LANGFUSE_PUBLIC_KEY="pk-lf-.."
LANGFUSE_SECRET_KEY="sk-lf-.."
OTEL_EXPORTER_OTLP_ENDPOINT = "https://cloud.langfuse.com/api/public/otel"
```

Let's use this code to load the env vars and set the telemetry with otlp headers.
```bash
$ cat set_telemetry.py 
```
```python
import os
import base64

from dotenv import load_dotenv
from strands.telemetry import StrandsTelemetry


def set_telemetry():
    load_dotenv()

    # Build Basic Auth header.
    LANGFUSE_AUTH = base64.b64encode(
        f"{os.environ.get('LANGFUSE_PUBLIC_KEY')}:{os.environ.get('LANGFUSE_SECRET_KEY')}".encode()
    ).decode()
    
    # Configure OpenTelemetry endpoint & headers
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {LANGFUSE_AUTH}"

    strands_telemetry = StrandsTelemetry()
    strands_telemetry.setup_otlp_exporter()
```

Since we are loading env above, we can remove it from the agent code. These lines can be removed:
```bash
$ cat k8s_mcp_agent.py | grep dotenv
from dotenv import load_dotenv
        load_dotenv()
```

And replace it with the new file we added.
```
$ cat k8s_mcp_agent.py | grep telemetry
from set_telemetry import set_telemetry
        set_telemetry()
```

## Streamlit
Let's now run our app.
```bash
streamlit run k8s_mcp_app.py
```
I tried a prompt to get the list of namespaces.
![Check the list of namespaces from streamlit](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pkiyjm6olopb46l7nwse.png)

We can see the trace for this in langfuse.
![Trace on langfuse](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1mwtv3qdtfrxe4adfari.png)

We can add some custom attributes to traces, let's add one by the name session.id with the trace_attributes argument.
```
import uuid

self.agent = Agent(
                callback_handler=None,
                model="us.amazon.nova-micro-v1:0",
                tools=tools,
                trace_attributes={
                    "session.id": str(uuid.uuid4()),
                },
            )
```
Which we can now see in the trace in the attributes section.
![Session id in trace](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ybpj9dny9uazj59bcd0e.png)


The final agent code will be:
```bash
$ cat k8s_mcp_agent.py 
```
```python
import re

from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
import streamlit as st

from set_telemetry import set_telemetry
import uuid

def remove_html_tags(text_with_html):
    text_with_out_html = re.sub(r"<[^>]+>", "", text_with_html)
    return text_with_out_html

async def stream_result(stream):
    result = ""
    placeholder = st.empty()
    async for chunk in stream:
        if 'data' in chunk:
            result += chunk['data']
            result = remove_html_tags(result)
            placeholder.write(result)


class KubernetesMCPAgent:
    def __init__(self):
        set_telemetry()
        server_params = {
            "command": "npx",
            "args": [
                "-y",
                "kubernetes-mcp-server@latest"
            ],
            "env": {
                "KUBECONFIG": "k3s.yaml"
            }
        }
        
        self.stdio_mcp_client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                **server_params
            )
        ))

        with self.stdio_mcp_client:
            # Get the tools from the MCP server
            tools = self.stdio_mcp_client.list_tools_sync()

            # Create an agent with these tools
            self.agent = Agent(
                callback_handler=None,
                model="us.amazon.nova-micro-v1:0",
                tools=tools,
                trace_attributes={
                    "session.id": str(uuid.uuid4()),
                },
            )

    
    async def send_prompt(self, prompt):
        with self.stdio_mcp_client:
            stream = self.agent.stream_async(prompt)
            await stream_result(stream)


kubernetes_mcp_agent = KubernetesMCPAgent()
```

That's it for the post, hope we got some insights on LLM observability. Thank you for reading!
