---
title: owasp juice shop >  run as container
categories: owasp juice shop
---

Let's run the juice shop as a docker container on our local system, you should have already 
installed docker to perform this exercise.

Check if docker is installed, I have the following version.
```
$ docker -v
Docker version 19.03.13, build cd8016b6bc
```

Pull the juice shop docker image from docker hub.
```
$ docker pull bkimminich/juice-shop
Using default tag: latest
latest: Pulling from bkimminich/juice-shop
ddad3d7c1e96: Pull complete 
3a8370f05d5d: Pull complete 
71a8563b7fea: Pull complete 
119c7e14957d: Pull complete 
21fe34ef8841: Pull complete 
501f36819cdc: Pull complete 
ada263f3355f: Pull complete 
bea7f14d7e5f: Pull complete 
Digest: sha256:8abf7e5b28b5b0e3e2a88684ecac9dc9740643b46e17a4edc9fc16141289869b
Status: Downloaded newer image for bkimminich/juice-shop:latest
docker.io/bkimminich/juice-shop:latest
```

We can now see this image in our local registry.
```
$ docker image ls bkimminich/juice-shop
REPOSITORY              TAG                 IMAGE ID            CREATED             SIZE
bkimminich/juice-shop   latest              3ed777581dce        5 weeks ago         488MB
```

Let's run it, on the localhost port 8000, which maps to the container port 3000.
```
$ docker run -d -p 8000:3000 bkimminich/juice-shop
23d947b010d8fe6667bff18bcc67124fbb25e9c70f90a95af49d405939bcf415
```

The container should be running in the background.
```
$ docker container ls
CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS              PORTS                    NAMES
23d947b010d8        bkimminich/juice-shop   "docker-entrypoint.s…"   46 seconds ago      Up 44 seconds       0.0.0.0:8000->3000/tcp   nice_khorana
```

Its running and hence we should be able to access it's UI in the browser on port 8000.
![OWASP Juice Shop](/assets/owasp-juice-shop-run-as-container.png)

The container can be stopped, when required by mentioning the container id with the stop command.
```
$ docker container stop 23d947b010d8
23d947b010d8
```

The container doesn't exist any more.
```
$ docker container ls
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
$ 
```

--end-of-post--
