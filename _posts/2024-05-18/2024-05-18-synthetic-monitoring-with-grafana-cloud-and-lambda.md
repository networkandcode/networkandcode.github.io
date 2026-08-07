---
canonical_url: "https://dev.to/aws-builders/synthetic-monitoring-with-grafana-cloud-1n5b"
date: "2024-05-18"
title: "Synthetic Monitoring with Grafana Cloud and Lambda"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fvvleso6jt686i30pmi1l.png"
tags: "aws, monitoring, http, javascript"
categories: "aws, monitoring, http, javascript"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/synthetic-monitoring-with-grafana-cloud-1n5b)**

:clock1:Time for some synthetic monitoring fun with Grafana...:bar_chart: We'd deploy a simple function on AWS Lambda that generates some data. We then expose this function with a public URL which would then be probed with a synthetic test from Grafana cloud servers.

## AWS Lambda
Create a new AWS lambda function with runtime as nodejs and a name such as `synthetic-monitoring-demo`. Put the following code in `index.js`, which returns data similar to what's returned by this Grafana provided [endpoint](https://test-api.k6.io/public/crocodiles/). We just create a lambda function here so that we could test as required and delete it when done.
```
const randomInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min
const randomChoice = (arr) => arr[randomInt(0, arr.length - 1)]

const generateCrocodileData = () => {
    const names = [
        "Smiley", "Snappy", "Bitey", "Chompy", "Jaws", "Scaly", "Cruncher", 
        "Munch", "Gator", "Nibbles", "Swampy", "Toothless", "Grin", "Sly", 
        "Snapper", "Croc", "Dagger", "Ripjaw", "Spike", "Thrasher"
    ]
    const species = [
        "Saltwater Crocodile", "Nile Crocodile", "Mugger Crocodile", 
        "American Crocodile", "Freshwater Crocodile", "Morelet's Crocodile", 
        "Cuban Crocodile", "Siamese Crocodile", "Philippine Crocodile", 
        "Orinoco Crocodile", "Dwarf Crocodile", "Slender-snouted Crocodile"
    ]

    return {
        name: randomChoice(names),
        species: randomChoice(species),
        age: randomInt(1, 70),
        sex: randomChoice(["M", "F"]),
    }
}

export const handler = async () => {
    const numRecords = 8
    const crocodiles = Array.from({ length: numRecords }, generateCrocodileData)
    return {
        statusCode: 200,
        body: JSON.stringify(crocodiles),
    }
}
```

The crocodile species names were taken via generative AI, so not quite sure if it's correct:wink:. 

Deploy the function, and then create a function URL in the configuration section with auth type as none, so that it could be accessed publicly:earth_africa:.
![Create function url](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4t2fl4mqsr9tvwgc1z1y.png)

Try accessing the function URL.
![Access the function url](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/c1dchscxgvnzw0kaarhq.png)

## K6
The synthetic monitoring in Grafana is based on k6. So we shall try some k6 basics on the local machine first.

