# API Reference — Incident Déjà Vu

> Base URL: `http://localhost:8000`
>
> Interactive docs available at `http://localhost:8000/docs` (Swagger UI) and `http://localhost:8000/redoc` (ReDoc)

---

## Health Check

### `GET /api/health`

Returns the service health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-09-28T15:30:00.000000",
  "version": "1.0.0"
}
```

---

## Incidents

### `GET /api/incidents`

Returns all incidents (seed data + runtime).

**Response:** `200 OK`
```json
[
  {
    "id": "INC-0047",
    "title": "prod-api-3 connection timeout",
    "description": "prod-api-3 is returning 502 errors. CPU is at 95%.",
    "status": "resolved",
    "severity": "High",
    "affected_services": ["prod-api", "auth-service"],
    "root_cause": "Connection pool exhaustion in auth-service v2.3.1",
    "resolution_steps": ["kubectl rollout restart deploy/sidecar-proxy -n prod"],
    "failed_approaches": ["Restarting nginx (symptoms returned in 10 mins)"],
    "time_to_resolve_mins": 4
  }
]
```

### `GET /api/incidents/{incident_id}`

Returns a specific incident by ID.

**Response:** `200 OK` — Incident object | `404 Not Found`

---

## Diagnosis (Core Feature)

### `POST /api/diagnose`

Diagnose an incident with or without Hindsight memory context.

**Request Body:**
```json
{
  "description": "prod-api-3 is returning 502 errors. CPU is at 95%.",
  "services": ["prod-api"],
  "memory_enabled": true
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `description` | string | ✅ | Free-text incident symptoms |
| `services` | string[] | ❌ | Affected service names |
| `memory_enabled` | boolean | ❌ | Enable Hindsight recall (default: `true`) |

**Response (Memory ON):** `200 OK`
```json
{
  "diagnosis": {
    "pattern_match": true,
    "confidence_score": 0.87,
    "similar_incidents": [
      {
        "id": "INC-0047",
        "symptoms": "502 errors on prod-api with CPU spike",
        "root_cause": "Connection pool exhaustion in auth-service"
      }
    ],
    "recommended_fix": "kubectl rollout restart deploy/sidecar-proxy -n prod\nkubectl scale deploy/auth-service --replicas=3 -n prod",
    "failed_approaches": [
      "Restarting nginx — symptoms return in 10 mins",
      "Scaling prod-api pods — bottleneck was upstream"
    ],
    "root_cause_analysis": "Connection pool exhaustion in auth-service. Historical pattern indicates upstream bottleneck."
  },
  "memory_used": true,
  "results_count": 1,
  "is_mock": false
}
```

**Response (Memory OFF):** `200 OK`
```json
{
  "diagnosis": {
    "pattern_match": false,
    "confidence_score": 0.0,
    "similar_incidents": [],
    "recommended_fix": "Check application logs and metrics.\nInspect recent deployments.",
    "failed_approaches": [],
    "root_cause_analysis": "Generic troubleshooting required. No historical context available."
  },
  "memory_used": false,
  "results_count": 0,
  "is_mock": true
}
```

> **Key Differentiator:** Compare the two responses above. With memory ON, the agent provides specific root cause, targeted fix commands, and explicitly warns against failed approaches from past incidents.

---

## Feedback / Correction Loop

### `POST /api/feedback`

Submit feedback on a diagnosis. Corrections are retained in Hindsight memory for future recall.

**Request Body:**
```json
{
  "incident_id": "INC-0047",
  "is_correct": false,
  "correction": "Actually, this time it was an expired SSL certificate on the internal load balancer."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `incident_id` | string | ✅ | The incident being corrected |
| `is_correct` | boolean | ✅ | Whether the diagnosis was correct |
| `correction` | string | ❌ | The correct diagnosis (triggers `retain`) |

**Response:** `200 OK`
```json
{
  "status": "success",
  "retained": true,
  "result": { "success": true, "mock": true, "bank_id": "mock", "items_count": 1 }
}
```

> **Memory Learning Loop:** When `is_correct=false` and a `correction` is provided, the correction is sanitized and retained in Hindsight. Future incidents with similar symptoms will recall this correction alongside the original resolution.

---

## Incident Resolution

### `POST /api/incidents/{incident_id}/resolve`

Resolve an incident and retain the full experience in Hindsight memory.

**Request Body:**
```json
{
  "id": "INC-0062",
  "root_cause": "Connection pool exhaustion (recurring)",
  "resolution_steps": ["Restart sidecar proxy", "Scale auth-service to 3 replicas"],
  "failed_approaches": ["Restarting nginx"],
  "time_to_resolve_mins": 6
}
```

**Response:** `200 OK`
```json
{
  "status": "success",
  "message": "Incident resolved and retained in memory.",
  "retention_result": { "success": true, "mock": true }
}
```

---

## Demo Endpoints

### `POST /api/demo/reset`

Reset the demo to initial state (reload seed data, clear runtime memories).

**Response:** `200 OK`
```json
{ "status": "success", "message": "Demo reset complete" }
```

### `POST /api/demo/seed`

Confirm that demo memories are seeded in the Hindsight client.

**Response:** `200 OK`
```json
{ "status": "success", "message": "Demo memories already seeded", "memory_count": 3 }
```
