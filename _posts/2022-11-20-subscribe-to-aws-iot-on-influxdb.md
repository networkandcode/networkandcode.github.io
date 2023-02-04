---
canonical_url: https://dev.to/aws-builders/send-messages-from-aws-iot-to-influxdb-via-native-mqtt-subscription-3366
categories: aws, influxdb, iot, mqtt
cover_image: 
https://images.unsplash.com/photo-1545259741-2ea3ebf61fa3?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80
date: 2022-11-20
tags: aws, influxdb, iot, mqtt
title: Subscribe to AWS IoT topic on InfluxDB
---

This post first appeared on [dev.to](https://dev.to/aws-builders/harperdb-on-eks-1bcb)

Hey :wave:, here is my first post after the community builder renewal :satisfied:. In this post, we would send some MQTT messages in line 
protocol format to AWS IoT, which would then get ingested to InfluxDB via a native MQTT subscription.

InfluxDB usually relies on systems such as Telegraf or some client programs to send metrics to it, however here with the native 
subscription, we don't need the intermediate system. 

As a prerequisite, follow this [post](https://dev.to/aws-builders/aws-iot-pubsub-over-mqtt-1oig) to understand how to publish messages from 
a Python based MQTT client to the MQTT endpoint in AWS.

We would be making change to the publisher code, as InfluxDB looks for messages in a different format called as the line protocol.

Refer to this 
[link](https://docs.influxdata.com/influxdb/cloud/reference/syntax/line-protocol/#:~:text=InfluxDB%20uses%20line%20protocol%20to,timestamp%20of%20a%20data%20point.&text=Lines%20separated%20by%20the%20newline,a%20single%20point%20in%20InfluxDB.) 
for more information on the lineprotocol.

A sample message in our case would be like *temp_sensor,id=client-d36a601f-0b0e-4ba2-9d54-45feec236deb,room=lobby temp=30 
1668930716251915510*  

Where temp_sensor is the measurement name, the tags are id and room, the field is temp. Note the timestamp above is in unix timestamp format 
in nanoseconds. Note that the tags & timestamp are optional in line protocol, and you can have more than one filed. The timestamp will 
default to the current time if not provided.

Our publisher code would look like below.
```
nc:~/environment/iot $ cat publish-line-protocol.py 
# import vars from connect.py
from connect import args, client_id, mqtt_connection

from awscrt import mqtt
import json, random, time

while True:
    rooms = [ 'bed-room', 'hall', 'kitchen', 'living-room', 'lobby' ]
    room = random.choice(rooms)
    
    # set random temperature between 24 and 32 (this is celsius range)
    temp = random.randrange(24, 32)
    
    # set timestamp in  nanoseconds
    now = time.time_ns()
    
    # form the message
    message = f'temp_sensor,id={client_id},room={room} temp={temp} {now}'
    
    # publish the  message
    mqtt_connection.publish(
        topic=args.topic,
        payload= message,
        qos=mqtt.QoS.AT_LEAST_ONCE
    )
    print(f'Message published: {message}')
    time.sleep(1)
```

Let's run the code.
```
nc:~/environment/iot $ python publish-line-protocol.py --ep $IOT_DEV_EP --pubcert pub-cert.pem --pvtkey pvt-key.pem --cacert ca-cert.pem 
--topic temperature
client-7219bca1-8c06-41c8-b69c-783c3ee85a41 is connected!
Message published: temp_sensor,id=client-7219bca1-8c06-41c8-b69c-783c3ee85a41,room=hall temp=29 1668932805475181112
Message published: temp_sensor,id=client-7219bca1-8c06-41c8-b69c-783c3ee85a41,room=hall temp=24 1668932806476308869
Message published: temp_sensor,id=client-7219bca1-8c06-41c8-b69c-783c3ee85a41,room=lobby temp=24 1668932807477465026
```

Press Ctrl C when you want to stop the code.

Now, let's launch InfluxDB, you may get a cloud subscription from the AWS 
[marketplace](https://aws.amazon.com/marketplace/pp/prodview-4e7raoxoxsl4y?ref_=unifiedsearch), or directly from the 
[influxdata](https://cloud2.influxdata.com/) portal.

On InfluxDB, Goto Load Data > Native Subscriptions and create a new suscription. Set the subscription name as *temp_sensor*. Enter some 
description like *Messages from AWS MQTT*. Go to Security details > certificate and copy/paste the ca certificate, private key and public 
certificate downloaded from AWS while creating the thing in  IoT. Set the topic as *temperature* because that's where we were publishing the 
messages to. And then set the write destination  to a bucket, which can be created if it doesn't exist yet.
![Create bucket for subscription in InfluxDB](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/s1bdzfhaeh1kfov6asiw.png)

That's it, save  the subscription.

We can now visit the data explorer, and see the graph for the   data sent. If we hover over the graph, we should be able to see the values 
for each of the tags(rooms) that have different colors.
![Data explorer on InfluxDB](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ejpz8urw9lgitw17rdpt.png)

This way we can send MQTT metrics to InfluxDB with subscriptions and visualize those. A couple of things before finishing, you may stop the 
subscription, when you don't want to keep it running,
![Stop subscription link in InfluxDB](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ju4u5524akcfd8amo4g3.png)

and there is a notifications link on the subscription that should help you with logs for troubleshooting errors.
![Notifications link in InfluxDB subscription](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yu1lclrg0z52sk5y4c1l.png)

Thank you for reading !!!
