# ---- Production Dockerfile for student-ml-api ----
# Uses explicit base-image version (not :latest)
FROM python:3.11-slim

# OCI image metadata labels (Part 23)
ARG APP_VERSION=unknown
ARG GIT_COMMIT=unknown
ARG BUILD_DATE=unknown
ARG REPO_URL=unknown

LABEL org.opencontainers.image.title="student-ml-api" \
      org.opencontainers.image.version="${APP_VERSION}" \
      org.opencontainers.image.revision="${GIT_COMMIT}" \
      org.opencontainers.image.source="${REPO_URL}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.description="ML prediction API for Advanced MLOps exercise"

# Set working directory
WORKDIR /app

# Install dependencies first (layer caching — requirements change less often than code)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .
COPY VERSION .

# Expose the API port
EXPOSE 5000

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
