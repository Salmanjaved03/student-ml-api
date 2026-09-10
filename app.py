"""
student-ml-api: A simple ML prediction API for MLOps workflow demonstration.
"""

import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Read version from VERSION file
VERSION_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION")
try:
    with open(VERSION_FILE, "r") as f:
        APP_VERSION = f.read().strip()
except FileNotFoundError:
    APP_VERSION = "unknown"


app = FastAPI(title="student-ml-api", version=APP_VERSION)


class PredictRequest(BaseModel):
    """Request model for the prediction endpoint."""
    value: float = Field(..., description="Numeric input value for prediction")


class PredictResponse(BaseModel):
    """Response model for the prediction endpoint."""
    input: float
    prediction: float


class HealthResponse(BaseModel):
    """Response model for the health endpoint."""
    status: str
    application: str
    version: str


@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint returning application status and version."""
    return HealthResponse(
        status="healthy",
        application="student-ml-api",
        version=APP_VERSION,
    )


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Prediction endpoint.
    Applies a simple 2x multiplier model to the input value.
    """
    prediction = request.value * 2
    return PredictResponse(
        input=request.value,
        prediction=prediction,
    )
