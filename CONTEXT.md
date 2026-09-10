# CONTEXT.md — Advanced MLOps Assignment Tracker

> This file tracks all 26 parts of the assignment, what has been completed via code,
> and provides step-by-step instructions for parts requiring manual GitHub interaction.

---

## Repository Structure

```
student-ml-api/
├── app.py                          # FastAPI application (/health, /predict)
├── requirements.txt                # Pinned Python dependencies
├── VERSION                         # Semantic version (currently 1.0.0)
├── Dockerfile                      # Production Docker image config
├── .dockerignore                   # Excludes .git, __pycache__, etc.
├── tests/
│   └── test_app.py                 # 4 automated tests
├── .github/
│   └── workflows/
│       ├── ci.yml                  # CI pipeline (PR → test → Docker build check)
│       └── release.yml             # Release pipeline (tag → test → build → push)
└── CONTEXT.md                      # This file
```

---

## Part-by-Part Status & Instructions

### ✅ Part 1 — Create the Application (CODE COMPLETE)

- **app.py**: FastAPI app with `/health` and `/predict`
- `/health` → `{"status":"healthy","application":"student-ml-api","version":"1.0.0"}`
- `/predict` → accepts `{"value": N}`, returns `{"input": N, "prediction": N*2}`
- Version read dynamically from `VERSION` file

### ✅ Part 2 — Automated Tests (CODE COMPLETE)

- **tests/test_app.py** contains 4 tests:
  1. `test_health_endpoint` — verifies /health returns 200 + correct payload
  2. `test_predict_success` — verifies /predict with value=10 returns prediction=20
  3. `test_predict_missing_input` — verifies empty body → 422
  4. `test_predict_invalid_input` — verifies string value → 422
- Run: `pytest tests/ -v`

### 📋 Part 3 — Git Workflow (MANUAL STEPS)

```bash
# 1. Initialize repo (if not already)
git init
git add .
git commit -m "feat: initial project structure"

# 2. Create GitHub repo named "student-ml-api"
#    Go to https://github.com/new → create public repo (no README)

# 3. Connect and push to main
git remote add origin https://github.com/<YOUR_USERNAME>/student-ml-api.git
git branch -M main
git push -u origin main

# 4. Create feature branch for the prediction API
git checkout -b feature/prediction-api

# 5. Make meaningful commits
git add app.py VERSION requirements.txt
git commit -m "feat: add prediction endpoint with health check"

git add tests/
git commit -m "test: add API unit tests for health and predict endpoints"

git add Dockerfile .dockerignore
git commit -m "build: add Dockerfile and .dockerignore"

git add .github/
git commit -m "ci: add CI and release GitHub Actions workflows"

git add CONTEXT.md
git commit -m "docs: add assignment context tracking file"

# 6. Push feature branch
git push origin feature/prediction-api
```

### 📋 Part 4 — Pull Request Description (MANUAL STEPS)

Go to GitHub → your repo → "Compare & pull request"

Use this PR template:

```
## Summary
Initial implementation of the student-ml-api prediction service with complete CI/CD pipeline.

## Changes
- **app.py**: FastAPI application with `/health` and `/predict` endpoints
- **tests/test_app.py**: 4 automated tests (health, predict, missing input, invalid input)
- **Dockerfile**: Production-oriented container image with OCI labels
- **.dockerignore**: Excludes .git, __pycache__, .venv, etc.
- **ci.yml**: GitHub Actions CI pipeline for PRs (test + Docker build validation)
- **release.yml**: Automated release pipeline triggered by version tags

## Testing Performed
- All 4 pytest tests pass locally
- Docker image builds successfully (`docker build -t student-ml-api:1.0.0 .`)
- API health endpoint verified via curl

## Docker Impact
- Base image: `python:3.11-slim`
- Exposed port: 5000
- Layer-optimized for build caching (requirements first, then source)

## Checklist
- [x] Application runs locally
- [x] Tests pass locally
- [x] Docker image builds successfully
- [x] No credentials are committed
- [x] API health endpoint works
- [x] Code is ready for review
```

**DO NOT merge yet** — wait for CI to run.

### ✅ Part 5 — GitHub Actions CI (CODE COMPLETE)

- **ci.yml** triggers on `pull_request` to `main`
- Pipeline: Checkout → Python 3.11 → Install deps → pytest → Docker build (no push)

### 📋 Part 6 — Deliberate Failure (MANUAL STEPS)

