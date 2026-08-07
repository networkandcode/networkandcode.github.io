---
canonical_url: "https://dev.to/aws-builders/mcp-with-amazon-q-cli-ac9"
date: "2025-05-06"
title: "GitHub MCP with Amazon Q CLI"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fjlb6iwqht4njpfl51jf3.webp"
tags: "aws, mcp, github, nextjs"
categories: "aws, mcp, github, nextjs"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/mcp-with-amazon-q-cli-ac9)**

Hi :wave:, let's explore some MCP stuff with the amazon q developer cli. We shall try onboarding a new nextjs app with boilerplate code on GitHub in this exercise. We then just clone the code to our machine and run it locally. Let's get started :rocket:

Install the q [cli](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html).
```
brew install amazon-q
```
Once installed open Amazon Q from the launchpad and follow the instructions there to integrate Q with shell, and then login with a builder ID.

Let's create a directory where we can keep our mcp code.
```
mkdir app-onboarding-with-q
cd app-onboarding-with-q 
```

## GitHub MCP server
We can now add the [github](https://github.com/github/github-mcp-server) mcp config.

Create a personal access token on github developer settings with access to `All repositories` and read and write permissions for `Administration` and `Content`.
![GitHub token permissions](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mp6j0y0ntlzj1s16j12v.png)


Add the mcp configuration in the directory on the file `.amazonq/mcp.json`.
```
{
    "mcpServers": {
      "github": {
        "command": "docker",
        "args": [
          "run",
          "-i",
          "--rm",
          "-e",
          "GITHUB_PERSONAL_ACCESS_TOKEN",
          "ghcr.io/github/github-mcp-server"
        ],
        "env": {
          "GITHUB_PERSONAL_ACCESS_TOKEN": "<your-github-pat>"
        }
      }
    }
}
```

Start the docker engine on your machine as the github mcp server defined above needs docker.

Launch `q` from the cli.
```
$ q
```

You should see that the mcp server is launched.
```
✓ github loaded in 0.33 s
✓ 1 of 1 mcp servers initialized
```

This should have started a docker container for us.
```
$ docker ps | grep github
76ff6beb314c   ghcr.io/github/github-mcp-server              "./github-mcp-server…"   26 seconds ago   Up 26 seconds                                                                                                   stupefied_heyrovsky
```

On the q-prompt if you enter `/tools` you should see the available tools including the MCP tools. Here is a glimpse.
```
github (MCP):
- github___search_issues                      * not trusted
- github___get_pull_request_reviews           * not trusted
- github___get_code_scanning_alert            * not trusted
- github___create_pull_request_review         * not trusted
```

There are certain built in tools as well, other than the mcp tools we installed.
```
Built-in:
- execute_bash    * trust read-only commands
- fs_write        * not trusted
- use_aws         * trust read-only commands
- fs_read         * trusted
- report_issue    * trusted
```

Let's create a nextjs boilerplate app.
```
> create a new repo in github with name nextjs-new-app and put nextjs bolierplate code in it, with the github mcp server
```

For brevity, Iam not going to copy the complete response, but we will see some key details from it. First, it will try to create a repo and ask us for confirmation.
```
🛠️  Using tool: create_repository from mcp server github
Allow this action? Use 't' to trust (always allow) this tool for the session. [y/n/t]:
```

We can press `y` to confirm. The repo is now created :fire:.
![New repo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pmjbn18o1c6bs33otz2l.png)

Note that we could also trust the tool by pressing `t`, however it's better to confirm actions for now(human in the loop), so that we are sure what the action would do.

Let's continue...

Amazon Q would then try to push multiple files to our repo.
```
🛠️  Using tool: push_files from mcp server github
```

Press `y` again after the which the files are all there.

![Repo with files](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5yy5xo2upur6nz7lpwbm.png)

## Run the app locally
Let's once try to run the app locally and see if it's all working, for which we have to clone it.
```
> clone the repo you just created and run the app
🛠️  Using tool: execute_bash
```

It will then try to do a few actions with the `execute_bash` tool.
```
 ● I will run the following shell command: 
cd /Users/networkandcode/app-onboarding-with-q && git clone https://github.com/networkandcode/nextjs-new-app.git

 ● I will run the following shell command: 
cd /Users/networkandcode/app-onboarding-with-q/nextjs-new-app && npm install

 ● I will run the following shell command: 
cd /Users/networkandcode/app-onboarding-with-q/nextjs-new-app && npm run dev
```

The app should have now started.
```
> y

> nextjs-new-app@0.1.0 dev
> next dev

 ⚠ Port 3000 is in use, trying 3001 instead.
  ▲ Next.js 14.2.28
  - Local:        http://localhost:3001

 ✓ Starting...
 ✓ Ready in 2.7s
```

We can try accessing `http://localhost:3001` as shown above.
![App running locally](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/fkl13twnjzgvqbbvslmb.png)

We can press ctrl c when done, so that we are back to the q prompt.
We can type `/quit` or `/exit` on the q-prompt anytime to exit.

Let's modify our code
```
> modify the code in the nextjs repo networkandcode/nextjs-new-app to show an analog clock on the home page with utc +5.30 time, note that it is written in typescript and has the src folder
```

It first tries to read the existing contents `🛠️  Using tool: get_file_contents from mcp server github`. Note that I resumed this exercise a bit later so had to give some extra context.

And then it would try to update files `🛠️  Using tool: create_or_update_file from mcp server github`

If we try running it again we should see the clock. Note that I have given a few more prompts to modify code.

![Homepage showing clock](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/sft9vbghqapf28duvfa0.png)

As next steps we could try deploying this app on platforms such as AWS Amplify(I think there is no MCP server as of this writing for Amplify deployments). Also, usually we write code first on the local system(we could use the [filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) mcp for that) and then push it to the git repo, however in this blog we tried the other way round.
