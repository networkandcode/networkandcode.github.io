---
title: owasp juice shop > launch with own docker image
categories: owasp juice shop
---

There is already an offical docker image for the juice shop application at the repo 
bkimminich/juice-shop. However we also have the provision to make a docker image of our own, using the 
docker file in the source code, as the juice shop is an open source application. In this blog post, 
we are gonna see how to do that. Its assumed you have cloned the source code of juice shop from github, 
you have installed docker on your system, and you have an account at docker hub.

Let's get started...

I'm at the root of the repo.
```
$ pwd
/home/networkandcode/juice-shop
```

There should be a Dockerfile at this directory.
```
$ ls Dockerfile
Dockerfile
```

Let's view the contents of this Dockerfile.
```
$ cat Dockerfile 
FROM node:12 as installer
COPY . /juice-shop
WORKDIR /juice-shop
RUN npm i -g typescript ts-node
RUN npm install --production --unsafe-perm
RUN npm dedupe
RUN rm -rf frontend/node_modules

FROM node:12-alpine
ARG BUILD_DATE
ARG VCS_REF
LABEL maintainer="Bjoern Kimminich <bjoern.kimminich@owasp.org>" \
    org.opencontainers.image.title="OWASP Juice Shop" \
    org.opencontainers.image.description="Probably the most modern and sophisticated insecure web application" \
    org.opencontainers.image.authors="Bjoern Kimminich <bjoern.kimminich@owasp.org>" \
    org.opencontainers.image.vendor="Open Web Application Security Project" \
    org.opencontainers.image.documentation="https://help.owasp-juice.shop" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.version="12.8.1" \
    org.opencontainers.image.url="https://owasp-juice.shop" \
    org.opencontainers.image.source="https://github.com/bkimminich/juice-shop" \
    org.opencontainers.image.revision=$VCS_REF \
    org.opencontainers.image.created=$BUILD_DATE
WORKDIR /juice-shop
RUN addgroup --system --gid 1001 juicer && \
    adduser juicer --system --uid 1001 --ingroup juicer
COPY --from=installer --chown=juicer /juice-shop .
RUN mkdir logs && \
    chown -R juicer logs && \
    chgrp -R 0 ftp/ frontend/dist/ logs/ data/ i18n/ && \
    chmod -R g=u ftp/ frontend/dist/ logs/ data/ i18n/
USER 1001
EXPOSE 3000
CMD ["npm", "start"]
```

From the dockerfile, we see its base image is node12:alpine which will be picked from dockerhub, and 
then its executing certain linux commands, we are not gonna get into the depth of those commands, here 
though. Finally it runs the command npm start, to start the juice shop application.

Let's build our docker image using this dockerfile. The format of the command would be ```docker build . 
-t <username/repo:tag>``` Here ```.``` refers to the current directory as we are going to run this command where 
the dockerfile is present. The username is your docker hub username, I have used my username which is 
s1405. The tag if not provided will be latest by default.
```
$ docker build . -t s1405/owasp-juice-shop:21080813
Sending build context to Docker daemon  46.23MB
Step 1/18 : FROM node:12 as installer
12: Pulling from library/node
08224db8ce18: Pull complete 
abd3caf86f5b: Pull complete 
71c316554a55: Pull complete 
--TRUNCATED--
Successfully built ef2e35d02cce
Successfully tagged s1405/owasp-juice-shop:21080813
```

The image is successfully built.
```
$ docker image ls s1405/owasp-juice-shop
REPOSITORY               TAG                 IMAGE ID            CREATED             SIZE
s1405/owasp-juice-shop   21080813            ef2e35d02cce        13 minutes ago      495MB
```

We can push this image to our docker hub repo, for which we need to login first.
```
$ docker login
Login with your Docker ID to push and pull images from Docker Hub. If you don't have a Docker ID, head over to https://hub.docker.com to create one.
Username: s1405
Password: 
WARNING! Your password will be stored unencrypted in /home/networkandcode/snap/docker/796/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

And then push. This stage is optional, however it helps with reusing the image in future, when not 
available locally.
```
$ docker push s1405/owasp-juice-shop:21080813
The push refers to repository [docker.io/s1405/owasp-juice-shop]
3661f3683042: Pushed 
1dbe1865b615: Pushed 
3548ffb57dd8: Layer already exists 
f166ad2b7b2d: Layer already exists 
052597e22e57: Layer already exists 
b5d9fcff4e03: Layer already exists 
a96e37fcd4d5: Layer already exists 
9a5d14f9f550: Layer already exists 
21080813: digest: sha256:8908216d39a2937c16c61ad7b4f65e30aa1e239adea08c1e26c15b9c827b8d7d size: 1999
```

The image should appear on docker hub too.
![OWASP Juice Shop Image](/assets/owasp-juice-shop-launch-with-own-docker-image-1.png)

We can now run the app with our docker image.
```
$ docker run -d -p 8000:3000 s1405/owasp-juice-shop:21080813
922fb0c8729f21ac649185246c2134f52c69f4cd920fad926e48dfbf3c0638ac
```

It wont pull the image from docker hub, as the image is already there locally, we have however pushed 
it to docker hub, so that we can use it in future when required.

The container is active.
```
$ docker container ls | grep juice-shop
922fb0c8729f        s1405/owasp-juice-shop:21080813   "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes        0.0.0.0:8000->3000/tcp      bold_mahavira
```

We can access the app on our browser.
![OWASP Juice Shop Image](/assets/owasp-juice-shop-launch-with-own-docker-image-2.png)

Stop the container when required.
```
$ docker container stop 922fb0c8729f
922fb0c8729f
```

Hope this post helps in building your own docker image version of the juice shop app, pushing it to 
your docker hub registry and running a container with the image. Thank you for reading.

--end-of-post--