```bash
# 1. On the feature/prediction-api branch, break a test:
#    In tests/test_app.py, change:
#      assert data["status"] == "healthy"
#    to:
#      assert data["status"] == "wrong"

# 2. Commit and push
git add tests/test_app.py
git commit -m "test: intentionally break health test for CI failure demo"
git push origin feature/prediction-api

# 3. Go to GitHub → observe the PR → CI should show ❌ FAILED
# 4. Take a screenshot of the failed workflow

# 5. Fix the test (change "wrong" back to "healthy")
git add tests/test_app.py
git commit -m "fix: correct health endpoint test"
git push origin feature/prediction-api

# 6. CI should now show ✅ PASSED
# 7. Take a screenshot of the passing workflow
```

### 📋 Part 7 — Branch Protection (MANUAL STEPS)

Go to: **GitHub → Settings → Branches → Add rule**

Configure for branch `main`:
- ✅ **Require a pull request before merging**
  - ✅ Require approvals (set to 0 if solo, 1 if team)
- ✅ **Require status checks to pass before merging**
  - Search and add: "Test & Validate" (the CI job name)
- ✅ **Do not allow bypassing the above settings**
- (Optional) ✅ Include administrators

**Document the settings you selected** — take a screenshot.

### 📋 Part 8 — Merge the Pull Request (MANUAL STEPS)

After CI passes:
1. Go to the PR on GitHub
2. Select **"Squash and Merge"**

**Justification**: Squash and merge combines all feature branch commits into a single clean commit on main, keeping the main branch history linear and readable while preserving the full development history in the PR.

### ✅ Part 9 — Dockerize the Application (CODE COMPLETE)

- **Dockerfile** follows best practices:
  - `FROM python:3.11-slim` (explicit version)
  - `WORKDIR /app`
  - `COPY requirements.txt` first → `pip install --no-cache-dir`
  - `COPY app.py .` and `COPY VERSION .`
  - `EXPOSE 5000`
  - `CMD ["uvicorn", ...]`
  - OCI labels via build args (Part 23)
- **.dockerignore** excludes `.git`, `__pycache__`, `.venv`, etc.

### 📋 Part 10 — Build Docker Image Locally (MANUAL STEPS)

```bash
# Build
docker build -t student-ml-api:1.0.0 .

# Run
docker run -d --name student-ml-api -p 5000:5000 student-ml-api:1.0.0

# Verify
curl http://localhost:5000/health
# Expected: {"status":"healthy","application":"student-ml-api","version":"1.0.0"}
```

### 📋 Part 11 — Docker Image Inspection (MANUAL STEPS)

```bash
# List images
docker images | grep student-ml-api

# List running containers
docker ps | grep student-ml-api

# View logs
docker logs student-ml-api

# Inspect container
docker inspect student-ml-api

# Execute shell inside container
docker exec -it student-ml-api sh

# Inside the container, verify:
# - Working directory: /app
# - ls to see app.py, VERSION, requirements.txt
# exit
```

**You must identify and document:**
- Container ID: (from `docker ps`)
- Image ID: (from `docker images`)
- Exposed port: 5000
- Running command: `uvicorn app:app --host 0.0.0.0 --port 5000`
- Working directory: `/app`

### 📋 Part 12 — Container Registry (MANUAL STEPS)

Using **GitHub Container Registry (GHCR)** (recommended):

```bash
# GHCR uses the GITHUB_TOKEN automatically in Actions.
# For local push, create a Personal Access Token (PAT) with `write:packages` scope.

# Login locally (optional, for manual testing)
echo "<YOUR_PAT>" | docker login ghcr.io -u <YOUR_USERNAME> --password-stdin

# Tag and push (optional manual step — release.yml handles this automatically)
docker tag student-ml-api:1.0.0 ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0
docker push ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0
```

### 📋 Part 13 — Git Tag and Release (MANUAL STEPS)

```bash
git checkout main
git pull origin main

# Create version tag
git tag v1.0.0

# Push tag → triggers release.yml workflow
git push origin v1.0.0
```

### ✅ Part 14 — Automated Release Workflow (CODE COMPLETE)

- **release.yml** triggers on `push tags: v*.*.*`

### ✅ Part 15 — Release Pipeline (CODE COMPLETE)

- Extracts version from tag: `${GITHUB_REF_NAME#v}` (no hard-coding)
- Pushes 3 tags: `<version>`, `latest`, `<commit-sha>`

### 📋 Part 16 — Registry Verification (MANUAL STEPS)

```bash
# After release workflow completes, verify on GitHub:
# Go to: https://github.com/<YOUR_USERNAME>?tab=packages

# Or via CLI:
docker pull ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0
docker inspect ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0 | grep -i digest

# Record the image digest (sha256:xxxx...)
```

### 📋 Part 17 — Artifact Reproducibility (MANUAL STEPS)

