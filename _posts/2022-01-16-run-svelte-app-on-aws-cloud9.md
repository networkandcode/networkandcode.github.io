---
canonical_url: https://dev.to/aws-builders/run-svelte-app-on-aws-cloud9-4j5b
categories: aws, cloud, solidjs, svelte
date: 2022-01-16
tags: aws, cloud, solidjs, svelte
title: Run Svelte/Solid app on AWS Cloud9
---

*This post first appeared on [dev.to](https://dev.to/aws-builders/run-svelte-app-on-aws-cloud9-4j5b)


Hey all :wave:, let's say you do not have a system with sufficient memory / CPU, to write code on IDE and then subsequently test / run it, or if you want to test code on a Linux instance such as Ubuntu/Amazon Linux2, or may be you  just keep things related to development isolated and you don't want to mess around with your machine, you could then leverage the online IDE offered by [AWS Cloud9](https://aws.amazon.com/cloud9/) to overcome all such restrictions and also use it's preview functionality, to test the app right there. Your work is also saved, and the associated instance gets terminated if it's idle based on the cost savings duration set.

You could also access other AWS services right from AWS Cloud9 too. I've been liking :green_heart:Cloud9 so far, and in this post I would just show how to setup and run the Svelte boilerplate, and then preview it on Cloud9. Svelte as most are aware is quite popular these days, seems a bit easy/fun to learn too.

Let's get started, by launching AWS cloud9. Search for Cloud9 on the AWS console, which should look like:
![Cloud9 console](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r5m6ijj6b5lepar0p1js.png)

And then create a new environment
![Create cloud9 environment](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rfgozetw1wvo3y7qkwmh.png)
 
Give it some name
![Cloud9 environment name](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/crcdqjdjknmo8zd99z6c.png)
  
I left all the other settings to be default, you may modify as required. The default settings in my case should launch an evironment with the following details:
- Name: cloud9-svelte
- Description: No description provided
- Environment type: EC2
- Instance type: t2.micro
- Platform: Amazon Linux 2 (recommended)
- Cost-saving settings: After 30 minutes (default)
- IAM role: AWSServiceRoleForAWSCloud9 (generated)

Note that Cloud9 only offers 3 platforms for now, to choose from.
![Choice of Linux platforms](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yq34e4tr133uawepn1ct.png)
 
The environment get's created in a while, once the create button is clicked.
![Create cloud9 environment](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k6k3mzhmeyo0mpqgqn49.png)

There should be a bash terminal on which I am now going to run certain commands.
![Bash on cloud9](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4kq9aodiycjojoo65qdb.png)

You can just drag the tiny bash window to the top and close other tabs that are not required.

Let's use degit as menitoned in the [Svelte](https://svelte.dev/blog/the-easiest-way-to-get-started) quick start guide, to bootstrap the svelte project.
```
nc:~/environment $ npx degit sveltejs/template my-svelte-project
Need to install the following packages:
  degit
Ok to proceed? (y) y
> cloned sveltejs/template#HEAD to my-svelte-project
npm notice 
npm notice New minor version of npm available! 8.1.2 -> 8.3.1
npm notice Changelog: https://github.com/npm/cli/releases/tag/v8.3.1
npm notice Run npm install -g npm@8.3.1 to update!
npm notice 
```
We can acknowledge the npm notice and update npm, if required.
```
nc:~/environment $ npm install -g npm@8.3.1

removed 8 packages, changed 38 packages, and audited 215 packages in 3s

10 packages are looking for funding
  run `npm fund` for details

3 moderate severity vulnerabilities

To address all issues, run:
  npm audit fix

Run `npm audit` for details.
```

Change to the project directory and then install the node modules.
```
nc:~/environment/my-svelte-project $ npm i

added 97 packages, and audited 98 packages in 6s

7 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```
Excellent, npm found no vulnerabilities.

Well, that's it run the Svelte app.
```
nc:~/environment/my-svelte-project $ npm run dev

                                                > svelte-app@1.0.0 dev
> rollup -c -w

rollup v2.64.0
bundles src/main.js → public/build/bundle.js...
LiveReload enabled
created public/build/bundle.js in 487ms

[2022-01-16 09:39:48] waiting for changes...

> svelte-app@1.0.0 start
> sirv public --no-clear "--dev"


  Your application is ready~! 🚀

  - Local:      http://localhost:8080
  - Network:    Add `--host` to expose

────────────────── LOGS ──────────────────

```
Make a note that it's running on port 8080, based on the output above.

Let's see if the app is working by using the curl command. press ALT T to open a new bash terminal. On the new terminal, execute the following command.
```
nc:~/environment $ curl localhost:8080
<!DOCTYPE html>
<html lang="en">
<head>
        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width,initial-scale=1'>

        <title>Svelte app</title>

        <link rel='icon' type='image/png' href='/favicon.png'>
        <link rel='stylesheet' href='/global.css'>
        <link rel='stylesheet' href='/build/bundle.css'>

        <script defer src='/build/bundle.js'></script>
</head>

<body>
</body>
</html>
```

So, we verified the app is working through the CLI:black_circle:. We can now try it on the browser. Hit Preview > Preview Running Application on the top bar. Boom:boom:, you should see the Svelte app on the preview browser tab. ![Preview on cloud9](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/c9lbskl5qric902u7isy.png)

This is so far, local preview, what if you want to view it from the Internet:globe_with_meridians:, or let's say your friends want to view your app over the  Internet while you are developing it. Let's exactly see that now,  let's get the instance's public IP.
```
nc:~/environment $ curl https://checkip.amazonaws.com
<cloud9-instance-public-ip>
```

We have to now modify the security  group, for which we can visit the EC2 instances page on AWS console, and select our instance id.

And then click on the Security group name in the Security tab. You can edit the inbound rules here.
![Edit inbound rules](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tcacd3dnul70c0hhwmle.png)

A rule can be added to allow port 8080, from your local machine.
![Add inbound rule](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/olpi2ku7n3mls19wgm7w.png)

Optionally, you can also add other source IPs, its always better to restrict traffic to minimal and known sources instead of applying rule for a broader range or subnet.

Save rules and you are done.
![Save rules](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/sncjdx0l92fz0bc0xtw5.png)

Let's stop the npm process by hitting Ctl C. And then run it again by prepending HOST=0.0.0.0. [Here](https://stackoverflow.com/questions/63255453/running-svelte-dev-on-server) is why.
```
nc:~/environment/my-svelte-project $ HOST=0.0.0.0 npm run dev

> svelte-app@1.0.0 dev
> rollup -c -w

rollup v2.64.0
bundles src/main.js → public/build/bundle.js...
LiveReload enabled
created public/build/bundle.js in 476ms

[2022-01-16 10:22:50] waiting for changes...

> svelte-app@1.0.0 start
> sirv public --no-clear "--dev"


  Your application is ready~! 🚀

  - Local:      http://0.0.0.0:8080
  - Network:    http://172.31.4.12:8080

────────────────── LOGS ──────────────────

```

If you now try to visit the Cloud9 instance's public IP on the browser, from your local machine, over port 8080, it should work.
![Svelte app on browser](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ta0aq86s7zpobhn5v0w6.png)
 

That's for the post, so you can make use of the online IDE offered by AWS Cloud9 and develop apps on the go. Thanks for reading !!! 

Update:
You can run [solid.js](https://docs.solidjs.com/guides/getting-started-with-solid/installing-solid) apps the same way. You can try the following commands:
```
npx degit solidjs/templates/ts my-app
cd my-app
npm  i
npm run dev -- --host --port 8080
```
![solid.js on Cloud9](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wziqv36qeiqtmy2geo4y.png)