from dotenv import load_dotenv
from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands_tools import http_request

load_dotenv()


def main():
    agent = Agent(
        callback_handler=None,
        description="A sample strands agent",
        model="us.amazon.nova-micro-v1:0",
        name="my strands agent",
        tools=[http_request],
    )
    a2a_server = A2AServer(agent=agent)
    a2a_server.serve()


if __name__ == "__main__":
    main()