```bash
# Delete local image
docker rmi student-ml-api:1.0.0
docker rmi ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0

# Pull from registry
docker pull ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0

# Run
docker run -d --name student-ml-api-test -p 5000:5000 ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0

# Verify
curl http://localhost:5000/health
```

### 📋 Part 18 — Develop Version 1.1.0 (MANUAL STEPS)

```bash
# 1. Create feature branch
git checkout main
git pull
git checkout -b feature/model-metadata

# 2. Update VERSION file
echo "1.1.0" > VERSION

# 3. Update app.py — modify the health endpoint to return:
#    {
#      "status": "healthy",
#      "application": "student-ml-api",
#      "application_version": "1.1.0",
#      "model_version": "model-1"
#    }
#
#    Changes needed in app.py:
#    - Update HealthResponse model to include application_version and model_version
#    - Update the health() function to return the new fields
#    - Replace "version" with "application_version" in the response

# 4. Update tests to match new /health response

# 5. Commit
git add -A
git commit -m "feat: add model metadata to health endpoint"

# 6. Push and create PR
git push origin feature/model-metadata
# Create PR on GitHub with a professional description

# 7. Wait for CI → merge
```

**Updated app.py health endpoint for v1.1.0:**
```python
class HealthResponse(BaseModel):
    status: str
    application: str
    application_version: str
    model_version: str

@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="healthy",
        application="student-ml-api",
        application_version=APP_VERSION,
        model_version="model-1",
    )
```

**Updated test for v1.1.0:**
```python
def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["application"] == "student-ml-api"
    assert "application_version" in data
    assert data["model_version"] == "model-1"
```

### 📋 Part 19 — Release Version 1.1.0 (MANUAL STEPS)

```bash
git checkout main
git pull
git tag v1.1.0
git push origin v1.1.0
# release.yml triggers automatically
```

Verify registry contains: `1.0.0`, `1.1.0`, and `latest` (pointing to 1.1.0)

### 📋 Part 20 — Rollback Exercise (MANUAL STEPS)

```bash
# Stop the current container
docker stop student-ml-api
docker rm student-ml-api

# Pull and run the known-good version
docker pull ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0
docker run -d --name student-ml-api -p 5000:5000 ghcr.io/<YOUR_USERNAME>/student-ml-api:1.0.0

# Verify rollback
curl http://localhost:5000/health
# Should show version 1.0.0
```

**Why is this easier than git clone → pip install → python app.py?**

> Container-based rollback is a single `docker run` command using a pre-built,
> pre-tested, immutable artifact. There is no dependency installation, no build step,
> no risk of environment drift. The image is the exact same binary that was tested
> in CI — no rebuilding required. Traditional deployment requires cloning the right
> commit, installing dependencies (which may have changed or become unavailable),
> and configuring the runtime environment, all of which introduce failure points.

### 📋 Part 21 — Traceability Challenge (MANUAL STEPS)

For version 1.1.0, document:

| Item | Value |
|---|---|
| PR Number | #2 (your actual PR number) |
| Merge Commit SHA | (from `git log --oneline -1 v1.1.0`) |
| Git Tag | v1.1.0 |
| Docker Image | ghcr.io/<YOUR_USERNAME>/student-ml-api:1.1.0 |
| Image Digest | sha256:... (from `docker inspect`) |

### ✅ Part 22 — Workflow Separation (EXPLANATION)

**CI Workflow** (ci.yml):
- Runs on: Pull Requests to main
- Does: Test, Validate, Build-check
- Does NOT publish images

**Release Workflow** (release.yml):
- Runs on: Version tags (v*.*.*)
- Does: Test, Build, Version, Publish

**Why not publish Docker images from every PR?**
> Publishing from every PR would flood the registry with untested, unreviewed,
> potentially broken images. PRs represent work-in-progress — they haven't been
> code-reviewed or approved. Publishing only from tagged releases on main ensures
> images are traceable to reviewed, merged, and explicitly versioned code.

### ✅ Part 23 — Image Metadata / OCI Labels (CODE COMPLETE)

The Dockerfile includes OCI labels via build args:
- `org.opencontainers.image.version` — app version
- `org.opencontainers.image.revision` — git commit SHA
- `org.opencontainers.image.source` — repository URL
- `org.opencontainers.image.created` — build timestamp

Verify: `docker inspect <image> | grep -A10 Labels`

### ✅ Part 24 — Commit SHA Tag (CODE COMPLETE)

The release.yml pushes 3 tags:
- `student-ml-api:<version>` (e.g., 1.1.0)
- `student-ml-api:latest`
- `student-ml-api:<commit-sha>` (e.g., 92f4abc...)

