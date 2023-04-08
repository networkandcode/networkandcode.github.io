---
canonical_url: https://dev.to/networkandcode/query-harperdbs-rest-api-via-apollo-graphql-21n1
date: 2023-02-17
title: Query HarperDB's REST API via Apollo GraphQL
categories: apolloserver, graphql, harperdb, rest
cover_image: https://source.unsplash.com/featured/?coding
tags: apolloserver, graphql, harperdb, rest
---

**This post first appeared on [dev.to](https://dev.to/networkandcode/query-harperdbs-rest-api-via-apollo-graphql-21n1)
## Introduction
Hi there :wave:, in this post, we shall launch an Apollo server with node, 
and perform some read & write operations from the Apollo studio sandbox to 
a HarperDB instance. Having some graphql fundamentals would be beneficial 
to understand better, though some parts of the code would be explained.

## Studio
I have an account in HarperDB [studio](https://studio.harperdb.io) and 
have setup an organisation and a free trier instance there. Once logged in 
to the instance, the config tab would give the instance credentials we 
would need to connect from our code.
![Instance 
config](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ou6rpws6ql4of4hqi773.png)


Note that the studio credentials(email/password) are different from the 
instance credentials(username/password). You can have more than one 
instance in the studio. You can have only one free tier instance though 
across organisations.

Copy the instance url and the basic token from the config shown in the 
image above, as we would need those while sending API calls.

## Clone
Clone the code from GitHub.
```
$ git clone git@github.com:networkandcode/fruits-apollo-hdb.git
```

## Dependencies
The 
[dependencies](https://github.com/networkandcode/fruits-apollo-hdb/blob/main/server/package.json#L13-L18) 
for the code are as follows.
```
  "dependencies": {
    "@apollo/datasource-rest": "^5.0.2",
    "@apollo/server": "^4.3.3",
    "dotenv": "^16.0.3",
    "graphql": "^16.6.0"
  }
```

We can install these.
```
$ npm i
```

About the packages above: 
- `@apollo/datasource-rest` is used to make rest api calls from apollo to 
endpoints such as HarperDB's instance url.
- `@apollo/server` is used to launch the apollo server itself.
- `dotenv` is used to read env vars.
- `graphql` is the core graphql library.

You may refer to this 
[guide](https://www.apollographql.com/docs/apollo-server/getting-started/#step-2-install-dependencies) 
for more info.

## Variable
Add an `.env` file, we just need one variable.
```
$ cat .env
HDB_INSTANCE_URL=https://<instance-name>.harperdbcloud.com
```

## Start
There is a start script with invokes the index file.
```
$ cat package.json| grep start
    "start": "node index.js"
```

Good to start the server
```
$ npm start

> server@1.0.0 start
> node index.js

🚀  Server ready at: http://localhost:4000/
```

## Apollo studio
Once the server is started we should be able to see the sandbox studio on 
the browser at http://localhost:4000/.
![Apollo 
studio](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y9t1050mz0k32nkiaah0.png)

## Token
Let's set the authorisation header, you may paste the basic token obtained 
from HarperDB studio here.
![Basic auth 
token](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8078w2kbat6uzcw939on.png)

We are setting this 
[token](https://github.com/networkandcode/fruits-apollo-hdb/blob/main/server/index.js#L20) 
in the server context.
```
    const token = req.headers.authorization;
```

Which would be 
[passed](https://github.com/networkandcode/fruits-apollo-hdb/blob/main/server/datasource.js#L46-L48) 
to HarperDB while the REST API call is being made.
```
    willSendRequest(_path, request) {
      request.headers['authorization'] = this.token;
    };
```

## Code
Let's see what code files we have and their purpose.
```
$ ls *.js
datasource.js   index.js        resolvers.js    schema.js
```
- `datasource.js` is where we are making calls to HarperDB via REST API.
- `index.js` has code that wraps the schema and resolvers in the server 
and starts it.
- `resolvers.js` contains resolvers that resolves all of the queries and 
mutations defined in `schema.js` by sending calls to HarperDB API defined 
in `datasource.js`
- `schema.js` contains our graphql schema that has built in types Query 
and Mutation as well as other user defined types and inputs.


### Schema
Our graphql 
[schema](https://www.apollographql.com/docs/apollo-server/schema/schema/) 
is a collection of type definitions. And hence it's common to use typeDefs 
as our schema variable.
```
$ cat schema.js 
const typeDefs = `
  input CreateTableBody {
    schema: String!
    table: String!
    hash_attribute: String!
  }

  input FruitInput {
    name: String!
    "calories per 100 gm"
    calories: Int!
  }

  type Query {
    fruits(schema: String!, table: String!): [Fruit]
    fruit(schema: String!, table: String!, name: String!): [Fruit]
  }

  type Mutation {
    createSchema(schema: String!): ApiResponse!
    createTable(body: CreateTableBody!): ApiResponse!
    insertRecords(schema: String!, table: String!, records: [FruitInput!]! 
): ApiResponse!
  }

  type Fruit {
    id: ID!
    name: String!
    calories: Int!
  }

  type ApiResponse {
    status: Int!
    message: String!
  }
`;

export default typeDefs;
```

In the schema, there are two built in types Query and Mutation. Query is 
meant for read operations where as Mutation refers to operations that 
involve create, update or deletion of data.

In Query, we have defined two fields fruits and fruit. `fruits` takes two 
arguments schema and table, both are strings and are mandatory or non 
nullable as denoted with `!`. Both fruits and fruit fields return same 
type of data denoted by [Fruit], this indicates an array of records, where 
each record is of type Fruit, this is not a built in type like String or 
Int, hence we have defined it as type Fruit. The type definition for Fruit 
denotes it’s structure, it would have three fields id, name and calories 
which are of types ID, String and Int respectively, and all 3 fields are 
non nullable. To summarise, we can have two Query operations one is fruits 
and the other is fruit both return a list of fruits(records from 
HarperDB).

Like wise for Mutation, we have three fields createSchema, createTable and 
insertRecords with their respective arguments, and all of them would 
return the same type of response as denoted by ApiResponse, that would 
have only 2 fields status and message.

Note that when a field type is not built in, we would define it with type, 
like we have defined type `Fruit` and type `ApiResponse` in our schema. 
Likewise, when an argument type is not built in, we would delete it with 
input, like we have defined input `CreateTableBody` and `FruitInput` in 
our schema. 

### Datasource
Here, we create a new class by name HdpApi that inherits from 
RESTDataSource. Note that we obtain the baseURL from the env var. 

The willSendRequest function is used to add the header while calls are 
being sent to the base url. There are just two functions we are defining 
here, as in HarperDB all the calls are of type 
[POST](https://api.harperdb.io), and there mainly two types of calls, one 
that sends SQL style statements and the other which they call as NoSQL 
operations.

```
$ cat datasource.js 
import { RESTDataSource } from '@apollo/datasource-rest'; 

class HdbApi extends RESTDataSource {
    baseURL = process.env.HDB_INSTANCE_URL;
    
    constructor(options) {
      super(options);
      this.token = options.token;
    };
  
    async sqlQuery(body) {
      // for read operations
      return await this.post(
        '',
        {
          body,
        }
      ).then((res) => {
        return res;
      })
    };
  
    async noSqlQuery(body) {
      return await this.post(
        '',
        {
          body,
        }
      ).then((res) => {
        const { message } = res;
        return {
          status: 200,
          message
        }
      }).catch((err) => {
        const { status, body } = err.extensions.response;
        const message = body.error;
  
        return {
          status,
          message
        }
      });
    };
  
    willSendRequest(_path, request) {
      request.headers['authorization'] = this.token;
    };
  
  };

  export default HdbApi;
```

### Index
In the index file, we import the modules first. And then, we import the 
schema, resolvers and our datasource. We use dotenv to read the var 
defines in `.env`.

We then create an Apollo server instance that takes two arguments: schema 
and resolvers.

We start the server finally, and we give options such as the listening 
port, and the context.

```
$ cat index.js 
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import dotenv from 'dotenv';

import typeDefs from './schema.js';
import resolvers from './resolvers.js';
import HdbApi from './datasource.js';

dotenv.config();
console.log(process.env)

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async({ req }) => {
    const { cache } = server;
    const token = req.headers.authorization;
    return {
      dataSources: {
        hdbApi: new HdbApi({ cache, token }),
      }
    }
  }
});

console.log(`🚀  Server ready at: ${url}`);
```

The context returns a dataSources dictionary that has a hdpApi key in it, 
and this points to a new HdpApi object which is defined in the datasource.

We can refer to this context in the resolvers.

### Resolvers
There are 2 main resolvers for the built in types Query and Mutation. 
Inside each resolver, we have a function for each field inside the type. 
In our schema we have defines two types fruits and fruit, hence there are 
two such functions inside the Query resolver too. Similarly we have three 
functions for the Mutations: createSchema, createTable and insertRecords. 

What these functions return will come as the result in the Apollo Studio 
for our GraphQL operation. The return statements are referring to 
contextValue which is the context function we defined in index. So, the 
resolvers are able to use the context defined in the server, which 
subsequently points to the api calls we defined in the datasource.

Note that there are four 
[arguments](https://www.apollographql.com/docs/apollo-server/data/resolvers/#resolver-arguments) 
for each function: parent, args, contextValue and info. We would only need 
the 2nd and 3rd args for this exercise though. We have already seen about 
`contextValue` above, and `args` refer to the variables we set while 
running an operation in the Apollo studio.
```
$ cat resolvers.js 
const resolvers = {
    Query: {
      fruits: (_, args, contextValue) => {
        const { schema, table } = args;
        const body = {
          "operation": "sql",
          "sql": `SELECT * FROM ${schema}.${table}`,
        }
  
        return contextValue.dataSources.hdbApi.sqlQuery(body);
      },
      fruit: (_, args, contextValue) => {
        const { schema, table, name } = args;
        const body = {
          "operation": "sql",
          "sql": `SELECT * FROM ${schema}.${table} where name = "${name}"`
        };
  
        return contextValue.dataSources.hdbApi.sqlQuery(body);
      },
    },
    Mutation: {
      // There are four args parent, args, contextValue and info
      createSchema: (_, { schema }, contextValue) => {
        const body = {
          operation: "create_schema",
          schema,
        };
  
        return contextValue.dataSources.hdbApi.noSqlQuery(body);
      },
      createTable: (parent, { body }, contextValue, info) => {
        body = {
          ...body,
          operation: "create_table",
        }
  
        return contextValue.dataSources.hdbApi.noSqlQuery(body);
      },
      insertRecords: (parent, { schema, table, records }, contextValue, 
info) => {
        const body = {
          operation: "insert",
          schema,
          table,
          records
        }
  
        return contextValue.dataSources.hdbApi.noSqlQuery(body);
      }
    }
  };

  export default resolvers;
```

### Operations
Ok so all the setup is done. We are good to go with the Query / Mutation 
operations. Let's start with Mutations.

## Create schema
Let's try creating a schema in HarperDB with the mutation in Apollo 
GraphQl. Make a note that this schema is not the GraphQL schema, it's the 
schema in HarperDB.
![Create 
schema](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lbuekkn64gvtyyff6ayn.png)

Building the operation and variables is easy, you just need to click on 
the plus sign next to the operation and field.

We can validate this in the browse section of HarperDB studio.
![Schema 
created](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/12zz0f8lmwd59rskcihg.png)

If we try to run the mutation again on Apollo studio, we should see an 
error message that says the schema already exists.
![Schema 
exists](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lumt7n23m9pfaz67v3fn.png)

## Create table
The schema is created, we can now try to add a table in this schema.
![Create 
table](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/01gfnkjb6a5cb80ch5no.png)

The operation is ready however we need to fill the data for the body 
variable, for which we can click on the argument.
![Body 
argument](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/e6bxpyvayymrbhp0hf28.png)

We should be able to see all the input data fields defined for the 
argument. We can add them all with the plus button.
![Input data fields for 
body](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p5dt21yp35da4ywvxqp3.png)

The variable should be populated for us with null fields.
![Variable with null 
values](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/orhxwkos5imyowrclpra.png)

We can replace null with the actual values.
![Variable with actual 
values](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mohdqjvk43j9ynxv8val.png)

We can run the operation and see the response.
![Table 
created](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qziq2daawq6jzt38jb8l.png)

If you try again, you should see an error message.
![Table already 
exists](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/30wz761toujajtokzlvr.png)

## Add entries to table
The operation in this case would be:
```
mutation Mutation($schema: String!, $table: String!, $records: 
[FruitInput!]!) {
  insertRecords(schema: $schema, table: $table, records: $records) {
    message
    status
  }
}
```

The variables would be:
```
  "schema": "myschema",
  "table": "fruits",
  "records": [
    {
      "name": "Apple",
      "calories": 52
    },
    {
      "name": "Banana",
      "calories": 89
    }
  ]
}
```

And the response as follows, after running the mutation:
```
{
  "data": {
    "insertRecords": {
      "message": "inserted 2 of 2 records",
      "status": 200
    }
  }
}
```

## Retrieve records
Let's try a query operation this time, for retrieving all records from the 
table.

The operation is:
```
query Fruits($schema: String!, $table: String!) {
  fruits(schema: $schema, table: $table) {
    calories
    id
    name
  }
}
```

The variables are:
```
{
  "schema": "myschema",
  "table": "fruits"
}
```

And the result of the query operation would be:
```
{
  "data": {
    "fruits": [
      {
        "calories": 52,
        "id": "3963a29c-d696-44ae-a3d8-e11de48bf339",
        "name": "Apple"
      },
      {
        "calories": 89,
        "id": "eec06bc5-85cf-48eb-87d2-89a25fd9f3c1",
        "name": "Banana"
      }
    ]
  }
}
```

## Retrieve selective records
And one final query to retrieve selective records.
The query is:
```
query Query($schema: String!, $table: String!, $name: String!) {
  fruit(schema: $schema, table: $table, name: $name) {
    calories
    id
    name
  }
}
```

Variables:
```
{
  "schema": "myschema",
  "table": "fruits",
  "name": "Apple"
}
```

And result of the query:
```
{
  "data": {
    "fruit": [
      {
        "calories": 52,
        "id": "3963a29c-d696-44ae-a3d8-e11de48bf339",
        "name": "Apple"
      }
    ]
  }
}
```

## Summary
Thus we were able to access the Apollo studio on the browser and send 
queries and mutations to HarperDB. HarperDB is considering GraphQL 
functionality on their roadmap. Check out their [Feedback 
Board](https://feedback.harperdb.io/) and give it an upvote if you think 
it would be helpful!

Feel free to ask questions if the flow is not clear, and correct if there 
are any mistakes. Thank you for reading !!!

Image credit: [unsplash](https://source.unsplash.com/featured/?coding)
























