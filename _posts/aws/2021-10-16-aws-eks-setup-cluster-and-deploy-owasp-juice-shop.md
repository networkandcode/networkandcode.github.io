---
categories: aws eks
title: aws eks > setup cluster and deploy owasp juice shop
---

Let's setup an EKS cluster and then install the 
[OWASP Juice Shop](https://networkandcode.github.io/owasp/juice/shop/2021/07/23/owasp-juice-shop-run-the-app-locally.html) on it using kubernetes manifests.

# Manifest
Here is the manifest file, that contains the spec for our [deployment](https://networkandcode.github.io/2019/04/02/kubernetes-deployment/) and 
[service](https://networkandcode.github.io/2019/09/04/kubernetes-expose-pods-using-services/).
```
┌─[nc@parrot]─[/tmp]
└──╼ $cat juice-shop.yaml 
kind: Deployment
apiVersion: apps/v1
metadata:
  name: juice-shop
spec:
  template:
    metadata:
      labels:
        app: juice-shop
    spec:
      containers:
      - name: juice-shop
        image: bkimminich/juice-shop
  selector:
    matchLabels:
      app: juice-shop
---
kind: Service
apiVersion: v1
metadata:
  name: juice-shop
spec:
  type: NodePort
  selector:
    app: juice-shop
  ports:
  - name: http
    port: 8000
    targetPort: 3000
```

# Kubectl
Let's install kubectl on the local machine, as we would need it to interact with the kubernetes cluster.
```
┌─[nc@parrot]─[/tmp]
└──╼ $curl -sO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

Verify checksum for the downloaded kubectl.
```
┌─[nc@parrot]─[/tmp]
└──╼ $curl -sO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"

┌─[nc@parrot]─[/tmp]
└──╼ $echo "$(<kubectl.sha256) kubectl" | sha256sum --check
kubectl: OK
```

It says OK which means the checksum is correct. Let's do rest of the installation now.
```
─[✗]─[nc@parrot]─[/tmp]
└──╼ $sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
[sudo] password for nc: 

┌─[nc@parrot]─[/tmp]
└──╼ $which kubectl
/usr/local/bin/kubectl

┌─[nc@parrot]─[/tmp]
└──╼ $kubectl version --client
Client Version: version.Info{Major:"1", Minor:"22", GitVersion:"v1.22.2", GitCommit:"8b5a19147530eaac9476b0ab82980b4088bbc1b2", GitTreeState:"clean", BuildDate:"2021-09-15T21:38:50Z", GoVersion:"go1.16.8", Compiler:"gc", Platform:"linux/amd64"}
```

We have successfully installed kubectl. We can now remove kubectl and the checksum file from the tmp directory as we no longer need those.
```
┌─[nc@parrot]─[/tmp]
└──╼ $rm kubectl*
```

# AWS CLI
We are going to launch a cluster in AWS EKS, we can do this via CLI. For that purpose, we need to install the 
[aws cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install) and eksctl.

Start with aws cli.
```
─[nc@parrot]─[/tmp]
└──╼ $curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"

┌─[nc@parrot]─[/tmp]
└──╼ $unzip awscliv2.zip 

┌─[✗]─[nc@parrot]─[/tmp]
└──╼ $sudo ./aws/install
You can now run: /usr/local/bin/aws --version

┌─[nc@parrot]─[/tmp]
└──╼ $aws --version
aws-cli/2.2.46 Python/3.8.8 Linux/5.10.0-6parrot1-amd64 exe/x86_64.parrot.4 prompt/off

```

AWS CLI is installed, so we can remove the files we downloaded.
```
┌─[✗]─[nc@parrot]─[/tmp]
└──╼ $rm -rf aws*
```

# IAM
We would need an access key to issue AWS commands, for which let's add an IAM user first, you need to vist this 
[URL](https://console.aws.amazon.com/iam/home#/users$new?step=details) it would look like 
![Add IAM User](/assets/aws-eks-setup-cluster-and-deploy-owasp-juice-shop-1.png)

On the next page, you can create a group, if there isnt one. ![Add IAM Group](/assets/aws-eks-setup-cluster-and-deploy-owasp-juice-shop-2.png)

I am going to create a group for the Administrators with the AdministratorAccess policy.
![Administrator Access](/assets/aws-eks-setup-cluster-and-deploy-owasp-juice-shop-3.png)

The user can now be mapped to the Administrators group. ![Map Group](/assets/aws-eks-setup-cluster-and-deploy-owasp-juice-shop-4.png)

I would be skipping the tags stage and finally create the user.![Create User](/assets/aws-eks-setup-cluster-and-deploy-owasp-juice-shop-5.png)

Once the user is created you could retreive the access key id and secret access key from the final page, just copy those. 
We can cd to the home dir now, and create the .aws directory.
```
┌─[nc@parrot]─[/tmp]
└──╼ $cd ~

┌─[nc@parrot]─[~]
└──╼ $mkdir .aws
```

We just need to create the credentials file in the .aws directory, and store the access key id and secret access key retrieved earlier. So that it looks like the 
following, note that the file below has dummy values. Check this [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for reference.
```
┌─[nc@parrot]─[~]
└──╼ $cat .aws/credentials 
[default]
aws_access_key_id=AKIAIOSFODNN7EXAMPLE
aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

# EKSCTL
So we have done the essential settings for the AWS CLI. Let's now continue with 
[eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html) installation.
```
┌─[nc@parrot]─[~]
└──╼ $curl -s "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

┌─[nc@parrot]─[~]
└──╼ $sudo mv /tmp/eksctl /usr/local/bin/eksctl
[sudo] password for nc: 

┌─[nc@parrot]─[~]
└──╼ $

┌─[nc@parrot]─[~]
└──╼ $eksctl version
0.70.0
```

Hmm done enough :sweat_smile:, let's now launch an EKS cluster
```
$ eksctl create cluster \
--name my-cluster \
--region us-west-2 \
--fargate
```

Take a break here:coffee:, I have seen this step taking a bit longer...

For more cluster customizations, you may visit the 
[EKS getting started guide](https://docs.aws.amazon.com/eks/latest/userguide/getting-started.html).

# Kubeconfig
Let's check the list of clusters using 
[aws eks cli](https://docs.aws.amazon.com/cli/latest/reference/eks/index.html). We need to specify the 
region or configure the default region prior to listing. In my case its us-west-2.
```
┌─[✗]─[nc@parrot]─[~]
└──╼ $aws eks list-clusters --region us-west-2
{
    "clusters": [
        "my-cluster"
    ]
}
```

There is only one cluster as shown above. We shall update the kubeconfig, so that we can use kubectl 
to interact with our aks cluster.
```
┌─[nc@parrot]─[~]
└──╼ $aws eks update-kubeconfig --name my-cluster --region us-west-2
Added new context arn:aws:eks:us-west-2:<account-id>:cluster/my-cluster to /home/nc/.kube/config
```

We can now start using kubectl, lets validate the context first.
```
─[nc@parrot]─[~]
└──╼ $kubectl config current-context
arn:aws:eks:us-west-2:<account-id>:cluster/my-cluster
```

The cluster nodes should be ready.
```
┌─[nc@parrot]─[~]
└──╼ $kubectl get nodes
NAME                                                   STATUS   ROLES    AGE     VERSION
fargate-ip-192-168-126-75.us-west-2.compute.internal   Ready    <none>   6m19s   v1.20.7-eks-135321
fargate-ip-192-168-177-91.us-west-2.compute.internal   Ready    <none>   6m16s   v1.20.7-eks-135321
```

# Deploy
It's time to create the kubernetes deployment and service for juice shop.
```
$ kubectl create -f /tmp/juice-shop.yaml 
deployment.apps/juice-shop created
service/juice-shop created
```

The pod should be up in some time.
```
┌─[nc@parrot]─[~]
└──╼ $kubectl get po
NAME                          READY   STATUS    RESTARTS   AGE
juice-shop-699c69578f-qmd8m   1/1     Running   0          34m
```

Let's check its events.
```
┌─[✗]─[nc@parrot]─[~]
└──╼ $kubectl describe po juice-shop-699c69578f-qmd8m | grep -A 15 Events:
Events:
  Type     Reason           Age   From               Message
  ----     ------           ----  ----               -------
  Warning  LoggingDisabled  37m   fargate-scheduler  Disabled logging because aws-logging configmap was not found. configmap "aws-logging" not found
  Normal   Scheduled        36m   fargate-scheduler  Successfully assigned default/juice-shop-699c69578f-qmd8m to fargate-ip-192-168-109-122.us-west-2.compute.internal
  Normal   Pulling          36m   kubelet            Pulling image "bkimminich/juice-shop"
  Normal   Pulled           35m   kubelet            Successfully pulled image "bkimminich/juice-shop" in 33.837789722s
  Normal   Created          35m   kubelet            Created container juice-shop
  Normal   Started          35m   kubelet            Started container juice-shop
```

All seems good so far, let's now see if the endpoints are ok.
```
┌─[✗]─[nc@parrot]─[~]
└──╼ $kubectl get ep juice-shop
NAME         ENDPOINTS              AGE
juice-shop   192.168.109.122:3000   38m
```

And this IP should be of our juice shop pod.
```
┌─[nc@parrot]─[~]
└──╼ $kubectl get po -o wide | grep 192.168.109.122
juice-shop-699c69578f-qmd8m   1/1     Running   0          39m   192.168.109.122   fargate-ip-192-168-109-122.us-west-2.compute.internal   <none>           <none>
```

As per the manifest the service should be functional on port 8000. Let's validate.
```
┌─[nc@parrot]─[~]
└──╼ $kubectl get svc juice-shop
NAME         TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
juice-shop   NodePort   10.100.201.210   <none>        8000:32741/TCP   41m
```

We can now expose the service on localhost, using the port forwarding functionality of kubectl.
```
┌─[nc@parrot]─[~]
└──╼ $kubectl port-forward svc/juice-shop 8080:8000
Forwarding from 127.0.0.1:8080 -> 3000
Forwarding from [::1]:8080 -> 3000

```

The application should now be accessible on port 8080.
![OWASP Juice Shop](/assets/aws-eks-setup-cluster-and-deploy-owasp-juice-shop-6.png)

# Clean up
You can press Ctrl C on the terminal to stop the port forwarding, which stops the application on the browser.
You can delete the kubernetes objects using the delete command
```
$ kubectl delete -f /tmp/juice-shop.yaml
```

And finally when you are done, if you wish to delete the cluster, you may do so as follows.
```
┌─[nc@parrot]─[~]
└──╼ $eksctl delete cluster --name hacktoberfest-2021 --region us-west-2
```

--end-of-post--
