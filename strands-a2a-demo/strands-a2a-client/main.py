import asyncio

from strands.agent.a2a_agent import A2AAgent


async def main():
    agent = A2AAgent(endpoint="http://localhost:9000")
    agent_card = await agent.get_agent_card()

    print("Invoking remote agent with agent card:")
    for key, value in agent_card:
        print(key, ":", value)
    print("-" * 20)

    while True:
        prompt = input("User: ")
        if prompt.lower() == "exit":
            break

        async for event in agent.stream_async(prompt):
            if "result" in event:
                print("AI: ", event["result"], end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
