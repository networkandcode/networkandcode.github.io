---
title: owasp juice shop > run the app locally
categories: owasp juice shop
---

OWASP juice shop is an open source AngularJS application developed with known vulnerabilities 
to aid with the process of learning cyber security. We are planning to write a series of topics 
with the juice shop app as base and use it to learn concepts such as CI/CD, Containerization etc.

In this post, we are going to clone the owasp juice shop, an opensource application from github 
and run it locally on a Linux system.

# Prerequisites
- Nodejs is installed
- NPM is installed
- Git is installed

Note that a standard version of NPM comes along with the installation of nodejs

# Check if Nodejs, NPM, and Git are Installed
This is an optional step to ensure the required packages are present in the machine.
The versions can slightly vary.
```
$ npm -v
6.14.13

$ node -v
v14.17.1

$ git --version
git version 2.25.1
```

# Clone the App
```
$ git clone https://github.com/bkimminich/juice-shop.git
```

# Change directory
```
$ cd juice-shop
```

# Check the contents
Optionally, you can check the contents of the directory to ensure the files are present in the 
directory
```
$ ls
app.json                 Dockerfile       monitoring                    SOLUTIONS.md
app.ts                   encryptionkeys   package.json                  swagger.yml
CODE_OF_CONDUCT.md       frontend         protractor.conf.js            test
config                   ftp              protractor.subfolder.conf.js  threat-model.json
config.schema.yml        Gruntfile.js     README.md                     tsconfig.json
CONTRIBUTING.md          HALL_OF_FAME.md  REFERENCES.md                 uploads
crowdin.yaml             i18n             routes                        vagrant
ctf.key                  lib              screenshots                   views
data                     LICENSE          SECURITY.md
docker-compose.test.yml  models           server.ts
```

# Install the modules
Install the node modules based on the contents in package.json. These modules would be required 
for the application to run. This step might take time according to the speed of the internet 
connection.

```
$ npm install
```

During the installation, you would be prompted, if you would like to share usage data, I have 
chosen Yes.
```
? Would you like to share anonymous usage data with the Angular Team at Google under
Google’s Privacy Policy at https://policies.google.com/privacy? For more details and
how to change this setting, see https://angular.io/analytics. Yes

Thank you for sharing anonymous usage data. If you change your mind, the following
command will disable this feature entirely:

    ng analytics off
```

At the end of the install command, you would see there are vulnerabilities in certain installed 
modules
```
found 20 vulnerabilities (3 low, 9 moderate, 5 high, 3 critical)
  run `npm audit fix` to fix them, or `npm audit` for details
```

The install stage has installed all modules in the node_modules directory.
```
$ ls | grep modules
node_modules
```

# Run the app
We can now run the app locally
````
$ npm start
```

If successful, we should get the following
```
info: Port 3000 is available (OK)
info: Server listening on port 3000
```

# Access the App
The app can now be accessed on the browser
![OWASP Juice Shop](/assets/owasp-juice-shop-home-page.png)

# Recap
So we saw how to clone the open source juice shop and deployed it locally on our system

--end-of-post--
