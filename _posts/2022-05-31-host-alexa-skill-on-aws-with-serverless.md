---
canonical_url: https://dev.to/aws-builders/setup-an-alexa-skill-with-serverless-1gck
categories: alexa, aws, node, serverless
date: 2022-05-31
tags: categories: alexa, aws, node, serverless
title: Host Alexa skill on AWS with Serverless
---

*This post first appeared on [dev.to](https://dev.to/aws-builders/setup-an-alexa-skill-with-serverless-1gck)*

Hey all :wave: we are gonna see how to setup an Alexa skill for a  trivia related to space events, using the [Serverless](https://serverless.com) framework. It's assumed you are ok with  some Alexa fundamentals and certain concepts of AWS such as IAM, Lambda etc. Let's get started.

You  may go through this nice [tutorial](https://developer.amazon.com/en-US/docs/alexa/workshops/build-an-engaging-skill/get-started/index.html) if you want to get started with Alexa by building an Alexa hosted skill. What we have done here in this blog is an AWS hosted skill.

## Alexa
Login to the Alexa skill kit [console](https://developer.amazon.com/alexa/console/ask) with your developer account.

You can then create a skill and give it some invocation name.
![Skill invocation name](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nl9hd8xcz26tiw2w8x8g.png)

### Intents 
I've addedd 2 built-in intents and 2 custom intents, than what gets added by default.
![Added intents](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tdpe0j1y4ty8i4nfdkau.png)

The GetAnswerIntent has the following utterances.
```
it's {date}
I guess it's on {date}
I think the date is {date}
{date}
I'm guessing it's {date}
```
You may add more or modify as you wish. The only slot here is `date` and it is of built-in type AMAZON.DATE.

Likewise the AskQuestionIntent has the following utterances.
```
could you ask me the question please
can you go back to the question
can you ask me the question
question please
go back to the question
next question
Ask question
```
Ensure to save and build the model once all the intents are added.

## IAM 
Log in to [AWS](https://console.aws.amazon.com) as a root user, and create a user group
![Create group](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ekfw77ben31bnw3o66vw.png)

The user group should be attached by the AWS managed permission policy [AWSCloud9User](https://console.aws.amazon.com/iam/home#/policies/arn:aws:iam::aws:policy/AWSCloud9User) that allows creating Cloud9 environments. This is not required though, if you are not using Cloud9.

I've then created another custom [policy](https://us-east-1.console.aws.amazon.com/iamv2/home#/policies) with the following [JSON](https://www.serverless.com/framework/docs/guides/providers#using-a-custom-iam-role-and-policy), with the name `ServerlessPolicy` that gives enough permissions for the serverless SDK to deploy using cloud formation stack, and access to other relevant services as listed.
``` 
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "apigateway:DELETE",
                "apigateway:GET",
                "apigateway:PATCH",
                "apigateway:POST",
                "apigateway:PUT",
                "cloudformation:CreateChangeSet",
                "cloudformation:CreateStack",
                "cloudformation:DeleteChangeSet",
                "cloudformation:DeleteStack",
                "cloudformation:DescribeChangeSet",
                "cloudformation:DescribeStackEvents",
                "cloudformation:DescribeStackResource",
                "cloudformation:DescribeStacks",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:ListStackResources",
                "cloudformation:UpdateStack",
                "cloudformation:ValidateTemplate",
                "events:DescribeRule",
                "events:PutRule",
                "events:PutTargets",
                "events:RemoveTargets",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:DeleteRolePolicy",
                "iam:GetRole",
                "iam:PassRole",
                "iam:PutRolePolicy",
                "iam:UpdateAssumeRolePolicy",
                "lambda:AddPermission",
                "lambda:CreateFunction",
                "lambda:DeleteFunction",
                "lambda:GetAccountSettings",
                "lambda:GetAlias",
                "lambda:GetEventSourceMapping",
                "lambda:GetFunction",
                "lambda:GetFunctionConfiguration",
                "lambda:GetLayerVersion",
                "lambda:GetLayerVersionPolicy",
                "lambda:GetPolicy",
                "lambda:InvokeFunction",
                "lambda:ListAliases",
                "lambda:ListEventSourceMappings",
                "lambda:ListFunctions",
                "lambda:ListLayerVersions",
                "lambda:ListLayers",
                "lambda:ListTags",
                "lambda:ListVersionsByFunction",
                "lambda:PublishVersion",
                "lambda:RemovePermission",
                "lambda:UpdateFunctionCode",
                "lambda:UpdateFunctionConfiguration",
                "logs:CreateLogGroup",
                "logs:DeleteLogGroup",
                "logs:DeleteSubscriptionFilter",
                "logs:DescribeLogGroups",
                "logs:FilterLogEvents",
                "logs:GetLogEvents",
                "logs:PutSubscriptionFilter",
                "s3:CreateBucket",
                "s3:DeleteBucket",
                "s3:DeleteBucketPolicy",
                "s3:DeleteBucketWebsite",
                "s3:DeleteObject",
                "s3:DeleteObjectVersion",
                "s3:GetBucketLocation",
                "s3:GetObject*",
                "s3:ListBucket",
                "s3:PutBucketPolicy",
                "s3:PutEncryptionConfiguration",
                "s3:PutObject",
                "sts:GetCallerIdentity"
            ],
            "Resource": "*"
        }
    ]
}
```

So the group is attached to both policies.
![Group permission policies](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y1og68nmzwtb4achexfd.png) 

Once the group is created, add a new user to the group.
![Add user to the group](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vuwunoyeivw48k2dmmyd.png)

And don't forget to copy the credentials

## Instance
You may now login to AWS as the new user. Next we need a machine from which we can clone the serverless code and deploy it, for this purpose I would be launching a [cloud 9](https://dev.to/aws-builders/run-svelte-app-on-aws-cloud9-4j5b) instance, so that I can also use it as an online editor. You can use any Linux machine though.

I'd be creating a Cloud9 environment in the Mumbai region, ap-south-1.
![Launch cloud9](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/eo0ry9tumj2ywurzdpm3.png)
I've choosen t3.small as the instance type, we may go with t2.micro if we want a free tier eligible instance.

Once it's created you shoud see the console.
![Cloud9 environment console](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n1ilc88c89ho82sfjd6a.png)

## AWS CLI
AWS CLI comes pre-installed in Cloud9 and it would also have the credentials file
```
serverless-user-1:~/environment $ ls ~/.aws/
credentials
```
We can setup the config though.
```
serverless-user-1:~/environment $ cat ~/.aws/config 
[default]
region=ap-south-1
```

## Clone
Let's clone the alexa skill repo [space-events-trivia](https://github.com/networkandcode/space-events-trivia) from github.
```
serverless-user-1:~/environment $ git clone https://github.com/networkandcode/space-events-trivia.git
``` 
The code we cloned is a set of nodejs functions and is compatible with the serverless sdk.
```
serverless-user-1:~/environment $ cd space-events-trivia/
serverless-user-1:~/environment/space-events-trivia (main) $ ls
AplRender.js                   GetAnswerIntentHandler.js  interceptors.js          README.md                      StartTriviaHandler.js
CancelAndStopIntentHandler.js  HelpIntentHandler.js       LaunchRequestHandler.js  RepeatIntentHandler.js         triviaFunctions.js
documents                      index.js                   package.json             serverless.yml
ErrorHandler.js                IntentReflectorHandler.js  package-lock.json        SessionEndedRequestHandler.js
```

The file [documents/questions.json](https://github.com/networkandcode/space-events-trivia/blob/main/documents/questions.json) contains the list of questions for the trivia, you may modify it as required.

## Packages
The package.json file should tell us the packages we would be using in our code.
![package.json](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/36jrhbpnxpjml3jxfscd.png)

Let's install those.
```
serverless-user-1:~/environment/space-events-trivia (main) $ npm i
npm WARN deprecated querystring@0.2.0: The querystring API is considered Legacy. new code should use the URLSearchParams API instead.
npm WARN deprecated uuid@3.3.2: Please upgrade  to version 7 or higher.  Older versions may use Math.random() in certain circumstances, which is known to be problematic.  See https://v8.dev/blog/math-random for details.

added 18 packages, and audited 19 packages in 2s

1 package is looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

## Serverless
We can install the serverless SDK and later deploy the code using it to AWS lambda. We are actually talking about two things here, one the serverless framework/SDK, and two the serverless technology offering from AWS which is Lambda. Instead of writing the functions directly on Lambda we are going to use the serverless SDK with it's constructs to acheieve the purpose in a controlled way.
```
serverless-user-1:~/environment $ npm i serverless -g
```
It should now be installed.
```
serverless-user-1:~/environment $ serverless -v
Framework Core: 3.18.2
Plugin: 6.2.2
SDK: 4.3.2
```
There is a serverless.yml file in  our repo, that has our serverless [configuration](https://www.serverless.com/framework/docs/providers/aws/guide/serverless.yml), you may modify it according to your setup.
```
serverless-user-1:~/environment/space-events-trivia (main) $ cat serverless.yml 
app: space-events-trivia
service: space-events-trivia

frameworkVersion: '3'

provider:
  environment:
    DYNAMODB_REGION: ${aws:region}
    DYNAMODB_TABLE: ${self:service}-users-${sls:stage}
  iam:
    role:
      statements:
      - Effect: 'Allow'
        Action:
        - 'dynamodb:CreateTable'
        - 'dynamodb:PutItem'
        - 'dynamodb:Get*'
        - 'dynamodb:Scan*'
        - 'dynamodb:UpdateItem'
        - 'dynamodb:DeleteItem'
        Resource: arn:aws:dynamodb:${aws:region}:${aws:accountId}:table/${self:service}-users-${sls:stage}
  name: aws
  region: ap-south-1
  runtime: nodejs16.x
  stage: dev

functions:
  handler:
    handler: index.handler
    events:
    - alexaSkill: amzn1.ask.skill.${param:alexaSkillId}
```
The org is missing in the configuration, we can specify that while deploying. We have also given permissions for the lambda function on DynamoDB incuding the create table permission, so that the lambda function can create the table if it doesn't exist.

## Deploy
Let's deploy the function, for which first login to serverless.
```
$ serverless login
? Which would you like to log into? Serverless Framework Dashboard
Logging into the Serverless Dashboard via the browser
If your browser does not open automatically, please open this URL:
https://app.serverless.com?client=cli&transactionId=<some-id>
```
Once logged in via the browser, you should see this screen.
![Serverless logged in](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5ga38coaffss3am7cm3m.png)

That's it, time to deploy.
```
$ serverless deploy --org <your-org> --param="alexaSkillId=<id>"
```
You have to mention your org and alexaSkillId before running the command above.  The org name is something you created in  serverless while signing up the account, and you can get the skill ID from the alexa developer console, so that it gets mapped with `alexaSkill: ${param:alexaSkillId}` in [serverless.yml](https://github.com/networkandcode/space-events-trivia/blob/main/serverless.yml)
![Copy skill id](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/op4lygzb3faoxw7tqj85.png) 

The function should get successfully deployed by now. The serverless dashboard should show a successful status with green color.
![Service deployed](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wnmy9bgr9lld3bfbh9yx.png)

## Endpoints
You can get the lambda endpoint straight from the Serverless CLI.
```
$ serverless info --param="alexaSkillId=<your-skill-id>" --verbose
service: space-events-trivia
stage: dev
region: ap-south-1
stack: space-events-trivia-dev
functions:
  handler: space-events-trivia-dev-handler

Stack Outputs:
  HandlerLambdaFunctionQualifiedArn: <lambda-arn>
  EnterpriseLogAccessIamRole: <role-name>  
  ServerlessDeploymentBucketName: <bucket-name>

Want to ditch CloudWatch? Try our new console: run "serverless --console"
```
You can copy the lambda ARN from the output above except the suffix which is a number, and set it as an endpoint in the Skill settings in Alexa developer console. It should have the format `arn:aws:lambda:<region>:<account-id>:function:<function-name>`. I've just added it for the default region.
![Set endpoint](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y68ygulez2hykdejg0il.png)

The skill could now be tested from the test window.
![Skill test](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/24s9oh4zxftkufnpnskn.png)

You can also test :test_tube: the skill from an Alexa device that's using the same account as your developer account.

Alright then, that's it for now, thanks for reading !!!

Image credit: [unsplash](https://source.unsplash.com/featured/?galaxy)