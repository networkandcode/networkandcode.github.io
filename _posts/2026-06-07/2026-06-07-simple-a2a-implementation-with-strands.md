---
canonical_url: "https://dev.to/aws-builders/simple-a2a-implementation-with-strands-2n7"
date: "2026-06-07"
title: "Simple A2A implementation with Strands"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fi8ymeydsxm4rg7pnh9sb.png"
tags: "ai, aws, agentskills, llm"
categories: "ai, aws, agentskills, llm"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/simple-a2a-implementation-with-strands-2n7)**

A2A has become like a standard for enabling agent to agent communication, we could use the a2a-sdk for running and configuring the a2a server and its features such as agent card, agent skills, agent executor, request handler etc. However we are going to go with a simplified approach here with strands where the agent card will be fetched automatically. Let's get started!

## Server
Initialize a uv project for the a2a server and switch to that directory.
```shell
uv init ~/strands-a2a-server
cd ~/strands-a2a-server 
```

Add the required packages.
```shell
uv add python-dotenv==1.2.2 strands-agents[a2a]==1.42.0
```

Change the code in `main.py` to look like below.
```python
$ cat main.py 
from dotenv import load_dotenv
from strands import Agent
from strands.multiagent.a2a import A2AServer

load_dotenv()

def main():
    agent = Agent(
        callback_handler=None,
        description="A sample strands agent",
        model="us.amazon.nova-micro-v1:0",
    )
    a2a_server = A2AServer(agent=agent)
    a2a_server.serve()

if __name__ == "__main__":
    main()
```

I like the simplicity here, as you see above, it's quite simple to start a basic a2a server from with in strands, with just a couple of lines of code, we didn't have to install the [a2a-sdk](https://pypi.org/project/a2a-sdk/) separately.

Run the code, to start the a2a server.
```console
$ uv run main.py 

INFO:     Started server process [18006]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:9000 (Press CTRL+C to quit)
```

## Client
Let's now do the client part on a separate terminal. Initialize the project and switch the directory.
```shell
uv init ~/strands-a2a-client
cd ~/strands-a2a-client
```

Modify `main.py` code to look as follows.
```python
import asyncio

from strands.agent.a2a_agent import A2AAgent

async def main():
    agent = A2AAgent(endpoint="http://localhost:9000")
    agent_card = await agent.get_agent_card()
    
    print("Invoking remote agent with agent card:")
    for key, value in agent_card:
        print(key, ":", value)
    print('-' * 20)
    
    while True:
        prompt = input("User: ")
        if prompt.lower() == "exit":
            break
            
        async for event in agent.stream_async(prompt):
            if "result" in event:
                print("AI: ", event["result"], end="", flush=True)

            
if __name__ == "__main__":
    asyncio.run(main())
```

We just call the remote endpoint, which is our a2a server, and iterate through the stream. We are also retrieving and printing the agent card of the remote agent.

Run the code.
```console
$ uv run main.py 
Invoking remote agent with agent card:
additional_interfaces : None
capabilities : extensions=None push_notifications=None state_transition_history=None streaming=True
default_input_modes : ['text']
default_output_modes : ['text']
description : A sample strands agent
documentation_url : None
icon_url : None
name : my strands agent
preferred_transport : JSONRPC
protocol_version : 0.3.0
provider : None
security : None
security_schemes : None
signatures : None
skills : []
supports_authenticated_extended_card : None
url : http://127.0.0.1:9000/
version : 0.0.1
--------------------
User: hi, tell me abt yourself in a single line
AI:  I'm an artificial intelligence system designed to assist and provide information on a wide range of topics.

User: exit
```

## Tools
As you see in the output above, for now the remote agent card didn't show any skills, we can add a tool on the server and the a2a wrapper in strands should automatically convert that to skills. So, we don't have to define the skills manually and can save some effort here. Let's try that. For simplicity I am going to use a built in tool from strands itself, let's add that package. Before this,  You can stop the server first with ctrl c if it's running...
```shell
uv add strands-agents-tools==0.8.0
```

We shall do a couple of changes in `main.py` of the a2a server. We have to import the tool at the top.
```python
from strands_tools import http_request
```

And we just need to use this in the agent.
```python
 tools=[http_request],
```

So our updated code will look like:
```python
$ cat main.py
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
```

We can run the server again with `uv run main.py`.

Run the client as well, in a different terminal.
```console
$ uv run main.py 

Invoking remote agent with agent card:
additional_interfaces : None
capabilities : extensions=None push_notifications=None state_transition_history=None streaming=True
default_input_modes : ['text']
default_output_modes : ['text']
description : A sample strands agent
documentation_url : None
icon_url : None
name : my strands agent
preferred_transport : JSONRPC
protocol_version : 0.3.0
provider : None
security : None
security_schemes : None
signatures : None
skills : [AgentSkill(description='Make HTTP requests to any API with comprehensive authentication including Bearer tokens, Basic auth, JWT, AWS SigV4, Digest auth, and enterprise authentication patterns. Includes session management, metrics, streaming support, cookie handling, redirect control, proxy support, and optional HTML to markdown conversion.', examples=None, id='http_request', input_modes=None, name='http_request', output_modes=None, security=None, tags=[])]
supports_authenticated_extended_card : None
url : http://127.0.0.1:9000/
version : 0.0.1
--------------------
User: 

```

If you see above, it automatically picked the skill from the added tool. It seems like a cool feature. Let's try some prompt.
```plaintext
User: check fruityvice.com and find out the fruit that has more calories      
AI:  <thinking> The data retrieved from the website provides a list of fruits along with their nutritional information, including calories. To determine which fruit has the most calories, I need to iterate through the list and compare the calorie values.</thinking>

After reviewing the list of fruits and their calorie content, it appears that **Hazelnut** has the highest calorie count with **628 calories**.

Here is the information for the fruit with the most calories:
- **Name**: Hazelnut
- **Family**: Betulaceae
- **Order**: Fagales
- **Genus**: Corylus
- **Nutritions**:
  - Calories: 628
  - Fat: 61.0
  - Sugar: 4.3
  - Carbohydrates: 17.0
  - Protein: 15.0

Therefore, the fruit that has the most calories on fruityvice.com is **Hazelnut**.

User: exit
```

Cool, it's working... Ok, so that's it for this post. We just used the features within strands to create an a2a server, and then we created a client with strands itself, and were able to communicate and get a response back from the server, and were also able to get it's agent card and skills automatically with out defining them. Thank you for reading..

Check out a few videos on Strands [here](https://youtube.com/playlist no?list=PLyRMqMV_QR0U4oB2XXYho4ULeyQBMyH30&si=URLtH4de_bHWF4sP)

Image credit: excallidraw.
