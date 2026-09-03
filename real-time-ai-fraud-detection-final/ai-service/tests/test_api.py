from fastapi.testclient import TestClient

from app.main import app


def test_health_does_not_claim_model_is_loaded():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert "model_loaded" in response.json()


def test_invalid_prediction_is_rejected_before_inference():
    with TestClient(app) as client:
        short_response = client.post("/predict", json={"text": "x"})
        blank_response = client.post("/predict", json={"text": "     "})
    assert short_response.status_code == 422
    assert blank_response.status_code == 422
