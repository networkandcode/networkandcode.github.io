---
canonical_url: https://dev.to/aws-builders/serverless-backend-setup-for-a-todo-list-in-aws-189l
categories: api, aws, lambda, serverless
date: 2022-04-10
tags: api, aws, lambda, serverless
title: Serverless backend setup for a todo list in AWS
---

*This post first appeared on [dev.to](https://dev.to/aws-builders/serverless-backend-setup-for-a-todo-list-in-aws-189l)

Hello :wave:, in this post :pencil: we are going to build a simple backend for a todo application using [AWS services](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-dynamo-db.html) :cloud: such as AWS API Gateway, AWS Lambda and AWS DynamoDB.

Starting with DynamoDB, we are gonna setup a table with **task** as the hash / partition key:key:. This table is a simple one with four fields task, description, date and done(binary). We don't have to specify all the fields while creating the table though except the hash key, the fields could be created dynamically while we add data to the table.
![Create database table](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yj1d4ffdu3w6a6out7x7.png)

Leave rest of the settings to the default and create the table.

Next, lets go to IAM and create a policy :page_with_curl:  which would allow CRUD operations on our DynamoDB table todo. I have set CrudOhioDynamoTodoTable as the policy name as Ohio(us-east-2) is the region where the table was created. You may visit this [site](https://awspolicygen.s3.amazonaws.com/policygen.html) to generate policies:vertical_traffic_light:. The policy json is as follows.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "dynamodb:DeleteItem",
                "dynamodb:GetItem",
                "dynamodb:PutItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:dynamodb:us-east-2:<account-id>:table/todo"
        }
    ]
}
```
![IAM policy created](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/26fk2vndj89uuf9gnyl8.png)

We have to now create a role and attach this policy.
![IAM role creation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/s6273406ti326dfl8in4.png)

Select the use case as Lambda and on the next page select the policy we have created.
![Attach roleto policy](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/52zj0qkfwd508w8lzdxn.png)

Choose a name for the Role, for ex. LambdaToCrudOhioDynamoTodoTable, and finally create the role.
![Role created](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/g7tdh4i7ppa7m4zvjhk2.png)

*Progress so far: Lambda service role > Crud Policy > DynamoDB*
  
So the IAM part is done, we are good to create the Lambda function now and attach the role to it. Just set a function name (ex. todo) and set the execution role to the role we created. Rest of the settings can be default.
![Create Lambda function](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/siv5t09on1n037oaycpp.png)
 

Replace the code in index.js with the following and deploy the function.
```
const AWS = require("aws-sdk");

const dynamo = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event, context) => {
  let body;
  let statusCode = 200;
  const headers = {
    "Content-Type": "application/json"
  };

  try {
    switch (event.routeKey) {
      case "DELETE /tasks/{task}":
        await dynamo
          .delete({
            TableName: "todo",
            Key: {
              task: event.pathParameters.task
            }
          })
          .promise();
        body = `Deleted task ${event.pathParameters.task}`;
        break;
        
      case "GET /tasks/{task}":
        body = await dynamo
          .get({
            TableName: "todo",
            Key: {
              task: event.pathParameters.task
            }
          })
          .promise();
        break;
        
      case "GET /tasks":
        body = await dynamo.scan({ TableName: "todo" }).promise();
        break;
        
      case "PUT /tasks":
        let requestJSON = JSON.parse(event.body);
        await dynamo
          .put({
            TableName: "todo",
            Item: {
              task: requestJSON.task,
              description: requestJSON.description,
              date: requestJSON.date,
              done: requestJSON.done ? true : false
            }
          })
          .promise();
        body = `New task added: ${requestJSON.task}`;
        break;
        
      default:
        throw new Error(`Unsupported route: "${event.routeKey}"`);
    }
  } catch (err) {
    statusCode = 400;
    body = err.message;
  } finally {
    body = JSON.stringify(body);
  }

  return {
    statusCode,
    body,
    headers
  };
};
```

Ok so our Lambda function is ready.
Lambda Function > Lambda Role > Crud Policy > Dynamo DB

What's next, something should invoke the Lambda, which is our API. Let's create a single API gateway with relevant API methods.

Go to API gateway on the console, and create an HTTP API with lambda integration.
![Create API gateway](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gknwx8qp3woq2z5ifx8r.png)
 
And next the routes.
![Configure API gateway routes](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0m4jxjiz3mfp6sxnqlcq.png)

The gateway can be created with other prompts set to default values.
![API gateway created](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mrd7qyfcgyprtnlh8mnh.png)
 
Make a note of the execution URL, as that would be used to make API calls.

I am going to better set it as an environment variable, so that I don't have to keep typing the longer URL for the rest of the post.
```
$ executionURL=https://j6yotbi8ta.execute-api.us-east-2.amazonaws.com
```

Hmm ok, so I think our backend is kinda setup now with this.
API gateway > Lambda Function > Lambda Role > CRUD policy > DynamoDB

Let's try making some calls and see if it actually works.
```
$ curl -X PUT ${executionURL}/tasks -H "Content-Type: application/json" -d '{                        
"task": "BuyBooks",
"description": "Buy Java and System Design books from Amazon",
"date": "10-Apr-2022"
}'
"New task added: BuyBooks"

 $ curl -X PUT ${executionURL}/tasks -H "Content-Type: application/json" -d '{
