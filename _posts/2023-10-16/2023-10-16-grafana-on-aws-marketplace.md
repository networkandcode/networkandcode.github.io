---
canonical_url: "https://dev.to/aws-builders/grafana-on-aws-marketplace-3189"
date: "2023-10-16"
title: "Grafana on AWS Marketplace"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fsource.unsplash.com%2Ffeatured%2F%3Fchart"
tags: "aws, devops, sre, cloud"
categories: "aws, devops, sre, cloud"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/grafana-on-aws-marketplace-3189)**

Hi there :wave:, We will see how to launch Grafana cloud from [AWS](https://grafana.com/products/cloud/marketplaces/aws-marketplace/) in an easy way, with no installation etc. Cool thing is it comes with a free trial :sunglasses: which should help us play on Grafana and learn about it's various visualization styles. In this post, we won't be building any graphs, to start with, we would just see a basic panel type which would help us creating links to other dashboards.

## Marketplace
Let's see how to launch Grafana from AWS Marketplace.
![Marketplace icon](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/urbu59pr3qsgo754bduk.png)
 Goto market place and click on discover products.
![Discover products link](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ggblgvdqlepz8xp01hcs.png)

Search for grafana cloud and click on the appropriate link.
![Grafana cloud](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/z7qprjr84jua77bloj76.png)

There is a free trial option, so I am clicking on Try for Free and Create Contract in the next step.

Clicking on Setup your Account would redirect to Grafana cloud URL where we can signup or link an existing account and create an organization. I have linked my existing account and chosen an existing organization.

Alright, we are all set to get started. You should be on the grafana organization URL with this format `https://grafana.com/orgs/<organization-name>`. On this page, click Add Stack to add your first stack.
![Add stack](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/uzud3z3srd83k4k7h2gj.png)

You can choose an instance URL and region for your stack. It should take a few minutes for the stack to launch. Your stack should have an instance URL in this format `https://<instance-name>.grafana.net`. You may sign in to this instance to see a page like this:![Grafana cloud](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tb2lfs7m3xyw58b62uov.png)

## Folder
Let's go to `Home > Dashboards` and create new folder with name `dummy-folder`.
![New folder](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/akfwn38dlb5j0su4y77b.png)

Inside this folder I am going to create a new dashboard.
![New dashboard](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/glxjghjipwwbg04vv2fq.png)
Goto settings name it `dummy-dashboard-1` and give it a tag `kubernetes`.
![Name and tag dashboard](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7zh05mgomy492mataxf8.png)
Then, save the dashboard.

Go back to the folder and create other dashboards similarly so that you have the following dashboards with tags `kubernetes`, `kafka` and `sql`:
![List of dashboards](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dbaniuxr2rwrgay4q5rb.png)

## Dashboard list
Goto `Home > Dashboards` and Create a new dashboard. Close the datasource selection window and click `Add a visualization`. Choose Dashboard List as the visualization type on the top right corner.
![Choose Dashboard list](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/okjfu2vg7lo69qalr5n8.png)

Give the panel a title such as `dashboard-list-all`.
![Panel title](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/pi9mnn5khcxjqmlqgxi9.png)

Scroll down, enable the `search` option, choose the folder as `dummy-folder` and leave the tags option empty like below.
![No tags selected](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5sg6xtlydlncdvzvasxm.png)

On the preview window on the left, it should show all the dashboards in the `dummy-folder`.
![All dashboards](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/z444a4wn22gvmiaoeo4c.png)

Save the panel, and save the dashboard with the name `dashboard-list`. You should see something like this:
![dashboard list all panel](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q6pzrlzpyujevd8viq0u.png)

Click on the three dots on the panel, and duplicate the panel by clicking on the appropriate option like shown below.
![Duplicate panel](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zjhxd69da2swcaxmh7ne.png)

Click on the three dots on the new panel, and edit it.
![Edit panel](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0vncs9ozivwxxdsk5khg.png)

Give this new panel, the title `dashboard-list-kubernetes` and add a tag `kubernetes`.
![Kubernetes tag](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xjpg505ltlh6rrpvlnkn.png)

Easy enough, the preview should now only show dashboards that are tagged with `kubernetes`, i.e. dashboards 1 to 3.
![dashboard list for kubernetes](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mkkj6koovf0zbwicn0n7.png)

Save the panel and repeat the steps for `kafka` and `sql`. So, finally you should see something like below.
![All panels](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/eqme3cvw6kgqrio76p6u.png)

## About tags
One thing to note, the tags we add in the panel are searched with `AND` condition. Meaning you will not see any dashboards if you added multiple tags like `kubernetes`, `kafka`, `sql`. Because, each of our dashboards had only one tag. For this purpose let's add a 10th dashboard with all 3 tags inside the `dummy-folder`.
![dashboard with all 3 tags](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y1j31aivbvbqoz6ks915.png)

And edit the dashboard-list-all panel to search for these 3 tags.
![dashboard-list-all-panel](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q4ihcwspz5tztkk4yae6.png)

![tags in dashboard list all](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vb362xt6no5tejffl0zr.png)

The dashboard should now look like this.
![Final dashboard](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rpxtsar0zqcblqi41a4z.png)

## Summary
So we have to seen how to launch Grafana cloud from AWS as a subscription, with free trial. Built some dummy dashboards on Grafana cloud and saw how to build panels with visualization type `Dashboard list` with the search folder and tags option, and played a bit with the tags.
