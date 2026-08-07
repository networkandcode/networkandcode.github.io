---
canonical_url: "https://dev.to/networkandcode/notes-app-with-nextjs-2l4g"
date: "2023-05-22"
title: "Notes app with NextJS"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fsource.unsplash.com%2Ffeatured%2F%3Fnote"
tags: "githubhack23, nextjs, auth0, harperdb"
categories: "githubhack23, nextjs, auth0, harperdb"
---
**This post first appeared on [dev.to](https://dev.to/networkandcode/notes-app-with-nextjs-2l4g)**

## What I built 
I developed a simple notes app with [NextJS](https://nextjs.org/) that authenticates via [Auth0](https://auth0.com/) and does CRUD operations via the API endpoints in NextJS to the database in [HarperDB](https://studio.harperdb.io/). This was deployed on [vercel](https://vercel.com/).

### Category Submission: 
Wacky Wildcards

### App Link
https://notes-app-pied-one.vercel.app/

### Screenshots 
Login:
![Login screen](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2vcc1wy96l047obk0i6w.png)

Auth0 login:
![Auth0 login](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/acgv134656vxxj0mfmxf.png)

Add note:
![Add note](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/u3pqdeu0omlbu0mel2m2.png)

View notes:
![View notes](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6ytqulpkldqx85hp4l0i.png)

Search:
![Search note](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5qq1xvwhcqwo9dnxyhll.png)

Edit or delete note:
![Edit or delete note](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mjr7rxmctsx7zpiszxj7.png)

### Description 
The app does the following:
- Let's the user signin with auth0
- Adds notes to the database created in HarperDB with the user's email
- Supports Editing or Deleting existing notes
- Search box in the homepage to filter notes

### Link to Source Code 
https://github.com/networkandcode/notes-app

### Permissive License 
MIT License

## Background (What made you decide to build this particular app? What inspired you?) 
I have the habit of taking notes while on calls at work or while watching or reading learning content. I mostly use notepad and save those notes in the localdrive, sometimes I also save notes on google docs, or as files in my github repo. This is a simple utility which I think can be used atleast by me for writing some short notes on web and use it anywhere. Secondly I wanted to participate atleast with anything simple as it's sometime now.

### How I built it (How did you utilize GitHub Actions or GitHub Codespaces? Did you learn something new along the way? Pick up a new skill?) 
I have used GitHub Codespaces initially for writing code for this project. I realised it had certain functionalities like AWS Cloud9. However Codespaces seems to be like VS code on the web, shortcuts like Ctrl b(hide or show folder), Ctrl j(Terminal toggle), Ctrl [ or ] for indentation, all seem working. I am yet to explore GitHub actions, I am guessing it could help setting up workflows or CI/CD pipelines for the code in the repo.

Here is a screenshot from codespaces:
![Codespaces](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9poac85boewuvun4hgi2.png)



### Additional Resources/Info
I followed this [quick start](https://auth0.com/docs/quickstart/webapp/nextjs/01-login) for integrating Auth0 with NextJS. The env vars related to HarperDB can be obtained from the config section of the studio. The list of environment variable names are added to [.env.example](https://github.com/networkandcode/notes-app/blob/main/.env.example). The sample notes used for testing where generated with ChatGPT. And I logged in with the google signin to test.

This app was lint checked with strict mode:
```
% npm run lint

> notes-app@1.0.0 lint
> next lint

- info Loaded env from /Users/networkandcode/notes-app/.env.local
✔ No ESLint warnings or errors
```
Image credit [unsplash](https://source.unsplash.com/featured/?note)

## Update:
I have tried github actions with an example [docker workflow](https://github.com/networkandcode/notes-app/blob/main/.github/workflows/docker.yml) provided in the actions page, for which I used this [dockerfile](https://github.com/networkandcode/notes-app/blob/main/dockerfile)

The workflow ran successfuly and an image was pushed [here](https://github.com/networkandcode/notes-app/pkgs/container/notes-app)

This image is public, and I can now use docker to pull and try running this on codespaces.
```
$ docker pull ghcr.io/networkandcode/notes-app:main

$ docker run -d -p 3000:3000 --env-file .env.local ghcr.io/networkandcode/notes-app:main
551c561623dcefe5dc26b4762bc8806ca018a863ff8ad728d213cd861c882d16

$ docker ps
CONTAINER ID   IMAGE                                   COMMAND                  CREATED          STATUS          PORTS                                       NAMES
551c561623dc   ghcr.io/networkandcode/notes-app:main   "docker-entrypoint.s…"   46 seconds ago   Up 44 seconds   0.0.0.0:3000->3000/tcp, :::3000->3000/tcp   elated_newton
```

I could now access the application on the codespaces url that's port forwared to localhost:3000.
![App preview with docker](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ocs9ik3vyrkykftq93cc.png). There are many more examples in the workflow actions, and I think it would be worth trying to extend the workflow to deploy directly to a kubernetes once the image is built.
