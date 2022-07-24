---
canonical_url: https://networkandcode.hashnode.dev/install-appwrite-on-linode
categories: appwrite, docker, linode, linux
date: 2022-06-11
tags: appwrite, docker, linode, linux
title: Install Appwrite on Linode
---

*This post first appeared on [hashnode.dev](https://networkandcode.hashnode.dev/install-appwrite-on-linode)*

## Introduction
[Appwrite](https://appwrite.io/) is a backend server that can be leveraged for integrating services such as authentication, storage, database etc. to our frontend application. It can be launched with docker, as it's a set of docker containers offering specific services. Here, we are going to install it on top of an Ubuntu machine on [Linode](https://www.linode.com/).

## SSH keys
This step is not required if you would be accessing the cloud instance via password. However SSH keys are a secure way to access instances than passwords. 

You can follow this on any Unix / Linux based machine, it works on [Git Bash](https://git-scm.com/download/win) too on Windows.

Generate SSH keys on your local machine, from which you would be accessing the Linode instance.
```
$ ssh-keygen
```
You can copy the public key, which is by default at the following location.
```
$ cat ~/.ssh/id_rsa.pub
```

## Instance
Appwrite needs atleast 1 CPU and 2 GB RAM as mentioned on their [docs](https://appwrite.io/docs/installation#systemRequirements). So, I have  created a Linode instance with the following spec.

![Create linode](https://cdn.hashnode.com/res/hashnode/image/upload/v1654915190109/lAaB7W6WH.png align="left")
```
OS: Ubuntu 22.04 LTS
Hostname: appwrite
2 CPU Cores, 80 GB Storage, 4 GB RAM

Plan:
Linode 4 GB

Region:
Mumbai, IN
```
You can setup password for the root user and optionally add the SSH keys(more secure) copied from the previous step, as per your convenience.

## Change hostname
The default hostname is localhost, so we can better change it to appwrite.
```
root@localhost:~# hostname appwrite
```
The new hostname would be effective from the next login.

## Install docker engine
We can now install the [docker engine](https://docs.docker.com/engine/install/ubuntu/)
```
apt-get update -y

apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release -y

mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y

apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y
```

We shoud now have docker and docker compose
```
root@appwrite:~# docker -v
Docker version 20.10.17, build 100c701

root@appwrite:~# docker compose version
Docker Compose version v2.6.0
```

## Add user
When we created the instance it would only have the root user. Login to the instance via the LISH console or any SSH client as root, and add a new user.
```
root@localhost:~# adduser appwrite
Adding user `appwrite' ...
Adding new group `appwrite' (1000) ...
Adding new user `appwrite' (1000) with group `appwrite' ...
Creating home directory `/home/appwrite' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for appwrite
Enter the new value, or press ENTER for the default
        Full Name []:
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] Y
```

The appwrite user should have been created under the appwrite group.
```
root@appwrite:~# id appwrite
uid=1000(appwrite) gid=1000(appwrite) groups=1000(appwrite)
```

## Add to group
The docker group would have read write permissions on the docker.sock file.
```
$ ls /var/run/docker.sock -l
srw-rw---- 1 root docker 0 Jun 11 03:06 /var/run/docker.sock
```
Hence, add the appwrite user to the docker group, so that we can run docker commands as the appwrite user. 
```
root@appwrite:~# usermod -aG docker appwrite
root@appwrite:~# id appwrite
uid=1000(appwrite) gid=1000(appwrite) groups=1000(appwrite),999(docker)
```

## Clone
Login as the appwrite user with the password for the first time, and then optionally you can copy the SSH public key from your local machine to the location `.ssh/authorized_keys` for futher logging in via SSH keys.

Clone the [appwrite](https://github.com/appwrite/appwrite.git) repo
```
appwrite@appwrite:~$ git clone https://github.com/appwrite/appwrite.git
```

## Up
Change directory and run docker compose.
```
cd appwrite
docker compose up
```
This is not the quick start installation mode, we are doing a full installation, so that we can update Appwrite environment configuration when required. There would be a build status at the top of the screen like below.
```
[+] Building 355.8s (85/609)
```
Note that this would take a while, and we have to wait until all the images are built. 

## Containers 
You can open a different SSH session and see if the containers are running.
```
appwrite@appwrite:~$ docker container ls | awk '{print $2}'
ID
appwrite_appwrite-worker-functions
traefik:2.7
appwrite_appwrite-executor
appwrite_appwrite-worker-database
appwrite_appwrite
appwrite_appwrite-maintenance
appwrite_appwrite-worker-mails
appwrite_appwrite-worker-deletes
appwrite_appwrite-worker-audits
appwrite_appwrite-worker-builds
appwrite_appwrite-worker-certificates
appwrite_appwrite-realtime
appwrite_appwrite-worker-webhooks
appwrite_appwrite-schedule
appwrite/requestcatcher:1.0.0
redis:6.2-alpine
adminer
mariadb:10.7
appwrite/telegraf:1.4.0
appwrite/influxdb:1.5.0
appwrite/mailcatcher:1.0.0
```
So Appwrite is following a [microservices](https://dev.to/appwrite/30daysofappwrite-appwrite-s-building-blocks-1936) architectural pattern where multiple microservices are running separately as containers to collectlively form the Appwrite stack/service.

## Appwrite
We can now try to login to the Appwrite UI on the browser with the same IP we used to SSH into the instance. It should provide the signup page where we can create the account.
![Appwrite signup](https://cdn.hashnode.com/res/hashnode/image/upload/v1654920901564/m3rgsuhD8.png align="left")

So we have finally installed and launched Appwrite successfully on Linode. Thank you for reading :)

