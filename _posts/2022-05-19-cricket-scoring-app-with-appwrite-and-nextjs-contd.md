---
canonical_url: https://dev.to/networkandcode/cricket-scoring-app-with-appwrite-and-nextjscontd-2k64
categories: appwrite, nextjs, react, tailwindcss
date: 2022-05-19
tags: appwrite, nextjs, react, tailwindcss
title: Cricket scoring app with Appwrite and NextJS(contd.)
---

*This post first appeared on [dev.to](https://dev.to/networkandcode/cricket-scoring-app-with-appwrite-and-nextjscontd-2k64/edit)*

Hey all :wave:, this is in continuation to the [previous post](https://dev.to/networkandcode/cricket-scoring-app-using-appwrite-nextjs-3730), that covered changes done on the [appwrite-hackathon](https://github.com/networkandcode/cricscore/tree/appwrite-hackathon) branch, which was mainly kept and submitted for the hackathon.

This post is not part of the [hackathon](https://dev.to/t/appwritehack), as it's over. I thought I would share a few more changes I have done recently, which should be visible on the [main](https://github.com/networkandcode/cricscore/tree/main) branch, and a preview is available via [vercel](https://cricscore.vercel.app/) hosting. Note that the web app may not work properly just in case the backend Appwrite server is not on, as I have used EC2 on [AWS Cloud9](https://dev.to/aws-builders/run-svelte-app-on-aws-cloud9-4j5b) for setting it up and there are chances it can be shut when idle.

Ok, so here are a few screenshots from Appwrite that shows some backend, DB configuration etc.

Make sure the platform configuration allows requests from the client URL, in my case it's as follows.
![Platform configuration](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qsvaovy6ue3l82ddfbls.png)Thank you @meldiron for the quick help on this platform stuff.

I have setup appwrite with a custom domain, by adding an IPv4 A record for a subdomain pointing to the EC2 instance's elastic IP. The DNS configuration can be done where you bought the domain from, with out any namespace changes. Since I am using Appwrite over a domain, I have to do two extra  things at Appwrite side, first the env variable _APP_DOMAIN_TARGET should be set to what ever domain over which you are intending to use Appwrite and then, you need to go the custom domains section and add the same URL.
![Custom domains](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rpvsrd9w30fnidp7ix83.png)

And once the .env file is setup properly Appwrite can be reinstalled/installed with `docker-compose up`, so you would need to first download both docker-compose.yaml and .env from the recent URL provided by [Appwrite](https://appwrite.io/docs/installation#manual), and also should have installed [docker-compose](https://docs.docker.com/compose/install/).

```
$ cat .env | grep -i DOMAIN_TARGET
_APP_DOMAIN_TARGET=<domain-where-appwrite-would-run>
```

The docker compose file should create a bunch of containers :fire:.
```
$ docker container ls | grep appwrite | awk '{print $2}' | uniq                                                                                           
appwrite/appwrite:0.13.0
traefik:2.5
appwrite/appwrite:0.13.0
redis:6.0-alpine3.12
mariadb:10.7
appwrite/telegraf:1.2.0
appwrite/influxdb:1.0.0
```
As seen above, appwrite also uses mariadb behind the scenes. Though I have used 0.13 here, [0.14](https://hub.docker.com/layers/appwrite/appwrite/appwrite/0.14/images/sha256-357db37e2db12816a8bb79c816b3fbdd86e6df1ae9358c265ba5a59599ab975d?context=explore) is already out:new:. I would plan for an upgrade though, just seeing how I can do a seamless upgrade.

What else, some screenshots from Appwrite that shows the DB fields.

The collections are as follows.
![Collections](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/14epfnvt8lnznmz9avcf.png)
 

And all the collections are setup with document level permissions.
![Document level permissions](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7bh72o9srw445378cjer.png)

The atrributes and indexes for each collection are as follows.

Players:
```
    "attributes": [
        {
            "key": "username",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "format": "email",
            "default": null
        },
        {
            "key": "players",
            "type": "string",
            "status": "available",
            "required": true,
            "array": true,
            "size": 255,
            "default": null
        }
    ]
``` 

Matches:
```
"attributes": [
        {
            "key": "matchName",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "matchNoOfPlayers",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "matchNoOfOvers",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "matchPlace",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "matchStatus",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "teamAName",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "teamAPlayers",
            "type": "string",
            "status": "available",
            "required": true,
            "array": true,
            "size": 255,
            "default": null
        },
        {
            "key": "teamBName",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "teamBPlayers",
            "type": "string",
            "status": "available",
            "required": true,
            "array": true,
            "size": 255,
            "default": null
        },
        {
            "key": "tossWinner",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "tossWinnerChoice",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "userID",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "winner",
            "type": "string",
            "status": "available",
            "required": false,
            "array": false,
            "size": 255,
            "default": null
        }
    ]
```

Overs:
```
"attributes": [
        {
            "key": "balls",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "bowler",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "matchID",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "innings",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "over",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "runs",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "wickets",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        }
    ],
    "indexes": [
        {
            "key": "matchID",
            "type": "key",
            "status": "available",
            "attributes": [
                "matchID"
            ],
            "orders": [
                "ASC"
            ]
        }
    ]
```

BattingScoreCard:
```
"attributes": [
        {
            "key": "balls",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "batsman",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "batsmanNo",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "innings",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "matchID",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "position",
            "type": "string",
            "status": "available",
            "required": true,
            "array": false,
            "size": 255,
            "default": null
        },
        {
            "key": "runs",
            "type": "integer",
            "status": "available",
            "required": true,
            "array": false,
            "min": -9223372036854776000,
            "max": 9223372036854776000,
            "default": null
        },
        {
            "key": "out",
            "type": "boolean",
            "status": "available",
            "required": false,
            "array": false,
            "default": false
        }
    ],
    "indexes": [
        {
            "key": "matchID",
            "type": "key",
            "status": "available",
            "attributes": [
                "matchID"
            ],
            "orders": [
                "ASC"
            ]
        }
    ]
```

The database could be even tweaked better, with precise min max values, note that the attributes have to be defined first, unlike firestore or [HarperDB](https://networkandcode.hashnode.dev/online-shop-with-nextjs-and-harperdb), where they could be created on the fly. But this approach is ok, I think we have more control, and is secure.

Ok give it a [try](https://cricscore.vercel.app/), and let me know if it's ok or needs improvements to the logic or UI, and feel free to modify the [code](https://github.com/networkandcode/cricscore) and make it better.
![Match summary](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/fmwohxgfjl7x896u3jl7.png)
   
Thank you !!! :slightly_smiling_face: