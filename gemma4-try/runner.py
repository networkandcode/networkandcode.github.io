from google.adk.runners import Runner

from agent import search_agent
from session_service import session_service
from vars import (
    APP_NAME,
)

runner = Runner(agent=search_agent, app_name=APP_NAME, session_service=session_service)
