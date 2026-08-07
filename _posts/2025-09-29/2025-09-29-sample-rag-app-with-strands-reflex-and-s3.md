---
canonical_url: "https://dev.to/aws-builders/sample-rag-app-with-strands-reflex-and-s3-4n6m"
date: "2025-09-29"
title: "🚀 Sample RAG app with Strands, Reflex and S3"
cover_image: "https://media2.dev.to/dynamic/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fplmpseutf6t7krfzwt79.webp"
tags: "aws, rag, vectordatabase, llm"
categories: "aws, rag, vectordatabase, llm"
---
**This post first appeared on [dev.to](https://dev.to/aws-builders/sample-rag-app-with-strands-reflex-and-s3-4n6m)**

Hi :wave:, these are some setup instructions for the app that lets store some notes for subjects 📚 in S3 as vectordb and query it with Strands. You may checkout the code [here](https://github.com/networkandcode/studynotes).

First goto S3 >> Vector buckets, and create a vector bucket there and give it some name such as *studynotes*.

Create an index there with dimension *1024*, this is going to be the size of the embedding vector.

Let's now clone the app and switch the directory.
```bash
git clone https://github.com/networkandcode/studynotes.git
cd studynotes
```

So we now have the following for our `.env` file, add it here.
```bash
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION="us-west-2"
AWS_S3_VECTOR_BUCKET_NAME=studynotes
AWS_S3_VECTOR_INDEX_NAME=books
```

*Note that its using nova micro in the app for the LLM calls, so make sure it's allowed in Bedrock.*

⚡ Run the app with uv/reflex.
```bash
uv run reflex run

Creating virtual environment at: .venv

App running at: http://localhost:3000/
Backend running at: http://0.0.0.0:8000
```

You can now access the app at http://localhost:3000/.


A few screenshots below.

## Home page
![Home page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/183u2jwmg0mqilwser22.png)

## Subjects
![Subjects page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q5usmgtmn3tektkaffdk.png)

## Upload notes
![Notes page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/en5jp0mhhc68g4lz6thf.png)

## Chat
![Chat page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/s71em8qqellrnex21v5a.png)

Ok, so that's it for the post. This was done mainly to see how we can use S3 vector with python for RAG. The code related to S3 vector operations is in this [file](https://github.com/networkandcode/studynotes/blob/4dc9682d6db0b63c8aac7fb1fa3edce76a1553eb/s3_vectors.py). The app may not be perfect yet, needs some improvement.
