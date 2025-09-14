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
