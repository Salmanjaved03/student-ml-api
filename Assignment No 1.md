## Advanced MLOps Exercise

## Professional CI Workflow with Pull Requests, Docker, and Container Registry

## Objective

You are part of an engineering team responsible for an ML inference service. Your task is to establish a professional development workflow in which:

- Developers work on feature branches.

- Changes reach main only through Pull Requests.

- GitHub Actions automatically validates every Pull Request.

- The application is containerized using Docker.

- Docker images are built automatically after approved changes are merged.

- Versioned Docker images are published to a container registry.

- The complete workflow remains traceable from:

Pull Request → Commit → Git Tag → Docker Image

The exercise should be implemented as if the repository were being prepared for a real production MLOps project.

## Scenario

Your organization maintains a simple prediction API called:

```
student-ml-api
```

The API currently accepts a numeric input and returns a prediction.

The repository has the following intended structure:


```
├── tests/
│ └── test_app.py
│
└── .github/
└── workflows/
├── ci.yml
└── release.yml
```

Your team follows this development policy:

```
feature branch
↓
Pull Request
↓
Automated CI
↓
Code Review
↓
Merge into main
↓
Version Tag
↓
Docker Build
↓
Container Registry
```

Direct development on main is not permitted.

## Part 1 — Create the Application

Develop a Flask or FastAPI application containing at least the following endpoints.

## Health Endpoint

```
GET /health
```

Expected response:

```
{
"status": "healthy",
"application": "student-ml-api",
```


```
"version": "1.0.0"
}
```

## Prediction Endpoint

## POST /predict

Input:

```
{
"value": 10
}
```

Example output:

```
{
"input": 10,
"prediction": 20
}
```

You may implement a simple mathematical prediction for this exercise.

The objective is the MLOps workflow rather than ML model performance.

## Part 2 — Add Automated Tests

Create automated tests for at least:

- 1. /health

- 2. Successful /predict

- 3. Missing input

- 4. Invalid input

Example:

pytest

must successfully run all tests.


Your project should contain at least four automated tests.

## Part 3 — Establish a Professional Git Workflow

The repository must contain:

main

and development must occur through feature branches.

Create a branch:

```
git checkout -b feature/prediction-api
```

Implement the application.

Use meaningful commits such as:

```
git commit -m "feat: add prediction endpoint"
git commit -m "test: add API unit tests"
```

Push:

```
git push origin feature/prediction-api
```

Then create a Pull Request:

feature/prediction-api

↓

main

## Part 4 — Pull Request Requirements

The Pull Request must contain a professional description.


It must include:

Summary

Changes

Testing Performed

Docker Impact

Checklist

## Example checklist:

[ ] Application runs locally

[ ] Tests pass locally

[ ] Docker image builds successfully

[ ] No credentials are committed

[ ] API health endpoint works

[ ] Code is ready for review

The Pull Request should not be merged immediately.

CI must first run successfully.

## Part 5 — GitHub Actions CI

## Create:

.github/workflows/ci.yml

The CI workflow must run when:

Pull Request → main

and optionally on pushes to development branches.

The pipeline must contain at least the following jobs.


```
PR
|
+----> Code Checkout
|
+----> Python Setup
|
+----> Dependency Installation
|
+----> Unit Tests
|
+----> Docker Build Validation
```

The Docker image should be built during CI, but it should not yet be pushed to the registry.

## Required CI Behaviour

Only a successful pipeline should allow the PR to be considered ready for merging.

## Part 6 — Introduce a Deliberate Failure

Before merging, intentionally break one test.


For example:

```
assert data["status"] == "wrong"
```

Push the change.

Observe:

```
Pull Request
|
v
GitHub Actions
|
v
FAILED
```

Capture evidence of the failed workflow.

Then fix the problem:

```
assert data["status"] == "healthy"
```

Commit:

```
git commit -m "fix: correct health endpoint test"
```

Push again.

The workflow should now pass.

This demonstration is mandatory.

## Part 7 — Protect the Main Branch

Configure branch protection for:

```
main
```


## At minimum:

- Require Pull Request before merging.

- Require successful status checks.

- Prevent accidental direct development on main .

Students should determine the most appropriate GitHub settings.

Document the settings selected.

## Part 8 — Merge the Pull Request

## After:

```
Tests
Docker Build ✓
Review
```

merge the Pull Request into:

main

Use one of:

Merge Commit

Squash and Merge

Rebase and Merge

You must state which strategy you selected and briefly justify the decision.

## Part 9 — Dockerize the Application

Create a production-oriented Dockerfile .

Minimum requirements:

```
FROM python:<specific-version>
```


Do not use:

FROM python:latest

Your Dockerfile should demonstrate good Docker practices including:

- Explicit base-image version

- WORKDIR

- Dependency installation

- Correct COPY ordering

- --no-cache-dir

- EXPOSE

- Appropriate CMD

