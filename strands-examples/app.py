import asyncio
from dotenv import load_dotenv
import time

from strands import Agent
import streamlit as st

load_dotenv()

async def main():

    agent = Agent(
        callback_handler=None,
        model="us.amazon.nova-micro-v1:0",
    )

    st.title("Strands App")

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    for message in st.session_state['messages']:
        role = message["role"]
        content = message["content"]

        with st.chat_message(role):
            st.markdown(content)

    if prompt := st.chat_input("How can I help you..."):
        messages = []
        with st.chat_message("user"):
            st.markdown(prompt)
            messages.append(
                {
                    "role": "user",
                    "content": prompt,
                }
            )

        with st.chat_message("assistant"):
            result = ""
            stream = agent.stream_async(prompt)
            placeholder = st.empty()
            async for chunk in stream:
                if 'data' in chunk:
                    result += chunk['data']
                    placeholder.markdown(result)
                    time.sleep(0.05)

            messages.append(
                {
                    "role": "assistant",
                    "content": result,
                }
            )
        st.session_state['messages'] += messages

asyncio.run(main())
