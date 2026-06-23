import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome to TrainPulse API" in response.json()["message"]

def test_get_kpis():
    response = client.get("/analytics/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "attendance_rate" in data
    assert "completion_rate" in data

def test_predict_completion():
    payload = {
        "attendance_rate": 0.8,
        "pretest_score": 50,
        "durasi_hari": 3
    }
    response = client.post("/predict/completion", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "probability" in data
    assert "status_lulus" in data
    assert "label" in data
