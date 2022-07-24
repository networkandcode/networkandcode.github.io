---
title: Install HarperDB on Linode
canonical_url: https://networkandcode.hashnode.dev/install-harperdb-on-linode
categories: docker, harperdb, linode, linux
date: 2022-06-13
tags: categories: docker, harperdb, linode, linux
---

*This post first appeared on [hashnode.dev](https://networkandcode.hashnode.dev/install-harperdb-on-linode)*

Hi... let's see how to install HarperDB with Docker on a Linux machine running on Linode. HarperDB is a NoSQL DB that also supports SQL style queries. It can be installed in various ways and we shall be installing it the Docker way, in this post.

## Instance
I launched an instance on Linode with the following spec.

```
Name: harperdb


Summary:
1 CPU Core, 50 GB Storage, 2 GB RAM

Plan:
Linode 2 GB

Region:
Mumbai, IN
```

Please refer to this [post](https://networkandcode.hashnode.dev/install-appwrite-on-linode) for instructions on SSH keys and installation of Docker.

## Hostname
Then I logged in to the instance on it's public IP via SSH, and changed the hostname.
```
root@localhost:~# hostname harperdb
```

## Add user
I have added a user harperdb.
```
root@harperdb:~# adduser harperdb
Adding user `harperdb' ...
Adding new group `harperdb' (1000) ...
Adding new user `harperdb' (1000) with group `harperdb' ...
Creating home directory `/home/harperdb' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for harperdb
Enter the new value, or press ENTER for the default
        Full Name []:
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] Y
```

This would also generate a group with the same name.
```
root@harperdb:~# id harperdb
uid=1000(harperdb) gid=1000(harperdb) groups=1000(harperdb)
```

## Add to group
Let's now add this to the docker group.
```
root@harperdb:~# usermod -aG docker harperdb
```

## Run
Login as the harperdb user and now run the docker command to install HarperDB. Different command line arguments are provided [here](https://hub.docker.com/r/harperdb/harperdb).
```
harperdb@harperdb:~$ docker run -d  -e HDB_ADMIN_USERNAME=HDB_ADMIN   -e HDB_ADMIN_PASSWORD=password  -p 9925:9925 harperdb/harperdb 
```
The container should be running.
```
harperdb@harperdb:~$ docker container ls
CONTAINER ID   IMAGE               COMMAND              CREATED         STATUS         PORTS                                       NAMES
eb3364e372ed   harperdb/harperdb   "tini -- harperdb"   8 minutes ago   Up 8 minutes   0.0.0.0:9925->9925/tcp, :::9925->9925/tcp   modest_raman
```

## API
Let's try a rest [API](https://api.harperdb.io/) call via CURL and see if it works.
```
harperdb@harperdb:~$  curl -u HDB_ADMIN -X POST 'http://localhost:9925' --header 'Content-Type: application/json'  --data-raw '{
    "operation": "create_schema",
    "schema": "dev"
}'
Enter host password for user 'HDB_ADMIN':
{"message":"schema 'dev' successfully created"}
```

## Remote
Let's try to delete  this schema, this time from a remote machine, where we need to replace localhost with the public IP of the HarperDB instance.
```
$  curl -u HDB_ADMIN -X POST 'http://<public-ip>:9925' --header 'Content-Type: application/json'  --data-raw '{
    "operation": "drop_schema",
    "schema": "dev"
}'
Enter host password for user 'HDB_ADMIN':
{"message":"successfully deleted schema 'dev'"}
```

In a similar manner we could send these rest API calls to HarperDB from client or server SDKs such as fetch, axios etc. instead of CURL and integrate it with our application. Thank you for reading :)