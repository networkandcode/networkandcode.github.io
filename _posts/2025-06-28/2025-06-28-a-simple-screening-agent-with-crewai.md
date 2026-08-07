---
canonical_url: "https://dev.to/aws-builders/a-simple-screening-agent-with-crewai-539l"
date: "2025-06-28"
title: "A simple screening agent with CrewAI"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Ft50zrclm9wcqyh44r0um.png"
tags: "aws, llm, python, ai"
categories: "aws, llm, python, ai"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/a-simple-screening-agent-with-crewai-539l)**

Let's try a simple exercise with [CrewAI](https://www.crewai.com/) with a single agent and task, that parses information it has from [AWS docs](https://docs.aws.amazon.com/), and prepares a list of questions that could be used for basic screening during interviews. Of course we can do this with chatgpt, gemini etc. with their UI, but having some sort of a code can also help, for repeatable tasks, and for further refining the logic and automation. Also, we shall look into some basic concepts of CrewAI such as agents, tasks, crew as we do this. Let's get started! :rocket:

Initialize a project with [uv](https://pypi.org/project/uv/) and switch directory.
```
$ uv init screening_agent
$ cd screening_agent/ 

$ ls -a
.               ..              .git            .gitignore      .python-version main.py         pyproject.toml  README.md
```

Setup a virtual environment and activate it.
```
$ uv venv
$ source .venv/bin/activate
```

Add crewai as dependency and install it.
```
$ cat pyproject.toml | grep dependencies
dependencies = ["crewai==0.134.0"]

$ uv lock

$ uv sync  
```

## LLM
I am using `gemini/gemma-3n-e2b-it` for this exercise, the API key for which was obtained from [Google AI studio](https://aistudio.google.com/apikey). We need to setup `.env` file to hold the key.
```
GOOGLE_API_KEY=<Paste-your-key>
```

We can add the llm setup in a separate python file `llm.py`.
```python
import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model='gemini/gemma-3n-e2b-it',
    api_key=os.getenv('GOOGLE_API_KEY'),
    temperature=0.0
)
```
So we have read the api key from `.env` file and passed it to the LLM.

## Agent
We can then define our agent in `agents.py`. We are using only one agent in this exercise to keep it simple.
```
from crewai import Agent
from llm import llm

screening_agent = Agent(
    role="Screening Agent for AWS interviews",
    goal="Get content from AWS official documentation about the topics: {topics}",
    backstory="You will explore relevant links from AWS official documentation https://docs.aws.amazon.com/ about the topics: {topics}"
              "Try as much as possible to gather links that have information about all the topics on the same webpage"
              "You will then prepare a total of 10 questions and their answers"
              "The number of questions to be evenly split among the topics as much as possible"
              "The length of each question should be 1 line"
              "The length of the answer should also be 1 line"
              "Display numbering for the questions from 1 to 10"
              "You also need to capture the link from which that question and answer was prepared",
	verbose=True,
    llm=llm,
)
```
All in plain English, we are setting proper context with the role, goal and backstory arguments. We are setting verbose to see somewhat detailed output while we run the code, and then map the llm we defined in the previous step. This means each agent can be mapped to a separate llm if required. Also, note that there is one parameter enclosed in curly braces `{topics}`, we will be passing this later as input when we initialize the crew.

## Task
Let's define our task in `tasks.py`, that will call the agent.
```python
from crewai import Task
from agents import screening_agent

screening_task = Task(
    description=(
        "Get key information about the topics: {topics}\n"
        "Make the content understandable for non technical audience as well"
        "As this task could be used by HR recruiters as well, for screening purposes"
    ),
    expected_output=(
        "There should be 10 sections in the output"
        "Each section should have Question:, Answer: and Reference Link:"
    ),
    agent=screening_agent
)
```
Again in plain English, give appropriate context with the description and expected_output arguments. Note that `{topics}` is used here as well just like the agent.

## Crew
We finally have the starting point of our code in `main.py` where our crew will be defined. We need to map it with both the agents and tools. Note that we only have a single tool in this case, if there are more tools, those would be executed sequentially, by default.
```python
from crewai import Crew
from agents import screening_agent
from tasks import screening_task

def main():
    crew = Crew(
        agents=[screening_agent],
        tasks=[screening_task],
    )
    topics_list = ["Redshift, Glue, S3"]
    topics = ', '.join(topics_list)

    result = crew.kickoff(
        inputs={"topics": topics}
    )

    with open('output.md', 'w') as f:
        f.write(result.raw)
    
if __name__ == "__main__":
    main()
```

Note that in the crew kickoff method, we are passing topics as input which we saw was referred to in both agent and tool configuration. In the code above we are trying to pass the topics as `Redshift, Glue, S3` which would be passed to the task and then to the agent, to retreive the questions and answers, we need for screening, the output is finally saved in a markdown file mentioned. Let's try runnig it with `uv run main.py`.
![Screenshot of cli output](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0rd44e7qjfzhrpyk1sif.png)

Here is a preview of the markdown generated.
![Markdown preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tqtmorbol094otk0ttuh.png)

So that's the end of this post, hope it was beginner friendly, and we just navigated some fundamentals of CrewAI, we could explore further on this such as passing the topics via user input, build multi tool based agents, add tools, mcp, rag and see options for integrating it with UI based tools for day to day use. Thank you for reading!!!
