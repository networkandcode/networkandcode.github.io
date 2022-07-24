---
canonical_url: https://dev.to/aws-builders/nextjs-deployment-via-aws-codecommit-amplify-6oj
categories: amplify, aws, cicd, nextjs
date: 2022-03-19
tags: amplify, aws, cicd, nextjs
title: NextJS deployment via AWS CodeCommit / Amplify
---

*This post first appeared on [dev.to](https://dev.to/aws-builders/nextjs-deployment-via-aws-codecommit-amplify-6oj/edit)*


Hey All :wave:, Let's see how to add the NextJS starter code in an AWS CodeCommit repo and deploy it with AWS Amplify. I am using the [Cloud9](https://dev.to/aws-builders/run-svelte-app-on-aws-cloud9-4j5b) IDE :cloud: for this exercise. You may follow these steps on any Linux/Unix based machine though.

I am using [aws cli v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). You may upgrade the version if required. Also ensure you have setup the CLI with the required authentication config.

```
$ aws --version
aws-cli/2.4.27 Python/3.8.8 Linux/4.14.262-200.489.amzn2.x86_64 exe/x86_64.amzn.2 prompt/off
```

The user id I'm using has administrator permissions :fire:, so I shouldn't  have any issues while creating the repo. If not an admin, the IAM user should be setup with [CodeCommit policies] (https://docs.aws.amazon.com/codecommit/latest/userguide/security-iam-awsmanpol.html).

Let's go ahead and create the repo.
```
$ aws codecommit create-repository --repository-name next-js-boilerplate --repository-description "Boilerplate code for NextJS" --tag "code=JavaScript,framework=NextJS"
{
    "repositoryMetadata": {
        "accountId": "<account-id>",
        "repositoryId": "<repository-id>",
        "repositoryName": "next-js-boilerplate",
        "repositoryDescription": "Boilerplate code for NextJS",
        "lastModifiedDate": "2022-03-19T08:17:28.327000+00:00",
        "creationDate": "2022-03-19T08:17:28.327000+00:00",
        "cloneUrlHttp": "https://git-codecommit.us-east-2.amazonaws.com/v1/repos/next-js-boilerplate",
        "cloneUrlSsh": "ssh://git-codecommit.us-east-2.amazonaws.com/v1/repos/next-js-boilerplate",
        "Arn": "arn:aws:codecommit:us-east-2:<account-id>:next-js-boilerplate"
    }
}
```

The repo :file_folder: is created and should appear in the list of repositories.
```
$ aws codecommit list-repositories --output text
REPOSITORIES    <repository-id>    next-js-boilerplate
```
Can be checked on the AWS console too, on  the browser.
![List of repositories in CodeCommit](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8h7dgx0vxc77na1yef17.png)

We are going to connect to the repo via SSH for which we have to upload the SSH public key to the AWS user account. But before that you have to ensure the SSH key is  already generated. You may refer to this [link](https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-ssh-unixes.html) if you want to know how to  generate the SSH key pair. The public key in my system is at the standard location i.e. ~/.ssh/id_rsa.pub. 

Let's upload this key :key: and retrieve the public key id.
```
$ SSHPublicKeyId=$(aws iam upload-ssh-public-key --user-name nc --ssh-public-key-body file://~/.ssh/id_rsa.pub --output text --query SSHPublicKey.SSHPublicKeyId)
```

Setup SSH config, and modify its permission so that only the owner(current user) of the file can access it(Read + Write).
```
$ cat > ~/.ssh/config <<EOF
Host git-codecommit.*.amazonaws.com
 User $SSHPublicKeyId
 EOF

$ chmod 600 ~/.ssh/config
```

Let's get the GIT SSH URL and then clone it.
```
$  gitUrl=$(aws codecommit get-repository --repository-name next-js-boilerplate --query repositoryMetadata.cloneUrlSsh --output text)                                            

$ git clone $gitUrl
Cloning into 'next-js-boilerplate'...
warning: You appear to have cloned an empty repository.
```

We have successfully cloned the repository, lets add some code to it. We can use npx for bootstraping a NextJS project. You may [install nodejs/npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) ) if its not already present in your system
```
$ cd next-js-boilerplate/

$ npx create-next-app@latest
✔ What is your project named? … next-js-boilerpate
```

This installs the NextJS project, and  it also creates a sub directory with the same name, so let's move contents from the sub directory to the main directory.
```
$ mv next-js-boilerplate/.* .
$ mv next-js-boilerplate/* .

$ rmdir next-js-boilerplate/

$ ls -a
.   .eslintrc.json  .gitignore      node_modules  package-lock.json  public     styles
..  .git            next.config.js  package.json  pages              README.md
```

The code can now be pushed to the repo.
```
$ git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .eslintrc.json
        .gitignore
        README.md
        next.config.js
        package-lock.json
        package.json
        pages/
        public/
        styles/

$ git add .
$ git commit -m 'adding nextjs boiler plate code'

$ git push
```

We can verify this on the AWS console.
![NextJS Boilerplate code in AWS CodeCommit repo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/e95g7njj4un0zye6nxii.png)


:cool: we can now deploy this code via AWS Amplify, I am going to use the GUI for this.

Search for Amplify, create a new app, and then choose CodeCommit.
![Select the repo type, in Amplify](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dpw2zkiw8t1q532xgbh9.png)

The next step is as follows, to select the correct repo and branch.
![Select repo and branch in Amplify screen](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/s3za78x0q0cw9zishodv.png)

Jus continue to the final step with no changes, and deploy.
![Deploy screen in Amplify](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/97e7geq58eljfqeyzis9.png)

In a few minutes :stopwatch:, the app should be deployed. We should see the 4 stages(provision, build, deploy and verify) to  be successful. There should also be a testing stage, which we haven't used here, as no tests are written.
![Amplify stages](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/93g1v2l6lbxmhehi51ha.png)

You should now be able to view :arrow_forward: the application by clicking on the https link provided above.
![NextJS deployment preview via Amplify](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3jl9b365pjq2apahj5xc.png)
 
Thus, we have gone through some parts of CodeCommit and Amplify. CLI was used with CodeCommit, just to see the power of AWS CLI and I think many cloud operations are possible with it. Note that we can customize Amplify deployments with environment variables, build command modifications etc.

That's  it for now, :slightly_smiling_face: thanks for reading...