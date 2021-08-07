---
title: owasp juice shop > scan container with trivy
categories: owasp juice shop
---

In this post, we would be using an opensource container scanning tool called Trivy, developed by 
Aquasecurity to scan the juice shop container image. You need to have some familiarity with jq to 
follow along.

Let's first install Trivy and its dependencies, I am using ubuntu, so the installation instructions 
may vary, if you are on a non debian system.

Install dependencies and update repos.
```
$ sudo apt-get update -y
$ sudo apt-get install wget apt-transport-https gnupg lsb-release -y
$ wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
$ echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
```

Update the system again, and install Trivy.
```
$ sudo apt-get update -y
$ sudo apt-get install trivy -y
```

Trivy should now be installed, we can check its version.
```
$ trivy -v
Version: 0.19.2
```

We can now scan the image in dockerhub.
```
$ trivy image bkimminich/juice-shop
---TRUNCATED---
------------------------------------------+
|               | CVE-2021-32804      |          |                   | 6.1.1, 5.0.6, 4.4.14, 3.2.2 | nodejs-tar: arbitrary File                   |
|               |                     |          |                   |                             | Creation/Overwrite vulnerability             |
|               |                     |          |                   |                             | via insufficient symlink protection          |
|               |                     |          |                   |                             | -->avd.aquasec.com/nvd/cve-2021-32804        |
+---------------+---------------------+----------+-------------------+-----------------------------+----------------------------------------------+
```

We can fetch the result in JSON to filter it with jq.
```
$ trivy image --format json --output /tmp/audit.json bkimminich/juice-shop
2021-08-07T17:55:14.342+0530	INFO	Detected OS: alpine
2021-08-07T17:55:14.343+0530	INFO	Detecting Alpine vulnerabilities...
2021-08-07T17:55:14.343+0530	INFO	Number of language-specific files: 2
2021-08-07T17:55:14.343+0530	INFO	Detecting npm vulnerabilities...
2021-08-07T17:55:14.378+0530	WARN	DEPRECATED: the current JSON schema is deprecated, check https://github.com/aquasecurity/trivy/discussions/1050 for more information.
```

The warning above w.r.t the JSON format can be overcome with an env variable TRIVY_NEW_JSON_SCHEMA.
```
$ TRIVY_NEW_JSON_SCHEMA=true trivy image --format json --output /tmp/audit.json bkimminich/juice-shop
2021-08-07T17:59:54.006+0530	INFO	Detected OS: alpine
2021-08-07T17:59:54.006+0530	INFO	Detecting Alpine vulnerabilities...
2021-08-07T17:59:54.007+0530	INFO	Number of language-specific files: 2
2021-08-07T17:59:54.007+0530	INFO	Detecting npm vulnerabilities...
```

We can parse this with jq. Lets try a few commands.
```
$ cat /tmp/audit.json | jq 'keys'
[
  "ArtifactName",
  "ArtifactType",
  "Metadata",
  "Results",
  "SchemaVersion"
]


$ cat /tmp/audit.json | jq '.Metadata'
{
  "OS": {
    "Family": "alpine",
    "Name": "3.11.11"
  },
  "RepoTags": [
    "bkimminich/juice-shop:latest"
  ],
  "RepoDigests": [
    "bkimminich/juice-shop@sha256:8abf7e5b28b5b0e3e2a88684ecac9dc9740643b46e17a4edc9fc16141289869b"
  ]
}

```

So, we have seen how to install Trivy and how to use it to scan the juice shop container image. Thank 
you for reading.

--end-of-post--
