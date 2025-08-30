from dotenv import load_dotenv
from strands import Agent
from strands_tools import current_time

load_dotenv()

def agent_callback(**kwargs):
    event = kwargs
    if 'result' in event:
        with open('result.md', 'w') as f:
            f.write(str(event['result']))

agent = Agent(
    callback_handler=agent_callback,
    model="us.amazon.nova-micro-v1:0",
    tools=[current_time],
)

agent("Give me the current time in 5 different countries")
