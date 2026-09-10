"""
Automated tests for the student-ml-api application.

Covers:
  1. Health endpoint returns correct status
  2. Successful prediction with valid input
  3. Missing input (empty body)
  4. Invalid input (string instead of number)
"""

import sys
import os

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


# ---------- Test 1: Health endpoint ----------
def test_health_endpoint():
    """Verify /health returns 200 with correct payload."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["application"] == "student-ml-api"
    assert "version" in data


# ---------- Test 2: Successful prediction ----------
def test_predict_success():
    """Verify /predict returns correct prediction for valid input."""
    response = client.post("/predict", json={"value": 10})
    assert response.status_code == 200
    data = response.json()
    assert data["input"] == 10
    assert data["prediction"] == 20  # 10 * 2


# ---------- Test 3: Missing input ----------
def test_predict_missing_input():
    """Verify /predict returns 422 when body is empty / missing 'value' field."""
    response = client.post("/predict", json={})
    assert response.status_code == 422


# ---------- Test 4: Invalid input ----------
def test_predict_invalid_input():
    """Verify /predict returns 422 when 'value' is not a number."""
    response = client.post("/predict", json={"value": "not_a_number"})
    assert response.status_code == 422