**Benefit of commit-specific tags:**
> Commit SHA tags provide an unambiguous link from a running container back to the
> exact source code that produced it. Unlike version tags (which can be moved or
> reused), commit SHAs are immutable. This is critical for debugging production
> issues — you can instantly identify and inspect the exact code running in any
> environment.

### 📋 Part 25 — Docker Build Cache (EXPLANATION / MANUAL STEPS)

```bash
# 1. Build once (all layers cached)
docker build -t student-ml-api:cache-test .

# 2. Modify only app.py, rebuild
#    → requirements.txt layer is CACHED (reused)
#    → Only app.py COPY and later layers rebuilt

# 3. Modify requirements.txt, rebuild
#    → requirements.txt COPY invalidates cache
#    → pip install runs again (slow)
#    → app.py COPY also runs again
```

**Why `COPY requirements.txt` before `COPY app.py`?**

```dockerfile
# GOOD — requirements cached when only code changes
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
```

```dockerfile
# BAD — ANY file change invalidates pip install cache
COPY . .
RUN pip install -r requirements.txt
```

> Docker caches layers sequentially. If a layer changes, all subsequent layers are
> invalidated. Requirements change rarely; source code changes frequently.
> By copying requirements first, pip install is cached across most builds.
> Using `COPY . .` means ANY file change (even a comment in app.py) forces a
> full pip install, wasting CI time and bandwidth.

### 📋 Part 26 — Failure Analysis (MANUAL STEPS)

Reproduce and document **at least 2** of these failures:

#### Failure 1: Failed pytest

**Symptom**: `pytest` exits with non-zero code, test assertions fail.

**How to reproduce**:
```python
# In test_app.py, change:
assert data["status"] == "healthy"
# to:
assert data["status"] == "wrong"
```

**Root Cause**: Test assertion does not match actual API response.

**Evidence**: pytest output showing `AssertionError: assert 'healthy' == 'wrong'`

**Correction**: Fix the assertion to match the actual API response.

---

#### Failure 2: Wrong container port

**Symptom**: `curl http://localhost:5000/health` returns "Connection refused"

**How to reproduce**:
```bash
# Run container mapping to wrong port
docker run -d --name bad-port -p 8080:8080 student-ml-api:1.0.0
curl http://localhost:8080/health  # Connection refused
```

**Root Cause**: The app listens on port 5000 inside the container, but the container maps host port 8080 to container port 8080 (where nothing is listening).

**Evidence**: `docker logs bad-port` shows uvicorn running on port 5000. `docker port bad-port` shows `8080/tcp -> 0.0.0.0:8080`.

**Correction**: Use correct port mapping: `docker run -d -p 5000:5000 student-ml-api:1.0.0`

---

## Viva Preparation — Quick Answers

1. **Why avoid pushing directly to main?** — Bypasses code review, testing, and CI. Risk of breaking production.

2. **Purpose of a PR beyond merging?** — Code review, discussion, documentation of changes, CI validation, knowledge sharing.

3. **Why CI before merge?** — Catches bugs before they reach main. Prevents broken code from affecting other developers.

4. **Docker image vs container?** — Image is a read-only template (blueprint). Container is a running instance of an image.

5. **Why version Docker images?** — Enables rollback, traceability, reproducibility. Know exactly what's deployed.

6. **Why `latest` is insufficient?** — `latest` is mutable and doesn't indicate which version is running. Can't rollback, can't audit.

7. **Why promote artifacts, not rebuild?** — Rebuilding may produce different results (dependency updates, environment drift). Promoting ensures the exact tested artifact is deployed.

8. **Purpose of a container registry?** — Centralized storage and distribution of versioned container images. Enables any machine to pull and run the same artifact.

9. **CI vs release workflow?** — CI validates changes (test + build-check), runs on PRs. Release builds, versions, and publishes artifacts, runs on tags.

10. **Why store credentials as secrets?** — Prevents exposure in code, logs, or version history. Secrets are encrypted and scoped.

11. **How to identify which commit produced an image?** — OCI labels (`org.opencontainers.image.revision`), commit SHA tag, or `docker inspect`.

12. **Why does Docker layer ordering matter?** — Layers are cached sequentially. Frequently changing layers should be last to maximize cache reuse.

13. **How to rollback 1.1.0 → 1.0.0?** — `docker stop` current container, `docker run` with `student-ml-api:1.0.0` from registry.

14. **Git tag vs Docker tag?** — Git tag marks a source code point. Docker tag marks an image version. They're linked by the release workflow: `v1.0.0` git tag → `1.0.0` Docker tag.

15. **MLOps: independent app/model versioning?** — Need to track both versions together. A model update without code changes (or vice versa) requires separate versioning schemes and compatibility matrices.
