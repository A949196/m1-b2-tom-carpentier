"""M1-B2 — API tests.

3 tests required (health, predict valid, predict invalid).
Bonus tests welcome (deterministic, info schema, etc.).
"""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    """/health returns 200 and the expected status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_health_returns_503_if_model_not_loaded(client: TestClient) -> None:
    """/health returns 503 if the model is not loaded."""
    from unittest.mock import patch

    with patch.object(client.app.state,"model", None):
        response = client.get("/health")
        assert response.status_code == 503

def test_predict_valid_payload(client: TestClient, valid_payload: dict) -> None:
    """/predict returns 200 with a well-formed response on valid input.

    TODO — Uncomment once /predict is implemented in app/main.py.
    """
    response = client.post("/predict", json=valid_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["prediction"] in (0, 1)
    assert 0.0 <= data["probability"] <= 1.0
    assert "request_id" in data
    assert "model_version" in data
    


def test_predict_missing_field_returns_422(
    client: TestClient, valid_payload: dict
) -> None:
    """/predict returns 422 on missing required field.

    TODO — Uncomment once /predict is implemented.
    """
    invalid = {k: v for k, v in valid_payload.items() if k != "loan_amnt"}
    response = client.post("/predict", json=invalid)
    assert response.status_code == 422
    assert "loan_amnt" in response.text

def test_info_exposes_version(client: TestClient) -> None:
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    required_keys = [
        "api_version", "model_version", "model_created_at", 
        "sklearn_version", "dataset_sha256", "metrics_holdout"
    ]
    for key in required_keys:
        assert key in data, f"Key {key} is missing in /info"
        assert data[key] is not None, f"Key {key} is None in /info"


# TODO — Add at least one bonus test (e.g. test_predict_is_deterministic)
def test_predict_is_deterministic(client: TestClient, valid_payload: dict) -> None:
    r1 = client.post("/predict", json=valid_payload).json()
    r2 = client.post("/predict", json=valid_payload).json()
    assert r1["prediction"] == r2["prediction"]
    assert r1["probability"] == r2["probability"]