You must also create:

.dockerignore

It should exclude unnecessary files such as:

```
.git
.github
__pycache__
*.pyc
.venv
.env
```

## Part 10 — Build the Docker Image Locally

Create version:

1.0.0

inside:

VERSION

Build:


docker build -t student-ml-api:1.0.0 .

Run:

```
docker run -d
--name student-ml-api
-p 5000:5000
student-ml-api:1.0.0
```

Verify:

curl http://localhost:5000/health

The container must return the expected application version.

## Part 11 — Docker Image Inspection

Students must demonstrate the following commands:

docker images

docker ps

docker logs student-ml-api

docker inspect student-ml-api

docker exec -it student-ml-api sh

You must identify:

- Container ID

- Image ID

- Exposed port

- Running command

- Application working directory


## Part 12 — Container Registry

Use either:

GitHub Container Registry (GHCR)

or:

Docker Hub

GHCR is recommended.

The final image should resemble:

ghcr.io/<username>/student-ml-api:1.0.0

## Part 13 — Git Tag and Release Version

After the PR has been merged into main :

```
git checkout main
git pull
```

Create:

Push:

git push origin v1.0.0

The relationship should now be:

Git Tag

v1.0.0


```
|
v
Docker Image
student-ml-api:1.0.0
```

## Part 14 — Automated Release Workflow

## Create:

```
.github/workflows/release.yml
```

The workflow must run only when a semantic-version tag is pushed.

## Example:

```
v1.0.0
v1.1.0
v2.0.0
```

Trigger concept:

```
on:
push:
tags:
- "v*.*.*"
```

## Part 15 — Release Pipeline Requirements

Your release workflow must perform:

```
Version Tag
|
v
Checkout
|
v
Run Tests
```


```
|
v
Authenticate to Registry
|
v
Build Docker Image
|
v
Apply Version Tag
|
v
Push Docker Image
```

The registry must receive:

```
student-ml-api:1.0.0
```

and:

```
student-ml-api:latest
```

Both may refer to the same image.

## Important Constraint

The workflow must derive:

1.0.0

from:

v1.0.0

automatically.

Students must not manually hard-code:

```
version: 1.0.0
```


inside the workflow.

## Part 16 — Registry Verification

After pushing:

verify that the registry contains:

Record the image digest.

Example:

sha256:xxxxxxxxxxxxxxxxxxxx

## Part 17 — Prove Artifact Reproducibility

Delete the local Docker image:

Then retrieve it from the registry:

Run the downloaded image.

Verify:


```
curl http://localhost:5000/health
```

This demonstrates:

```
Build Machine
|
v
Container Registry
|
v
Different Runtime Environment
```

without rebuilding the application.

## Part 18 — Develop Version 1.1.0

Create another feature branch:

```
git checkout -b feature/model-metadata
```

Modify /health to return:

```
{
"status": "healthy",
"application": "student-ml-api",
"application_version": "1.1.0",
"model_version": "model-1"
}
```

Update tests.

Then repeat the complete professional process:

```
feature branch
↓
commits
↓
push
↓
Pull Request
```


```
↓
CI
↓
review
↓
merge
```

Do not bypass the PR workflow.

## Part 19 — Release Version 1.1.0

After merging:

```
git tag v1.1.0
git push origin v1.1.0
```

The registry should now contain:

```
student-ml-api:1.0.0
student-ml-api:1.1.0
student-ml-api:latest
```

Verify that:

```
latest → 1.1.0
```

while:

```
1.0.0
```

is still available.

## Part 20 — Rollback Exercise

Assume:


```
1.1.0
```

contains a production issue.

Without modifying the source code and without rebuilding an image, restore:

```
1.0.0
```

using the registry.

Expected solution concept:

```
Registry
|
+-- 1.0.0 ← known good
|
+-- 1.1.0 ← problematic
```

Run version:

```
1.0.0
```

again.

Verify its /health endpoint.

Explain why this is easier than a deployment process based on:

```
git clone
pip install
python app.py
```

## Part 21 — Traceability Challenge

For version 1.1.0 , students must document the complete chain:

```
Pull Request Number
↓
```


```
Merge Commit SHA
↓
Git Tag
↓
Docker Image Tag
↓
Docker Image Digest
```

## Example:

PR:

Merge Commit:

Git Tag:

Docker Image:

Image Digest:

The values must come from the student's actual repository.

#14

92f4abc

v1.1.0

student-ml-api:1.1.0

sha256:abcd...

## Part 22 — Advanced GitHub Actions Requirement

Separate the workflows conceptually.

## CI workflow

Runs on:

Pull Request

Responsibilities:

```
Test
Validate
Build-check
```

It must not publish a release artifact.

## Release workflow

Runs on:


Version Tag

Responsibilities:

Test

Build

Version

Publish

Students must explain why publishing Docker images directly from every Pull Request is usually undesirable.

