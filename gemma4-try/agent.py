from google.adk import Agent

from dotenv import load_dotenv

from tool import fetch_fruits, greet_user

load_dotenv()

from vars import (
    AGENT_NAME,
    MODEL,
)

search_agent = Agent(
    name=AGENT_NAME,
    model=MODEL,
    tools=[fetch_fruits, greet_user]
)
