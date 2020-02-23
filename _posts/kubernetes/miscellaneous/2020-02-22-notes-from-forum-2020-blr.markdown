---
title: kubernetes > notes from forum 2020 in bangalore, india
categories: kubernetes
---

I had the privilege of getting sponsored by the company for attending the Kubernetes forum 2020 in Bangalore, India. I wanted 
to save some information that I captured during the event, and I think this post serves that purpose. 

They had covered wide range of topics such as marketing, proposals, best practices, etc. 
Few of them were presented so well, some highlights that I remember are:
- The Minecraft example, by Don Kahn, on how Kubernetes is leveraging individual Linux tool kits such as IP tables, ETCD, 
cgroups, dns, etc. to make that consolidated super software
- What each upgrade of Kubernetes is trying to solve, I think version 1.16 was related to CRDs
- A deep dive on deep learning, kube flow on AWS
- Share of Kubernetes in Cloud, Seems 71% of the workloads are on Public cloud
- Evolution of cortex, grafana, index caching, query caching, Project Frankestein a.k.a Cortex etc. was quite technical though
- Use of multiple ingress controllers with a shared load balancer
- Containerization best practices, securing images, choice of CNI, use of kata containers
- The use of Link local IP addressing in Calico
- **session 12 on the youtube channel** => Nice promotion of Vitess(based on mysql). Vitess use cases, with JD.com, slack. Sugu Sukumaran said how they are able to cater both big giants and startups such as Nozzle. Nozzle wanted everything in the cloud in k8s and how migration from Azure to Google Cloud with a k8s supported database system, in an hour helped them. Each Vitess Pod seems to run an empty dir volume. The JD.com example was catchy - 40K keyspaces => 30K Pods => 35 M peak Qps
- **session 25 on the youtube channel** => A cool and audience friendly session covering kubectl tips and tricks
- Ways of contributing to CNCF, their slack channels, user groups, etc.

What else, nice food, big forum, proomotions, goodies, etc. It was more of an event eyeing human talent with Kubernetes skills

I might have misinterpreted some info though, however they have uploaded all the videos here - [CNCF YouTube channel](http://www.cvent.com/api/email/dispatch/v1/click/75xgx6jxqkcb4x/r4pnbq4q/aHR0cHMlM0ElMkYlMkZ3d3cueW91dHViZS5jb20lMkZwbGF5bGlzdCUzRmxpc3QlM0RQTGo2aDc4eXpZTTJNaWUzV1lVR19PanhnX1EwMWhJR3NVJldrN1BxNyUyQmx6VjhGeUdMcWxpZk1QbXcyZ3JwWUgzMVA4blozQ3NzazB5QSUzRCZDTkNGK1lvdVR1YmUrY2hhbm5lbA).

--end-of-post--
