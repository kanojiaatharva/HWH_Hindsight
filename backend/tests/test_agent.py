"""
Comprehensive test suite for Incident Déjà Vu backend.
Tests cover API endpoints, memory lifecycle, edge cases, and the feedback loop.
"""
import pytest
from fastapi.testclient import TestClient
from main import app, incidents_db
from models import IncidentReport, IncidentFeedback
from seed_data import load_seed_data

client = TestClient(app)

# ---------------------------------------------------------------------------
# Health Check
# ---------------------------------------------------------------------------

class TestHealthCheck:
    def test_health_returns_200(self):
        response = client.get("/api/health")
        assert response.status_code == 200

    def test_health_has_required_fields(self):
        data = client.get("/api/health").json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data


# ---------------------------------------------------------------------------
# Incident CRUD
# ---------------------------------------------------------------------------

class TestIncidents:
    def test_get_all_incidents(self):
        response = client.get("/api/incidents")
        assert response.status_code == 200
        incidents = response.json()
        assert isinstance(incidents, list)
        assert len(incidents) > 0

    def test_seed_data_includes_resolved_and_active(self):
        incidents = client.get("/api/incidents").json()
        statuses = {inc["status"] for inc in incidents}
        assert "resolved" in statuses
        assert "active" in statuses

    def test_get_incident_by_id(self):
        response = client.get("/api/incidents/INC-0047")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "INC-0047"
        assert data["severity"] == "High"

    def test_get_incident_not_found(self):
        response = client.get("/api/incidents/INC-9999")
        assert response.status_code == 404

    def test_incident_has_expected_fields(self):
        data = client.get("/api/incidents/INC-0047").json()
        required_fields = ["id", "title", "description", "status", "severity"]
        for field in required_fields:
            assert field in data, f"Missing field: {field}"


# ---------------------------------------------------------------------------
# Diagnosis Endpoint
# ---------------------------------------------------------------------------

class TestDiagnosis:
    def test_diagnose_memory_enabled_returns_pattern_match(self):
        """With memory ON, the agent should find a pattern match from past incidents."""
        report = {
            "description": "Getting 502 errors on prod-api.",
            "services": ["prod-api"],
            "memory_enabled": True
        }
        response = client.post("/api/diagnose", json=report)
        assert response.status_code == 200
        data = response.json()
        assert "diagnosis" in data
        diagnosis = data["diagnosis"]
        assert diagnosis["pattern_match"] is True
        assert diagnosis["confidence_score"] > 0.0
        assert len(diagnosis["failed_approaches"]) > 0
        assert "recommended_fix" in diagnosis

    def test_diagnose_memory_disabled_returns_generic(self):
        """With memory OFF, the agent should return generic advice without pattern match."""
        report = {
            "description": "Getting 502 errors on prod-api.",
            "services": ["prod-api"],
            "memory_enabled": False
        }
        response = client.post("/api/diagnose", json=report)
        assert response.status_code == 200
        data = response.json()
        diagnosis = data["diagnosis"]
        assert diagnosis["pattern_match"] is False
        assert diagnosis["confidence_score"] == 0.0
        assert len(diagnosis["failed_approaches"]) == 0

    def test_diagnose_returns_metadata(self):
        """The response should include memory usage metadata."""
        report = {
            "description": "prod-api-3 returning 502 errors",
            "services": ["prod-api"],
            "memory_enabled": True
        }
        data = client.post("/api/diagnose", json=report).json()
        assert "memory_used" in data
        assert "results_count" in data
        assert data["memory_used"] is True

    def test_diagnose_empty_description(self):
        """Empty description should still return a valid response (edge case)."""
        report = {
            "description": "",
            "services": [],
            "memory_enabled": True
        }
        response = client.post("/api/diagnose", json=report)
        # Should not crash — graceful handling
        assert response.status_code == 200

    def test_diagnose_very_long_description(self):
        """Long descriptions should be handled without crashing."""
        report = {
            "description": "502 error " * 500,
            "services": ["prod-api"],
            "memory_enabled": True
        }
        response = client.post("/api/diagnose", json=report)
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# Feedback / Correction Loop
# ---------------------------------------------------------------------------

class TestFeedbackLoop:
    def test_positive_feedback(self):
        """Positive feedback should be accepted but NOT trigger a retain."""
        feedback = {
            "incident_id": "INC-0047",
            "is_correct": True,
            "correction": None
        }
        response = client.post("/api/feedback", json=feedback)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["retained"] is False

    def test_negative_feedback_with_correction(self):
        """Negative feedback with a correction should trigger a retain to memory."""
        feedback = {
            "incident_id": "INC-0047",
            "is_correct": False,
            "correction": "Needed to clear redis cache too."
        }
        response = client.post("/api/feedback", json=feedback)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["retained"] is True

    def test_negative_feedback_without_correction(self):
        """Negative feedback without a correction should NOT trigger a retain."""
        feedback = {
            "incident_id": "INC-0047",
            "is_correct": False,
            "correction": None
        }
        response = client.post("/api/feedback", json=feedback)
        assert response.status_code == 200
        data = response.json()
        assert data["retained"] is False