[Install](https://grafana.com/docs/k6/latest/set-up/install-k6/) k6.
```
brew install k6
```

The command `k6 new test.js` should create a file with name `test.js` with some references in it. However, for our case we can add a file `test.js` from scratch. Let's first import the functions/modules we need.
```
import { check } from 'k6'
import http from 'k6/http'
```

We just need to create a function that's exported by default in this code inside which we can try calling the api with http modules's get() function. Let's use the function URL we generated as endpoint for this purpose and try printing the status, response body as an array and length of the returned response array.
```
export default function main() {
  const res = http.get('https://ieaivrjwpcdbuxh4tws5autdoa0sflqi.lambda-url.us-east-1.on.aws/')
  console.log('The response status is', res.status)
  console.log('The response array is', res.json())
  console.log('The length of the response array is', res.json().length)
}
```

We could now this run this code with k6 and see the output as well as some test results.
```
$ k6 run test.js

          /\      |‾‾| /‾‾/   /‾‾/   
     /\  /  \     |  |/  /   /  /    
    /  \/    \    |     (   /   ‾‾\  
   /          \   |  |\  \ |  (‾)  | 
  / __________ \  |__| \__\ \_____/ .io

     execution: local
        script: test.js
        output: -

     scenarios: (100.00%) 1 scenario, 1 max VUs, 10m30s max duration (incl. graceful stop):
              * default: 1 iterations for each of 1 VUs (maxDuration: 10m0s, gracefulStop: 30s)

INFO[0001] The response status is 200                    source=console
INFO[0001] The response array is [{"name":"Chompy","species":"Mugger Crocodile","age":41,"sex":"M"},{"name":"Snappy","species":"Orinoco Crocodile","age":24,"sex":"M"},{"name":"Spike","species":"Mugger Crocodile","age":64,"sex":"M"},{"species":"Siamese Crocodile","age":40,"sex":"M","name":"Gator"},{"species":"Freshwater Crocodile","age":44,"sex":"F","name":"Snapper"},{"sex":"F","name":"Sly","species":"Slender-snouted Crocodile","age":11},{"age":24,"sex":"M","name":"Ripjaw","species":"Mugger Crocodile"},{"name":"Thrasher","species":"Orinoco Crocodile","age":67,"sex":"M"}]  source=console
INFO[0001] The length of the response array is 8         source=console

     data_received..................: 6.5 kB 7.3 kB/s
     data_sent......................: 542 B  606 B/s
     http_req_blocked...............: avg=533.74ms min=533.74ms med=533.74ms max=533.74ms p(90)=533.74ms p(95)=533.74ms
     http_req_connecting............: avg=246.67ms min=246.67ms med=246.67ms max=246.67ms p(90)=246.67ms p(95)=246.67ms
     http_req_duration..............: avg=356.86ms min=356.86ms med=356.86ms max=356.86ms p(90)=356.86ms p(95)=356.86ms
       { expected_response:true }...: avg=356.86ms min=356.86ms med=356.86ms max=356.86ms p(90)=356.86ms p(95)=356.86ms
     http_req_failed................: 0.00%  ✓ 0        ✗ 1
     http_req_receiving.............: avg=357µs    min=357µs    med=357µs    max=357µs    p(90)=357µs    p(95)=357µs   
     http_req_sending...............: avg=297µs    min=297µs    med=297µs    max=297µs    p(90)=297µs    p(95)=297µs   
     http_req_tls_handshaking.......: avg=285.27ms min=285.27ms med=285.27ms max=285.27ms p(90)=285.27ms p(95)=285.27ms
     http_req_waiting...............: avg=356.21ms min=356.21ms med=356.21ms max=356.21ms p(90)=356.21ms p(95)=356.21ms
     http_reqs......................: 1      1.117563/s
     iteration_duration.............: avg=894.17ms min=894.17ms med=894.17ms max=894.17ms p(90)=894.17ms p(95)=894.17ms
     iterations.....................: 1      1.117563/s


running (00m00.9s), 0/1 VUs, 1 complete and 0 interrupted iterations
default ✓ [======================================] 1 VUs  00m00.9s/10m0s  1/1 iters, 1 per VU
```

So based on the output above, the api is returning 8 crocodiles with it's name, gender and other details. The test results give us some metrics such as data recd., sent and other http metrics. Note that we haven't added any checks so far, though we have imported the check function.

For this usecase let's do a few checks such as:
1. Check the response status to be 200
2. Is it sending back 8 crocodile details
3. Is it giving back the details of 4 male and 4 crocodiles, meaning is the response distrubuted equally based on gender
4. There should be atleast one crocodile under 15 years of age

The code for these checks should look like below:
```
  check(res, {
    'is status 200': (r) => r.status === 200,
    'is response length 8': (r) => r.json().length === 8,
    'is response distributed equally based on gender': (r) => {
      let maleCount = 0
      let femaleCount = 0
      r.json().forEach(crocodile => {
        if (crocodile.sex === 'M') {
          maleCount++
        } else if (crocodile.sex === 'F') {
          femaleCount++
        }
      })
      return (maleCount === femaleCount)
    },
    'is any crocodile under 15 years of age': (r) => {
      const isAnyUnder15 = r.json().some(crocodile => crocodile.age < 15)
      return isAnyUnder15
    }
  })
```

Please keep the checks block inside the main function after which we can run the test again.
```
% k6 run test.js
---TRUNCATED---
     ✓ is status 200
     ✓ is response length 8
     ✗ is response distributed equally based on gender
      ↳  0% — ✓ 0 / ✗ 1
     ✗ is any crocodile under 15 years of age
      ↳  0% — ✓ 0 / ✗ 1
---TRUNCATED---
```
So, couple of our checks are failing.

All good:thumbsup:, so we got some grip on how to run k6 and add some checks. We can try doing the same stuff on grafana.

## Grafana
Go to `Grafana Cloud > Home > Testing & synthetics > Add a new check > Scripted check`. I have defined the following options in the form.
```
Job name: test-job
Instance: test-instance
Probe locations: Seoul(I have chosen only one)
```

In the script from, just put the same script we used before, and test/save it.
![Set synethtic monitoring in Grafana](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p3h1m09vnnqm36eqpejd.png)

Note that by default the logs and metrics related to our test would go to the loki and mimir endpoints of Grafana cloud.

The out of box dashboard for our check should appear in sometime. The assertions panel which gives a stat and timeseries graph(expanded view) for the four checks.
![Dashboard preview](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jnio6uuw1p7crexvnx2m.png)

As a bonus let's go to `Home > Dashbooards > New Dashboard` and try creating a custom dashboard panel with mimir(prometheus type datasource).
![Current probe checks status](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/oy0whqdzmymds4f72du1.png)
Here is the panel json for this.
```
{
  "datasource": {
    "uid": "grafanacloud-prom",
    "type": "prometheus"
  },
  "type": "stat",
  "title": "Current probe checks status",
  "gridPos": {
    "x": 0,
    "y": 8,
    "w": 12,
    "h": 8
  },
  "id": 1,
  "targets": [
    {
      "datasource": {
        "type": "prometheus",
        "uid": "grafanacloud-prom"
      },
      "refId": "A",
      "expr": "sum(probe_checks_total{job=\"test-job\"}) by(result)",
      "range": false,
      "instant": true,
      "editorMode": "code",
      "legendFormat": "__auto",
      "useBackend": false,
      "disableTextWrap": false,
      "fullMetaSearch": false,
      "includeNullMetadata": true,
      "format": "time_series",
      "exemplar": false
    }
  ],
  "options": {
    "reduceOptions": {
      "values": true,
      "calcs": [
        "lastNotNull"
      ],
      "fields": ""
    },
    "orientation": "auto",
    "textMode": "auto",
    "wideLayout": true,
    "colorMode": "value",
    "graphMode": "area",
    "justifyMode": "auto",
    "showPercentChange": false
  },
  "transformations": [
    {
      "id": "calculateField",
      "options": {
        "mode": "binary",
        "reduce": {
          "reducer": "sum"
        },
        "binary": {
          "left": "fail",
          "right": "pass"
        },
        "alias": "total"
      }
    },
    {
      "id": "calculateField",
      "options": {
        "mode": "binary",
        "binary": {
          "left": "pass",
          "operator": "/",
          "right": "total"
        },
        "alias": "success ratio"
      }
    }
  ],
  "fieldConfig": {
    "defaults": {
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          {
            "value": null,
            "color": "green"
          },
          {
            "value": 80,
            "color": "red"
          }
        ]
      },
      "color": {
        "mode": "thresholds"
      }
    },
    "overrides": [
      {
        "matcher": {
          "id": "byName",
          "options": "fail"
        },
        "properties": [
          {
            "id": "thresholds",
            "value": {
              "mode": "absolute",
              "steps": [
                {
                  "color": "green",
                  "value": null
                },
                {
                  "color": "red",
                  "value": 1
                }
              ]
            }
          }
        ]
      },
      {
        "matcher": {
          "id": "byName",
          "options": "success ratio"
        },
        "properties": [
          {
            "id": "unit",
            "value": "percentunit"
          },
          {
            "id": "thresholds",
            "value": {
              "mode": "absolute",
              "steps": [
                {
                  "color": "red",
                  "value": null
                },
                {
                  "color": "yellow",
                  "value": 0.8
                },
                {
                  "value": 0.9,
                  "color": "green"
                }
              ]
            }
          }
        ]
      },
      {
        "matcher": {
          "id": "byName",
          "options": "total"
        },
        "properties": [
          {
            "id": "color",
            "value": {
              "mode": "shades",
              "fixedColor": "purple"
            }
          }
        ]
      }
    ]
  },
  "pluginVersion": "11.1.0-70724"
}
```

And one with loki for logs.
![Logs panel](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r0dkh2blb2st7j69l2te.png)

Cool, we came to the end of this post:clap:, here we tried synthetic testing first with k6 and used the same script with Grafana cloud and visualized the data with couple of panels. As a housekeeping reminder, you may delete the check that's created in Grafana, so that it stops polling the endpoint, and then may delete the function in AWS Lambda. Thanks for reading!!!
