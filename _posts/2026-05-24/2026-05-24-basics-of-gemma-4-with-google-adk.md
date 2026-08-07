---
canonical_url: "https://dev.to/networkandcode/basics-of-gemma-4-with-google-adk-4jh4"
date: "2026-05-24"
title: "Basics of Gemma 4 with Google ADK"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fow4r7ol7woqw415ci70z.png"
tags: "devchallenge, gemmachallenge, gemma, googlecloud"
categories: "devchallenge, gemmachallenge, gemma, googlecloud"
---
**This post first appeared on [dev.to](https://dev.to/networkandcode/basics-of-gemma-4-with-google-adk-4jh4)**

*This is a submission for the [Gemma 4 Challenge: Write About Gemma 4](https://dev.to/challenges/google-gemma-2026-05-06)*

Nothing fancy here :), we  shall just explore how to use gemma4 with adk, in a step by step way, to learn the basics.

I am not going to install and run gemma4 locally(we shall discuss a few options at the end), I'd rather use the [google api](https://ai.google.dev/gemini-api/docs/pricing#gemma-4) with it, which is currently available through the free tier.

Let's initialize a uv [project](https://github.com/networkandcode/networkandcode.github.io/tree/main/gemma4-try) and set that as the current directory.
```shell
uv init gemma4-try
cd gemma4-try
```

Get an API key from the Google AI studio, and use it in .env.
```console
$ cat .env      
GOOGLE_API_KEY=<your-api-key>
```

Add the packages
```shell
uv add python-dotenv google-adk
```
Here is our [agent](https://github.com/networkandcode/networkandcode.github.io/blob/main/gemma4-try/agent.py) code, we are setting the gemma4 model..
```python
$ cat agent.py 
from google.adk import Agent

from dotenv import load_dotenv

load_dotenv()

from vars import (
    AGENT_NAME,
    MODEL,
)

search_agent = Agent(
    name=AGENT_NAME,
    model=MODEL,
)
```
The agent would be initialized with the code above, with a specific agent name and attached to a specific model, which are mentioned on a different [vars](https://github.com/networkandcode/networkandcode.github.io/blob/main/gemma4-try/vars.py) file.
```python
$ cat vars.py
AGENT_NAME="test_agent"
APP_NAME = "test_app"
MODEL="gemma-4-31b-it" # gemma-4-26b-a4b-it is also supported
SESSION_ID = "test_session"
USER_ID = "test_user"
```

We then have the [runner](https://github.com/networkandcode/networkandcode.github.io/blob/main/gemma4-try/runner.py) code, using which we will invoke the agent. The runner will also have a appname and session service associated with it.
```python
$ cat runner.py 
from google.adk.runners import Runner

from agent import search_agent
from session_service import session_service
from vars import (
    APP_NAME, 
)

runner = Runner(
    agent=search_agent,
    app_name=APP_NAME,
    session_service=session_service
)
```

The [session](https://github.com/networkandcode/networkandcode.github.io/blob/main/gemma4-try/session_service.py) service is defined in a different file. For simplicity we'd be using an in memory session service.
```python
$ cat session_service.py 
from google.adk.sessions import InMemorySessionService

session_service = InMemorySessionService()
```

Our final code is the app's entry point, [main.py](https://github.com/networkandcode/networkandcode.github.io/blob/main/gemma4-try/main.py).
```python
$ cat main.py 
import asyncio

from google.genai import types

from runner import runner
from session_service import session_service
from vars import (
    APP_NAME,
    SESSION_ID,
    USER_ID,
)
    
async def main():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    
    while True:
        user_message = input("User: ")
        content = types.Content(role='user', parts=[types.Part(text=user_message)])
        
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if (not part.thought):
                            print(part.text)

if __name__ == "__main__":
    asyncio.run(main())
```
All it does is, create a session first for test_app, test_user and test_session. And then it would invoke the agent via the runner and just print the final response with out the thinking output. If we also print `part.text`, when `part.thought` is true, it would print everything that the model goes through...

Let's run it.
```console
$ uv run main.py 
User: hello, how are you
Hello! I am test_agent. I'm doing well, thank you for asking! How can I help you today?
User: tell me abt yourself
I am an AI agent, and for our current interaction, my internal name is **test_agent**.

Essentially, I am a large language model trained to process information, answer questions, and assist with a wide variety of tasks. You can think of me as a versatile digital assistant. 

**Here are a few things I can help you with:**
*   **Answering Questions:** From complex scientific topics to general trivia.
*   **Writing & Editing:** I can help you draft emails, write stories, polish essays, or create professional documents.
*   **Problem Solving & Coding:** I can help write, debug, or explain code in various programming languages.
*   **Brainstorming:** If you're stuck on an idea for a project or a gift, I can give you a list of suggestions.
*   **Summarization:** Give me a long text, and I can boil it down to the key points.

I don't have personal feelings, beliefs, or a physical form, but I am designed to be helpful, objective, and efficient. 

Is there anything specific you'd like to test my capabilities on?
User: ^Z
```

Cool, so it works great. It also supports image & tool calling, can try may be some other time...

Although you can access gemma4 via the free tier in google API, sometimes you may get an internal server error from Google API with the free tier, it'd be better to host it on platforms such as model garden, ollama or use paid APIs though platforms such as Open router. I'd prefer APIs instead of hosting, as it may come with pay as you go offerings. I tried downloading the model with ollama with these instructions:
```shell
brew install ollama
ollama serve # keep this open
ollama run gemma4
```
However I didn't quite continue with the API, as my system was getting a bit slow...

## Model garden
Some notes about model garden, if you'd like to try...
Go to VertexAI model registry, hmm I think there is some change in there product names :), it's actually inside Agent Platform... Enable all APIs here.. And then go to model garden, search for Gemma4 and deploy it.
![Gemma4 on Model garden](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ypjnj45v5z4mga7ari1j.png)
Don't forget to delete this deployment, once you are done with your work to aovid compute charge...

Once the model is deployed there should be an endpoint created. You can then use the steps [here](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/start) to invoke the model. However we are not following this method here, in this post.

Thank you for reading!

Image credit: a quick prompt on excallidraw with some refining on gemini.
