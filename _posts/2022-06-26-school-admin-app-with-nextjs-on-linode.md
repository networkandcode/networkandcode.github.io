---
date: 2022-06-26
canonical_url: https://networkandcode.hashnode.dev/school-admin-app-with-nextjs-on-linode
categories: linode, nextjs, tailwindcss, typescript
tags: linode, nextjs, tailwindcss, typescript
title: School admin app with NextJS on Linode
---

*This post first appeared on [hashnode.dev](https://networkandcode.hashnode.dev/school-admin-app-with-nextjs-on-linode)*

## Introduction
Hi 👋, in this post we shall see how to deploy a school management web app with some fundamental functionalities, on Linode, and then see some screenshots from the running app. You may click [here](https://github.com/networkandcode/sms) to check the GitHub repo.

## Instance
Let's launch an instance on Linode. Go to this [link](https://cloud.linode.com/linodes/create) and create an instance with the following spec.
```
Ubuntu 
2 CPU Cores, 80 GB Storage 4 GB RAM

Plan: Linode 4 GB
Region: Mumbai, IN
```

## Hostname
SSH into the instance as root user with either password or SSH key as relevant, and change the hostname which should be effective from next login.
```
root@localhost:~# hostname  sms
```

## Node
Let's install [nodejs](https://github.com/nodejs/help/wiki/Installation) on our system.
```
root@sms:~#  wget https://nodejs.org/dist/v18.4.0/node-v18.4.0-linux-x64.tar.xz
root@sms# tar -xvJf node-v18.4.0-linux-x64.tar.xz -C /usr/local/lib/nodejs
root@sms# rm node-v18.4.0-linux-x64.tar.xz
```

## Add a user
Add a new user, so that we can do rest of the operations as that user
```
# adduser sms
Adding user `sms' ...
Adding new group `sms' (1000) ...
Adding new user `sms' (1000) with group `sms' ...
Creating home directory `/home/sms' ...
Copying files from `/etc/skel' ...
New password:
Retype new password:
passwd: password updated successfully
Changing the user information for sms
Enter the new value, or press ENTER for the default
        Full Name []:
        Room Number []:
        Work Phone []:
        Home Phone []:
        Other []:
Is the information correct? [Y/n] Y
```
Once the user is added, you may exit the shell and relogin as new user.

## Sudo
We can add the new user to the sudo group, to run commands that may require sudo privileges.
```
root@sms:~# usermod -aG sudo sms
```
We can validate using the id command.
```
root@sms:~# id sms
uid=1000(sms) gid=1000(sms) groups=1000(sms),27(sudo)
```
So the user sms belongs to two groups sms and sudo.

## Path
Update path to access node and npm.
```
sms@sms:~$ export PATH=/usr/local/lib/nodejs/node-v18.4.0-linux-x64/bin:$PATH
sms@sms:~ .  ~/.profile
```

Validate.
```
sms@sms:~$ node -v
v18.4.0
sms@sms:~$ npm -v
8.12.1
```

## Clone
Clone the code from  github.
```
sms@sms:~$ git clone https://github.com/networkandcode/sms.git
```

## Backend
I have used [Appwrite](https://networkandcode.hashnode.dev/install-appwrite-on-linode) for authentication, and [HarperDB](https://networkandcode.hashnode.dev/install-harperdb-on-linode) as database. You may click on the respective hyperlinks for instructions to set up those on Linode.

## Appwrite
Update  the platform settings on Appwrite, to allow requests from the client, you can either use the IP or domain. In this case I can use the public IP of the instance we have launched in this post.
![Platform settings](https://cdn.hashnode.com/res/hashnode/image/upload/v1656177416027/ov-xFqXoq.png align="left")

## Variables
Change directory and set the environment variables.
```
sms@sms:~$ cd sms
sms@sms:~/sms$ cat .env
APPWRITE_API_KEY=<value>
HARPERDB_URL=<value>
HARPERDB_USERNAME=<value>
HARPERDB_PASSWORD=<value>
NEXT_PUBLIC_APPWRITE_SUPER_ADMINS=<value>
NEXT_PUBLIC_APPWRITE_EMAIL_VERIFICATION_URL=<value>
NEXT_PUBLIC_APPWRITE_ENDPOINT=<value>
NEXT_PUBLIC_APPWRITE_NEW_MEMBER_URL=<value>
NEXT_PUBLIC_APPWRITE_PROJECT_ID=<value>
```
Please replace <value> with actual values.

## Install
We can install all the modules defined in package.json using  npm.
```
sms@sms:~/sms$ npm i
npm WARN deprecated querystring@0.2.0: The querystring API is considered Legacy. new code should use the URLSearchParams API instead.

added 300 packages, and audited 301 packages in 7s

79 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
npm notice
npm notice New minor version of npm available! 8.12.1 -> 8.13.1
npm notice Changelog: https://github.com/npm/cli/releases/tag/v8.13.1
npm notice Run npm install -g npm@8.13.1 to update!
npm notice
```

So there are no vulnerabilties as per the output above. We can also try npm audit.
```
sms@sms:~/sms$ npm audit
found 0 vulnerabilities
```

## Dev
First, let's run it in development mode.
```
sms@sms:~/sms$ npm run  dev

> sms@0.1.0 dev
> next dev

ready - started server on 0.0.0.0:3000, url: http://localhost:3000
info  - Loaded env from /home/sms/sms/.env
wait  - compiling...
event - compiled client and server successfully in 2.9s (212 modules)
Attention: Next.js now collects completely anonymous telemetry regarding usage.
This information is used to shape Next.js' roadmap and prioritize features.
You can learn more, including how to opt-out if you'd not like to participate in this anonymous program, by visiting the following URL:
https://nextjs.org/telemetry
```

The website should now be available on port 3000, we can check it on the browser with the public IP of the instance.

Once logged in, you should see a screen like below.
![Home screen](https://cdn.hashnode.com/res/hashnode/image/upload/v1656225817326/rre27Heks.png align="left")

For the first time, when logged in as super admin, the generate tables link at the bottom can be clicked, to generate tables in HarperDB.

Press Ctrl ^ C to stop the running application.

## Build
Now we can make a build and run it.

```
sms@sms:~/sms$ npm run build
sms@sms:~/sms$ npm run start

> sms@0.1.0 start
> next start

ready - started server on 0.0.0.0:3000, url: http://localhost:3000
info  - Loaded env from /home/sms/sms/.env
```
The app can be accessed again on the same URL on port 3000.

## Screenshots
Here are some screenshots from the app.

### Authentication
![Signup](https://cdn.hashnode.com/res/hashnode/image/upload/v1656222329569/f7r2rGfkg.png align="left")

![Login](https://cdn.hashnode.com/res/hashnode/image/upload/v1656222363925/CVKxwEf2o.png align="left")

### Screens visible for Admins
![Classes](https://cdn.hashnode.com/res/hashnode/image/upload/v1656221269852/KjxH2ZWiK.png align="left")

![Class](https://cdn.hashnode.com/res/hashnode/image/upload/v1656221214177/acZeAGZvp.png align="left")

![Class students](https://cdn.hashnode.com/res/hashnode/image/upload/v1656222821792/fBe7mD_QS.png align="left")

![Class attendance](https://cdn.hashnode.com/res/hashnode/image/upload/v1656222923838/2A92fTPwf.png align="left")

![Class timetable](https://cdn.hashnode.com/res/hashnode/image/upload/v1656221701407/Pz5O_6Bl4.png align="left")

![Exam score](https://cdn.hashnode.com/res/hashnode/image/upload/v1656223094365/HMKW2ztH-.png align="left")

![Teams](https://cdn.hashnode.com/res/hashnode/image/upload/v1656222096881/Qri87V2Cd.png align="left")

![Team members](https://cdn.hashnode.com/res/hashnode/image/upload/v1656223895315/XxBUZebA6.png align="left")

### Screens visible for parents
![Home screen for parent](https://cdn.hashnode.com/res/hashnode/image/upload/v1656222584587/IYMKnehkS.png align="left")

![Profile](https://cdn.hashnode.com/res/hashnode/image/upload/v1656224814592/EKzA3-t85.png align="left")

![Children](https://cdn.hashnode.com/res/hashnode/image/upload/v1656224995274/3wgtIie1N.png align="left")

Clicking on the timetable would redirect to the screen shown in the admin section earlier.

## Security
We are now using 3 instances on Linode.

![instances](https://cdn.hashnode.com/res/hashnode/image/upload/v1656226856640/fV8PPQsqk.png align="left")

We have been using port 3000 for the NextJS app, 80 for Appwrite and 9925 for HarperDB. So let's create firewalls on Linode and restrict access.
![Create firewall](https://cdn.hashnode.com/res/hashnode/image/upload/v1656226828582/qzNYbAltw.png align="left")

I would be creating 3 firewall rules.

For Appwrite
![Appwrite firewall rule](https://cdn.hashnode.com/res/hashnode/image/upload/v1656228109564/h5V55qMZO.png align="left")

For HarperDB
![HarperDB firewall rule](https://cdn.hashnode.com/res/hashnode/image/upload/v1656228055129/OAPCcUfrT.png align="left")

For the NextJS app
![sms firewall rule](https://cdn.hashnode.com/res/hashnode/image/upload/v1656228005578/vFs8V-IXY.png align="left")

I have mentioned the source as all though, which could be changed to allow only specific IPs.

## Endnote
The app has some fundamental uses and the logic can be expanded further to include various features such as holiday management, file sharing, etc..

The app can also be deployed as a container on a VM or on linode’s kubernetes engine.

Thanks for reading !!!

Image credit: [unsplash](https://unsplash.com)