---
canonical_url: https://dev.to/networkandcode/trying-my-hands-on-neo4j-with-some-iot-data-28g7
categories: cypher, graphdb, iot, neo4j
date: 2022-06-30
tags: cypher, graphdb, iot, neo4j
title: Trying my hands on Neo4j with some IoT data
---

*This post first appeared on [dev.to](https://dev.to/networkandcode/trying-my-hands-on-neo4j-with-some-iot-data-28g7)*

## Introduction

Hello :wave:, time for some GraphDB...

Neo4j is a Graph DB written  in Java, the j in 4j at the end stands for Java :). I like the variety of self placed [courses](https://graphacademy.neo4j.com/courses/) and the certifications offered by them, all for free, wow.

[Cypher](https://neo4j.com/docs/cypher-manual/current/) is the declarative query language we would be using to interact with the Neo4j database. We can run Cypher queries directly on the Neo4j [browser](https://neo4j.com/docs/browser-manual/current/) and can use one of the [drivers](https://neo4j.com/developer/language-guides/) to make calls to the database from our application.

In this post we shall focus on running certain Cypher queries from the browser, and see some key GraphDB concepts along the  way. Let's get started...

## Sandbox
Head over to this [link](https://neo4j.com/sandbox/), signup/signin, and create a sandbox > create a project, choose Blank Project.

We have choosen blank project cause we can also load our own data instead of working with some pre-built data.

Click on the Open button to open the project with the Neo4j browser.

## Delete all
I have already added some data to the blank project before, so I'm going to delete all the nodes and their relationships first, you may not need this yet, however you may come back to this step later on when needed.
```
MATCH (n) DETACH DELETE n

Deleted 42 nodes, deleted 1 relationship, completed after 9 ms.
```
In the command above, the parentheses pair represents a node, and n is a variable that represents a node, so we are matching all nodes (as there are no conditions) and subsequently deleting those including their relationships using [DETACH DELETE](https://neo4j.com/docs/cypher-manual/current/clauses/delete/).

## Node
A node is a discrete entity, for our IoT use case, it could be an Edge device, power source etc. Refer to this github [repo](https://github.com/muntasirjoarder/NeoThings) for a sample IoT data modeling.

In Cypher a Node is enclosed in parantheses, for ex. `(e)` refers to a node represented by a variable e. 

### Labels
And then comes label(s) which are denoted by colon `:`, that we could use to tag a node, for instance if it's an edge device we could label it `:EdgeDevice`. So now our node becomes `(e:EdgeDevice)`. Note that labels are usually written in PascalCase.

We could add multiple labels to a node, so let's also label our edge device as a thing, making our node look like `(e:EdgeDevice:Thing)`,  

### Properties
Properties are key value pairs defining the actual object. Let's say we want to give some names to our edge devices, like Edge Device 1, 2 etc. and another property to identify the floor in which they are installed, like GF, 1F, 2F etc. The properties for our first device would then be like:
```
{
    name: 'Edge Device 1',
    floor: 'GF'
}
```

### Create nodes
Our node should finally look like `(e:EdgeDevice:Thing { name: 'Edge Device 1', floor: 'GF' } )`. Note that the variable name is only optional and is required only if we reuse the variable in our query. Let's create the node on the browser.
```
CREATE (e:EdgeDevice:Thing { name: 'Edge Device 1', floor: 'GF' } ) RETURN e
```
You should now see a graph output like ![Edge Device 1 graph](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/38qkhytq3slruitbo7le.png)

And the respective table should be:
```
{
  "identity": 41,
  "labels": [
    "EdgeDevice",
    "Thing"
  ],
  "properties": {
"name": "Edge Device 1",
"floor": "GF"
  }
}
```
Note that the identity was auto generated.

### Constraints
What if we create another node with the same properties.
```
CREATE (e:EdgeDevice:Thing { name: 'Edge Device 1', floor: 'GF' } ) RETURN e
```

It would get created, and we would now have two similar nodes.
```
MATCH (e:EdgeDevice:Thing { name: 'Edge Device 1'} ) RETURN COUNT(e)

2
```

let's say we want the name of the device  to be unique, in such case, we could create a [constraint](https://neo4j.com/docs/cypher-manual/current/constraints/examples/) to set the name as unique.

But before doing so, we should get rid of the duplicates, as otherwise it would throw an error. Let's first get the IDs of the nodes.
```
MATCH (e:EdgeDevice:Thing) RETURN(ID(e))

0
41
```
So there are two nodes with IDs 0 and 41, we can delete one, let's go with 41. Note the numbers may vary in your case.
```
MATCH (e) WHERE ID(e) = 41 DELETE e

Deleted 1 node, completed after 8 ms.
```

Let's now create the constraint.
```
CREATE CONSTRAINT unqiue_edge_device_name FOR (e:EdgeDevice) REQUIRE e.name IS UNIQUE

Added 1 constraint, completed after 70 ms.
```

Now, if we try to create another device with the same name, it should fail.
```
CREATE (e:EdgeDevice:Thing { name: 'Edge Device 1', floor: 'GF' } ) RETURN e

Neo.ClientError.Schema.ConstraintValidationFailed
Node(0) already exists with label `EdgeDevice` and property `name` = 'Edge Device 1'
```
The above [error](https://neo4j.com/docs/status-codes/current/) denotes ClientError as the error classification, Schema as the error category and ConstraintValidationFailed as the error title.

### Import nodes
So far, we have added only one edge device, we could add other devices as required in a similar manner. However it's common to import many such nodes from a CSV as it would be faster, than executing CREATE statements individually.

I am just going to add some data in Google sheets as follows.
![Google sheet for edge devices](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/864ldautyu73t9yp0xdi.png) There are 74 devices in the table, from device 2 to 75.

I then published it with the following settings.![Google sheets publish](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4oft6ekutuzcyhkajt51.png). Let's now create nodes.
```
LOAD CSV WITH HEADERS FROM <google-spreadsheet-link> AS row
CREATE (:EdgeDevice:Thing { name: row.name, floor: row.floor })

Added 148 labels, created 74 nodes, set 148 properties, completed after 586 ms.
```
Awesome, so we have successfully created the edge device nodes.

### Manufacturer nodes
Let's do a similar exercise to add nodes for the manufacturers. We would add only one property which is name.

Note that I got the companies list from [here](https://builtin.com/internet-things/iot-internet-of-things-companies)

Let's create those. But this time let's go with a loop as we would only add 10 companies.
```
WITH ['Cooler Screens',
    'Farmer’s Fridge',
    'Simplisafe',
    'Inspire',
    'Enovo',
    'Tive',
    'Xage Security',
    'Samsara',
    'Arm',
    'Clearblade'] AS manufacturers
FOREACH ( manufacturer IN manufacturers | CREATE (m:Manufacturer{ name:  manufacturer}) )

Added 10 labels, created 10 nodes, set 10 properties, completed after 8 ms.
```

Let's also add a constraint for the name.
```
CREATE CONSTRAINT unqiue_manufacturer_name FOR (m:Manufacturer) REQUIRE m.name IS UNIQUE
```

## Sensor types
Let's add few other nodes for the sensor type. I obtained the info form this [link](https://behrtech.com/blog/top-10-iot-sensor-types/)
```
WITH [
    'Temperature',
    'Humidity',
    'Pressure',
    'Proximity',
    'Level',
    'Accelerometers',
    'Gyroscope',
    'Gas',
    'Infrared',
    'Optical'
] AS sensorTypes
FOREACH ( sensorType IN sensorTypes | CREATE (:SensorType{ name:  sensorType }) )

Added 10 labels, created 10 nodes, set 10 properties, completed after 7 ms.
```

## Relatioships
So far we have been adding nodes, for now these nodes are isolated data entities with out any relationships to other nodes.

Let's now add a relationship between the nodes Edge Device 1 and Cooler Screens.

Relationships are represented by arrows and square brackets. They are unidirectional `-[]->` or `<-[]-`. They also have a label like node, but it's only one label for a relationship unlike a node, and the relationship label is also called a relationship type. 

Like a node, we can also add properties to a relationship. So if we use `r` as the variable and `IS_MANUFACTURED_BY` as the label it should now become `-[r:IS_MANUFACTURED_BY]->`. Just like nodes, using a variable is optional here too, and is useful when there is a need to reuse it.

Ok, so now let's put the source and target nodes in the relation, so the  final Cypher would be `(:Edge_Device:Thing { name: 'Edge Device 1' } ) -[]-> (:Manufacturer { name: 'Cooler Screens'})`
 
We have formed the cypher, we just need to put CREATE before it to create the relation.
```
Match ( e:EdgeDevice:Thing {name: 'Edge Device 1'}), (m:Manufacturer { name: 'Cooler Screens' } )
CREATE (e) -[r:IS_MANUFACTURED_BY]-> (m)
RETURN e, r, m
```

Let's use MATCH to get the graph.
```
MATCH (e:Edge_Device:Thing { name: 'Edge Device 1' } ) -[r:IS_MANUFACTURED_BY]-> (m:Manufacturer { name: 'Cooler Screens'}) RETURN e, r, m
```

The graph should look like ![Relationship graph](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0mwep5gzq8jf1arem1lj.png)

Note that we can drag the graph objects for desired visibility. 

### Sensor
To say Edge device device 1 supports Temperature sensor.
```
Match ( e:EdgeDevice:Thing {name: 'Edge Device 1'}), (s:SensorType { name: 'Temperature' })
CREATE (e) -[r:HAS_SENSOR_TYPE]-> (s)
RETURN e, r, s
```

The returned graph should be
![Sensor relationship](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/x0ka1w2y6adee1b2gi64.png)

Let's now see the final graph of Edge device 1 with both relationships.
```
MATCH (e:EdgeDevice:Thing) -[r]-> (n) RETURN e, r, n
```
![Graph with all relationships](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b2pyb54v2y9ljtld2dqy.png)
 
Thus, we have put some minimal data relevant to IoT and explored some fundamental concepts/functionalities of GraphDB, Cypher, and the Neo4j browser. Thank you for reading !!!

 