## Part 23 — Advanced Challenge: Image Metadata

Add OCI labels during the Docker build so the image contains metadata such as:

```
Application version
Git commit
Repository
Build date
```

For example, the image should be traceable to the commit that produced it.

Verify using:

docker inspect

## Part 24 — Advanced Challenge: Commit SHA Tag

In addition to:

1.1.0

latest

automatically publish another image tag based on the Git commit.

Example:


```
student-ml-api:1.1.0
student-ml-api:latest
student-ml-api:92f4abc
```

Students must explain the benefit of a commit-specific image tag.

## Part 25 — Advanced Challenge: Docker Build Cache

Inspect the Docker build output.

Modify only:

```
app.py
```

Rebuild.

Determine which Docker layers were reused.

Then modify:

requirements.txt

and rebuild.

Compare the two builds.

Explain why:

```
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
```

is usually preferable to:

```
COPY . .
RUN pip install -r requirements.txt
```


## Part 26 — Failure Analysis

Students must deliberately reproduce and diagnose at least two of the following problems:

```
Failed pytest
Failed Docker build
Wrong container port
Application bound to 127.0.0.1
Invalid Docker registry credentials
Registry push denied
Incorrect image tag
Missing dependency
```

For each failure document:

Symptom

Root Cause

Evidence

Correction

## Submission Requirements

Each student/group must submit:

## 1. GitHub Repository

The repository must contain:

```
app.py
requirements.txt
Dockerfile
.dockerignore
VERSION
tests/
.github/workflows/ci.yml
.github/workflows/release.yml
```


## 2. Pull Requests

At least:

2 professionally documented PRs

must be visible in repository history.

## 3. GitHub Actions Evidence

Provide evidence of:

One failed CI execution

One successful CI execution

One successful release execution

## 4. Registry Evidence

Registry must contain at least:

1.0.0

1.1.0

latest

## 5. Release Tags

Repository must contain:

v1.0.0

v1.1.0

## 6. Demonstration

Students must demonstrate:

Clone repository

↓

Inspect Git history

↓

Inspect PR

↓

Inspect GitHub Action


```
↓
Pull image from registry
↓
Run container
↓
Test API
↓
Rollback
```

## Restrictions

The following approaches will result in loss of marks:

Directly pushing development work to main

Manually uploading Docker images

Hard-coding registry passwords in YAML

Using only the latest Docker tag

Creating Docker images manually instead of using the release workflow

Skipping automated tests

Creating a PR only after all work has already been merged

The GitHub history must demonstrate the intended workflow.

## Evaluation Rubric

| Component | Marks |
| --- | --- |
| Application implementation and tests | 10 |


| Component Marks Git branching and commit quality 10 Professional Pull Requests 10 |
| --- |
| GitHub Actions CI 15 |
| Dockerfile and containerization quality 15 Automated registry publishing 15 Semantic version/tag integration 10 Rollback and artifact reproducibility 5 Traceability 5 Failure analysis and explanation 5 Total 100 |

## Viva Questions

Students should be prepared to answer:

- 1. Why should developers avoid directly pushing to main ?

- 2. What is the purpose of a Pull Request beyond simply merging code?

- 3. Why should CI execute before a PR is merged?

- 4. What is the difference between a Docker image and a container?

- 5. Why should Docker images be versioned?

- 6. Why is latest insufficient for production traceability?

- 7. Why should the same Docker artifact be promoted rather than rebuilt?

- 8. What is the purpose of a container registry?

- 9. What is the difference between the CI workflow and release workflow?

- 10. Why should registry credentials be stored as secrets?

- 11. How can you identify which source-code commit produced a Docker image?

- 12. Why does Docker layer ordering affect CI/CD performance?

- 13. How would you rollback from version 1.1.0 to 1.0.0 ?

- 14. What is the relationship between a Git tag and a Docker image tag?

- 15. In an MLOps system, what additional problems arise when the application version and model version change independently?


## Expected Final Pipeline

```
Developer
|
v
Feature Branch
|
v
Commit + Push
|
v
Pull Request
|
v
+-----------------------+
| GitHub Actions CI |
| |
| Tests |
| Docker Build Check |
+-----------------------+
|
v
Review + Merge
|
v
main
|
v
Semantic Version Tag
v1.1.0
|
v
+-----------------------+
| Release Workflow |
| |
| Test |
| Docker Build |
| Registry Login |
| Image Tagging |
| Image Push |
+-----------------------+
|
v
Container Registry
|
+---- 1.0.0
```


```
|
+---- 1.1.0
|
+---- latest
```

## Core Principle

At the end of the exercise, students should be able to explain this statement:

Git manages the evolution of source code. Pull Requests control how changes enter the main branch. CI verifies those changes. Docker converts approved source code into a reproducible artifact. The container registry stores and distributes versioned artifacts that can later be delivered consistently to staging and production.