"task": "ShutEC2Instances",
"description": "Shut down the unused EC2 instances to avoid billing",                                      
"date": "10-Apr-2022"              
}'
"New task added: ShutEC2Instances"
```
We were able to successfully add couple new tasks with the PUT method.

Let's retrieve all items from the DB table.
```
$ curl --silent ${executionURL}/tasks | jq                                                            
{
  "Items": [
    {
      "date": "10-Apr-2022",
      "task": "ShutEC2Instances",
      "description": "Shut down the unused EC2 instances to avoid billing",
      "done": false
    },
    {
      "date": "10-Apr-2022",
      "task": "BuyBooks",
      "description": "Buy Java and System Design books from Amazon",
      "done": false
    }
  ],
  "Count": 2,
  "ScannedCount": 2
}
```

And now, retrieve items based on the primary key which in our case is task.
```
$ curl --silent ${executionURL}/tasks/BuyBooks | jq
{
  "Item": {
    "date": "10-Apr-2022",
    "task": "BuyBooks",
    "description": "Buy Java and System Design books from Amazon",
    "done": false
  }
}

$ curl --silent ${executionURL}/tasks/ShutEC2Instances | jq                                               
{
  "Item": {
    "date": "10-Apr-2022",
    "task": "ShutEC2Instances",
    "description": "Shut down the unused EC2 instances to avoid billing",
    "done": false
  }
}
```
Lets make couple changes to the tasks. For the first one Java is replaced with JavaScript, and the second one I'm setting done as true.
```
$ curl -X PUT https://j6yotbi8ta.execute-api.us-east-2.amazonaws.com/tasks -H "Content-Type: application/json" -d '{
"task": "BuyBooks",
"description": "Buy JavaScript and System Design books from Amazon",                                                                                  
"date": "10-Apr-2022"
}'
"New task added: BuyBooks"

$ curl -X PUT https://j6yotbi8ta.execute-api.us-east-2.amazonaws.com/tasks -H "Content-Type: application/json" -d '{
"task": "ShutEC2Instances",
"description": "Shut down the unused EC2 instances to avoid billing",
"date": "10-Apr-2022", "done": "true"
}'
"New task added: ShutEC2Instances"
```
The put method either creates a new item, or replaces an existing item, which I think is fine in  our case as our table is kinda small. Let's view the contents one more time.
```
$ curl --silent https://j6yotbi8ta.execute-api.us-east-2.amazonaws.com/tasks | jq                                                                
{
  "Items": [
    {
      "date": "10-Apr-2022",
      "task": "ShutEC2Instances",
      "description": "Shut down the unused EC2 instances to avoid billing",
      "done": true
    },
    {
      "date": "10-Apr-2022",
      "task": "BuyBooks",
      "description": "Buy JavaScript and System Design books from Amazon",
      "done": false
    }
  ],
  "Count": 2,
  "ScannedCount": 2
}
```
The value for "done" is boolean though we have set it as string while executing the curl command, this is due to the following code in Lambda function.
```
done: requestJSON.done ? true : false
```

Finally, the delete method.
```
$ curl  -X DELETE ${executionURL}/tasks/ShutEC2Instances                                                                                                    "Deleted task ShutEC2Instances"

$ curl  -X DELETE ${executionURL}/tasks/BuyBooks
"Deleted task BuyBooks"
```
So we have been sending unauthenticated calls from CURL. For some security, we can add IAM authorizer to all the routes.
![Attach IAM authorizer to routes](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lalpa3xvyywtcxmxpz2a.png)
 
With this, we shouldn't be able to make calls like before, we should now be authenticated and authorized.
```
$ curl ${executionUrl}/tasks |  jq                                                                                       
curl: (3) URL using bad/illegal format or missing URL
```

Let's use [postman](https://aws.amazon.com/premiumsupport/knowledge-center/iam-authentication-api-gateway/) as its easy to send requests from it with AWS signature.
![Get request in postman](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/u7yrm39qwgy29518jbdc.png)

The IAM user whose credentials are entered should have permissions to send API calls to the API gateway. In my case the user id has admin permissions and hence it works good.
![Response in postman](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2l25a4c2ci07jjfz3hwz.png)

Well that's it for this post.. :thumbsup: So we saw how to setup the backend for a mini todo application with API gateway, Lambda and IAM. And we tested it with a few API calls via CURL(with out authentication) and Postman(with IAM authentication).

But what's pending, we could have some sort of a web frontend that could send API calls to the API gateway using client libraries such as fetch, axios etc.  just like CURL / Postman did it for us from the CLI / Desktop, thus  resulting in a proper web application...

Thanks for reading !!! Don't forget to delete the resources you have created, if they are no longer in use :)