import asyncio
import streamlit as st
from k8s_mcp_agent import kubernetes_mcp_agent

async def main():
    st.title("Kubernetes MCP App")

    if prompt := st.chat_input("Chat with the Kubernetes API through MCP"):
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            await kubernetes_mcp_agent.send_prompt(prompt)

asyncio.run(main())
