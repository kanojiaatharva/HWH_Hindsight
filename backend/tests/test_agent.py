import pytest
from fastapi.testclient import TestClient
from main import app
from models import IncidentReport, IncidentFeedback

client = TestClient(app)

def test_get_incidents():
    response = client.get("/api/incidents")
    assert response.status_code == 200
    incidents = response.json()
    assert isinstance(incidents, list)
    assert len(incidents) > 0 # Seed data should be loaded

def test_diagnose_memory_enabled():
    report = {
        "description": "Getting 502 errors on prod-api.",
        "services": ["prod-api"],
        "memory_enabled": True
    }
    response = client.post("/api/diagnose", json=report)
    assert response.status_code == 200
    data = response.json()
    assert "pattern_match" in data
    assert "recommended_fix" in data
    # When memory is enabled, the mock fallback (or groq) returns failed approaches
    assert "failed_approaches" in data

def test_diagnose_memory_disabled():
    report = {
        "description": "Getting 502 errors on prod-api.",
        "services": ["prod-api"],
        "memory_enabled": False
    }
    response = client.post("/api/diagnose", json=report)
    assert response.status_code == 200
    data = response.json()
    assert "pattern_match" in data

def test_feedback_loop():
    feedback = {
        "incident_id": "INC-0047",
        "is_correct": False,
        "correction": "Needed to clear redis cache too."
    }
    response = client.post("/api/feedback", json=feedback)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
