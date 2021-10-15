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

We can also use Trivy check kubernetes configuration files and docker files for misconfiguration.
```
$ trivy config .
2021-08-20T14:27:48.418+0530	INFO	Need to update the built-in policies
2021-08-20T14:27:48.418+0530	INFO	Downloading the built-in policies...
2021-08-20T14:29:31.874+0530	INFO	Detected config files: 4

Dockerfile (dockerfile)
=======================
Tests: 23 (SUCCESSES: 23, FAILURES: 0, EXCEPTIONS: 0)
Failures: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)


juice-shop-deploy.yaml (kubernetes)
===================================
Tests: 28 (SUCCESSES: 17, FAILURES: 11, EXCEPTIONS: 0)
Failures: 11 (UNKNOWN: 0, LOW: 6, MEDIUM: 5, HIGH: 0, CRITICAL: 0)

+---------------------------+------------+----------------------------------------+----------+--------------------------------------------+
|           TYPE            | MISCONF ID |                 CHECK                  | SEVERITY |                  MESSAGE                   |
+---------------------------+------------+----------------------------------------+----------+--------------------------------------------+
| Kubernetes Security Check |   KSV001   | Process can elevate its own privileges |  MEDIUM  | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should set         |
|                           |            |                                        |          | 'securityContext.allowPrivilegeEscalation' |
|                           |            |                                        |          | to false                                   |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv001        |
+                           +------------+----------------------------------------+----------+--------------------------------------------+
|                           |   KSV003   | Default capabilities not dropped       |   LOW    | Container 'juice-shop' of Deployment       |
|                           |            |                                        |          | 'juice-shop' should add 'ALL' to           |
|                           |            |                                        |          | 'securityContext.capabilities.drop'        |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv003        |
+                           +------------+----------------------------------------+          +--------------------------------------------+
|                           |   KSV011   | CPU not limited                        |          | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should             |
|                           |            |                                        |          | set 'resources.limits.cpu'                 |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv011        |
+                           +------------+----------------------------------------+----------+--------------------------------------------+
|                           |   KSV012   | Runs as root user                      |  MEDIUM  | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should set         |
|                           |            |                                        |          | 'securityContext.runAsNonRoot' to true     |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv012        |
+                           +------------+----------------------------------------+----------+--------------------------------------------+
|                           |   KSV014   | Root file system is not read-only      |   LOW    | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should set         |
|                           |            |                                        |          | 'securityContext.readOnlyRootFilesystem'   |
|                           |            |                                        |          | to true                                    |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv014        |
+                           +------------+----------------------------------------+          +--------------------------------------------+
|                           |   KSV015   | CPU requests not specified             |          | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should             |
|                           |            |                                        |          | set 'resources.requests.cpu'               |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv015        |
+                           +------------+----------------------------------------+          +--------------------------------------------+
|                           |   KSV016   | Memory requests not specified          |          | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should             |
|                           |            |                                        |          | set 'resources.requests.memory'            |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv016        |
+                           +------------+----------------------------------------+          +--------------------------------------------+
|                           |   KSV018   | Memory not limited                     |          | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should             |
|                           |            |                                        |          | set 'resources.limits.memory'              |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv018        |
+                           +------------+----------------------------------------+----------+--------------------------------------------+
|                           |   KSV019   | Seccomp policies disabled              |  MEDIUM  | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should             |
|                           |            |                                        |          | specify a seccomp profile                  |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv019        |
+                           +------------+----------------------------------------+          +--------------------------------------------+
|                           |   KSV020   | Runs with low user ID                  |          | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should set         |
|                           |            |                                        |          | 'securityContext.runAsUser' > 10000        |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv020        |
+                           +------------+----------------------------------------+          +--------------------------------------------+
|                           |   KSV021   | Runs with low group ID                 |          | Container 'juice-shop' of                  |
|                           |            |                                        |          | Deployment 'juice-shop' should set         |
|                           |            |                                        |          | 'securityContext.runAsGroup' > 10000       |
|                           |            |                                        |          | -->avd.aquasec.com/appshield/ksv021        |
+---------------------------+------------+----------------------------------------+----------+--------------------------------------------+

juice-shop-svc.yaml (kubernetes)
================================
Tests: 28 (SUCCESSES: 28, FAILURES: 0, EXCEPTIONS: 0)
Failures: 0 (UNKNOWN: 0, LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0)


test/smoke/Dockerfile (dockerfile)
==================================
Tests: 23 (SUCCESSES: 21, FAILURES: 2, EXCEPTIONS: 0)
Failures: 2 (UNKNOWN: 0, LOW: 0, MEDIUM: 1, HIGH: 1, CRITICAL: 0)

+---------------------------+------------+--------------------+----------+------------------------------------------+
|           TYPE            | MISCONF ID |       CHECK        | SEVERITY |                 MESSAGE                  |
+---------------------------+------------+--------------------+----------+------------------------------------------+
| Dockerfile Security Check |   DS001    | ':latest' tag used |  MEDIUM  | Specify a tag in the 'FROM'              |
|                           |            |                    |          | statement for image 'alpine'             |
|                           |            |                    |          | -->avd.aquasec.com/appshield/ds001       |
+                           +------------+--------------------+----------+------------------------------------------+
|                           |   DS002    | root user          |   HIGH   | Specify at least 1 USER                  |
|                           |            |                    |          | command in Dockerfile with               |
|                           |            |                    |          | non-root user as argument                |
|                           |            |                    |          | -->avd.aquasec.com/appshield/ds002       |
+---------------------------+------------+--------------------+----------+------------------------------------------+
```

So, we have seen how to install Trivy and how to use it to scan the juice shop container image and 
check misconfigurations in files. Thank you for reading.

--end-of-post--