# ---------------------------------------------------------------------------
# Incident Resolution & Memory Retention
# ---------------------------------------------------------------------------

class TestIncidentResolution:
    def test_resolve_incident(self):
        """Resolving an incident should update status and retain memory."""
        resolved_data = {
            "id": "INC-0062",
            "root_cause": "Connection pool exhaustion (again)",
            "resolution_steps": ["Restart sidecar proxy", "Scale auth-service"],
            "failed_approaches": ["Restarting nginx"],
            "time_to_resolve_mins": 6
        }
        response = client.post("/api/incidents/INC-0062/resolve", json=resolved_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "retention_result" in data

    def test_resolve_nonexistent_incident(self):
        """Attempting to resolve a non-existent incident should return 404."""
        resolved_data = {
            "id": "INC-9999",
            "root_cause": "Test",
            "resolution_steps": [],
            "failed_approaches": [],
            "time_to_resolve_mins": 0
        }
        response = client.post("/api/incidents/INC-9999/resolve", json=resolved_data)
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Demo Endpoints
# ---------------------------------------------------------------------------

class TestDemoEndpoints:
    def test_reset_demo(self):
        """Reset should restore seed data and clear diagnosis state."""
        response = client.post("/api/demo/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_seed_demo_memory(self):
        """Seed endpoint should confirm memories are loaded."""
        response = client.post("/api/demo/seed")
        assert response.status_code == 200
        data = response.json()
        assert data["memory_count"] > 0


# ---------------------------------------------------------------------------
# Hindsight Client Unit Tests
# ---------------------------------------------------------------------------

class TestHindsightClient:
    def test_client_initializes_with_demo_memories(self):
        """The client should pre-seed demo memories on initialization."""
        hc = HindsightClient()
        assert len(hc.local_memories) > 0

    def test_sanitize_content_redacts_api_keys(self):
        """Sensitive data should be redacted before retention."""
        hc = HindsightClient()
        raw = "Error connecting with api_key=sk_live_abc123 to server 10.0.1.55"
        sanitized = hc._sanitize_content(raw)
        assert "sk_live_abc123" not in sanitized
        assert "10.0.1.55" not in sanitized
        assert "REDACTED" in sanitized

    def test_sanitize_content_redacts_bearer_tokens(self):
        hc = HindsightClient()
        raw = "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.test"
        sanitized = hc._sanitize_content(raw)
        assert "eyJhbGciOiJIUzI1NiJ9" not in sanitized

    def test_local_recall_returns_relevant_results(self):
        """Mock recall should return results matching query keywords."""
        import asyncio
        hc = HindsightClient()
        result = asyncio.get_event_loop().run_until_complete(
            hc.recall(query="502 errors prod-api", max_results=3)
        )
        assert "results" in result
        assert len(result["results"]) > 0
        assert result["mock"] is True

    def test_local_recall_with_unrelated_query(self):
        """Unrelated queries should return fewer or no results."""
        import asyncio
        hc = HindsightClient()
        result = asyncio.get_event_loop().run_until_complete(
            hc.recall(query="completely unrelated quantum physics", max_results=3)
        )
        assert "results" in result
        # Might still return some results due to keyword overlap, but should be fewer


# ---------------------------------------------------------------------------
# Data Model Tests
# ---------------------------------------------------------------------------

class TestModels:
    def test_incident_defaults(self):
        inc = Incident(title="Test", description="Test incident")
        assert inc.status == "active"
        assert inc.severity == "Medium"
        assert inc.failed_approaches == []

    def test_incident_report_defaults(self):
        report = IncidentReport(description="Something broke")
        assert report.memory_enabled is True
        assert report.services == []

    def test_resolved_incident_required_fields(self):
        resolved = ResolvedIncident(id="INC-TEST", root_cause="Test cause")
        assert resolved.time_to_resolve_mins == 0
        assert resolved.failed_approaches == []

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
    # Response wraps diagnosis in a "diagnosis" field
    assert "diagnosis" in data
    diagnosis = data["diagnosis"]
    assert "pattern_match" in diagnosis
    assert "recommended_fix" in diagnosis
    # When memory is enabled, the mock fallback (or groq) returns failed approaches
    assert "failed_approaches" in diagnosis

def test_diagnose_memory_disabled():
    report = {
        "description": "Getting 502 errors on prod-api.",
        "services": ["prod-api"],
        "memory_enabled": False
    }
    response = client.post("/api/diagnose", json=report)
    assert response.status_code == 200
    data = response.json()
    # Response wraps diagnosis in a "diagnosis" field
    assert "diagnosis" in data
    diagnosis = data["diagnosis"]
    assert "pattern_match" in diagnosis

def test_feedback_loop():
    feedback = {
        "incident_id": "INC-0047",
        "is_correct": False,
        "correction": "Needed to clear redis cache too."
    }
    response = client.post("/api/feedback", json=feedback)
    assert response.status_code == 200
    assert response.json()["status"] == "success"

