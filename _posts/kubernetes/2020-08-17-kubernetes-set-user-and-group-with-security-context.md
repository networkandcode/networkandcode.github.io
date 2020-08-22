---
title: kubernetes > set user and group with security context
categories: kubernetes
---

We are going to enhance security in a running container with the use of security context, by setting the user and group for running processes and filesystem in the container.

# Reference
https://kubernetes.io/docs/tasks/configure-pod-container/security-context/


# Prerequisites
You should know how Deployments and Pod volumes such as EmptyDir work.

# Deploy a node app
Lets deploy a node app using the manifest below.
```
$ cat deploy-nodeapp-with-security-context-user-group.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: basicnodeapp
spec:
  selector:
    matchLabels:
      app: node
  template:
    metadata:
      labels:
        app: node
    spec:
      volumes:
      - name: ed
        emptyDir: {}
      containers:
      - name: node
        image: s1405/basicnodeapp
        volumeMounts:
        - name: ed
          mountPath: /tmp/ed
...
```

```
$ kubectl create -f deploy-nodeapp-with-security-context-user-group.yaml
deployment.apps/basicnodeapp created
```

# Login to the container
```
$ kubectl get pods
NAME                            READY   STATUS    RESTARTS   AGE
basicnodeapp-648568547f-z28nl   1/1     Running   0          2m5s

$ kubectl exec -it basicnodeapp-648568547f-z28nl -- bash
root@basicnodeapp-648568547f-z28nl:/usr/src/app#
```

## Check the current user details
```
root@basicnodeapp-648568547f-z28nl:/usr/src/app# whoami
root
```
This shows you are logged in as root, its also evident from the from the container prompt that says root@.

## Check the id
```
root@basicnodeapp-648568547f-z28nl:/usr/src/app# id
uid=0(root) gid=0(root) groups=0(root)
```
uid refers to the user id of the user, gid refers to the primary group id of the user, groups stands for all the groups the user belongs to, in addition to the primary group.

So, the current container user is root, it's user id is 0, primary group id is also 0, the primary group name is root. And it doesnt belong to any additional groups.

## Processes
All the running processes will be owned the current user and its only group, which are both root
```
root@basicnodeapp-648568547f-z28nl:/usr/src/app# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  1.7 571908 36696 ?        Ssl  07:57   0:00 node server.js
root        14  0.0  0.1  18184  3304 pts/0    Ss   07:59   0:00 bash
root        22  0.0  0.1  36632  2692 pts/0    R+   08:02   0:00 ps aux
```

## New file
And any new files we create will also be owned by the current user root and its only group root.
```
root@basicnodeapp-648568547f-z28nl:/usr/src/app# touch /tmp/test-file

root@basicnodeapp-648568547f-z28nl:/usr/src/app# ls /tmp/ -l | grep test-file
-rw-r--r-- 1 root root    0 Aug 22 08:03 test-file
```
By default, as shown above, new files will get read write (rw-) permission for the user 'root', read only (r--) permission for the group 'root' and others.

## New file in the volume
Any new file in the volume will also be owned by the current user root and its only group root.
```
root@basicnodeapp-648568547f-z28nl:/usr/src/app# touch /tmp/ed/test-file
root@basicnodeapp-648568547f-z28nl:/usr/src/app# ls /tmp/ed -l
total 0
-rw-r--r-- 1 root root 0 Aug 22 08:06 test-file
```
Note that we have earlier mentioned /tmp/ed as the mount path in the container for the shared empty directory volume.

## Exit the container
```
root@basicnodeapp-648568547f-z28nl:/usr/src/app# exit
exit
```

# Set user and group using security context
We are now going to use the security context feature to set the running user / group.
## Non root user and group
Well as seen above, certain containers, run as root. 
Logging into a container as root may not be secure, as it can interact with sensitive files, hence we can change it to a 
nonroot user during runtime. We are going to slightly modify the deployment manifest as follows.
```
$ cat deploy-nodeapp-with-security-context-user-group.yaml
--TRUNCATED--
    spec:
      securityContext:
        runAsUser: 11000
        runAsGroup: 22000
        fsGroup: 33000
      volumes:
--TRUNCATED--
```
So we have added the securityContext to pod spec and have configured to run all the containers in the Pod as user id 11000 and group id 22000. Note that the extra parameter fsGroup is the supplementary group the user would belong to, and any new files in  the mounted volume will be owned by this group.

Let's delete the existing deployment and create a new one.
```
$ kubectl delete deploy --all
deployment.extensions "basicnodeapp" deleted

$ kubectl create -f deploy-nodeapp-with-security-context-user-group.yaml
deployment.apps/basicnodeapp created

$ kubectl get pods
NAME                            READY   STATUS    RESTARTS   AGE
basicnodeapp-5cd66b595b-pnrzr   1/1     Running   0          25s
```

## Test
Let's launch the shell of the new container and test.
```
 kubectl exec -it basicnodeapp-5cd66b595b-pnrzr -- bash
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$
```
It shows 'I have no name' above cause this use is not part of the /etc/passwd file, and we didnt not set it any name.
```
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ whoami
whoami: cannot find name for user ID 11000
```

### Id
```
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ id
uid=11000 gid=22000 groups=22000,33000
```
We see two groups, 22000 is the primary group and 33000 is the supplementary group

### Processes
```
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
11000        1  0.0  1.7 572184 36212 ?        Ssl  08:16   0:00 node server.js
11000       14  0.0  0.1  18284  3308 pts/0    Ss   08:18   0:00 bash
11000       22  0.0  0.1  36632  2832 pts/0    R+   08:24   0:00 ps aux
```
All the running processes are owned by the current user with uid 11000

### New file
```
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ ls /tmp -l | grep test-file
-rw-r--r-- 1 11000 22000    0 Aug 22 08:25 test-file
```
Any new file is owned by uid 11000 and the primary group id 22000. We were able to add a file to the /tmp directory, cause any user would have write permissions into it.
```
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ ls / -l | grep tmp
drwxrwxrwt   1 root root 4096 Aug 22 08:25 tmp
```

However, we wouldn't be able to modify any files in a directory such as /etc, that can only be written by root. This would have been possible if we logged in as root into the container.
```
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ ls / -l | grep etc
drwxr-xr-x   1 root root 4096 Aug 22 08:16 etc

I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ touch /etc/testfile
touch: cannot touch '/etc/testfile': Permission denied
```

### New file in the volume
```
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ ls /tmp/ -l | grep ed
drwxrwsrwx 2 root  33000 4096 Aug 22 08:16 ed

I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ ls /tmp/ -l | grep ed
drwxrwsrwx 2 root  33000 4096 Aug 22 08:31 ed

I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ ls /tmp/ed -l
total 0
-rw-r--r-- 1 11000 33000 0 Aug 22 08:31 test-file
```
The volume directory is owned by the root user, however its owned by the group 33000 as specified in fsGroup. And we know any new files including the ones in the volume would belong to the current user, but they will still be owned by the fsGroup. So the fsGroup parameter effectes only the volume mount path, and any files created in it.

```
I have no name!@basicnodeapp-5cd66b595b-pnrzr:/usr/src/app$ exit
exit
```

--end-of-post--





