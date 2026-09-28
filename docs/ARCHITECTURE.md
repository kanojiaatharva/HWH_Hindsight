# Architecture & Memory Model

## System Overview

Incident Déjà Vu is a memory-first incident response agent. The architecture separates **reasoning** (LLM) from **memory** (Hindsight) to create a system that structurally improves with every resolved incident.

```mermaid
graph TB
    subgraph Frontend ["Frontend (Next.js)"]
        UI["Incident Workspace UI"]
        Toggle["Memory ON/OFF Toggle"]
        FeedbackUI["Correction Input"]
    end

    subgraph Backend ["Backend (FastAPI)"]
        API["REST API Gateway"]
        Orchestrator["Agent Orchestrator"]
        Sanitizer["Data Sanitizer"]
    end

    subgraph Memory ["Memory Layer"]
        Hindsight["Hindsight Cloud API"]
        LocalFallback["Local In-Memory Fallback"]
    end

    subgraph Intelligence ["Intelligence Layer"]
        Groq["Groq LLM API"]
        Prompt["Structured Prompt Builder"]
    end

    UI -->|POST /api/diagnose| API
    Toggle -->|memory_enabled flag| API
    FeedbackUI -->|POST /api/feedback| API

    API --> Orchestrator
    Orchestrator -->|1. Recall| Hindsight
    Orchestrator -->|1. Recall fallback| LocalFallback
    Hindsight -->|Similar incidents| Orchestrator
    LocalFallback -->|Similar incidents| Orchestrator

    Orchestrator -->|2. Build context| Prompt
    Prompt -->|3. Diagnose| Groq
    Groq -->|Structured JSON| Orchestrator

    Orchestrator -->|4. Return diagnosis| API
    API -->|Response| UI

    FeedbackUI -->|Correction| API
    API -->|5. Retain| Sanitizer
    Sanitizer -->|Sanitized memory| Hindsight
    Sanitizer -->|Sanitized memory| LocalFallback
```

## Memory Lifecycle

The system implements a complete **Retain → Recall → Reason → Act → Learn** cycle:

```mermaid
sequenceDiagram
    participant Operator
    participant Frontend
    participant Backend
    participant Hindsight
    participant LLM as Groq LLM

    Note over Operator,LLM: Phase 1 — Incident Diagnosis
    Operator->>Frontend: Report symptoms
    Frontend->>Backend: POST /api/diagnose
    Backend->>Hindsight: recall(symptoms, top_k=5)
    Hindsight-->>Backend: Similar past incidents
    Backend->>LLM: Symptoms + recalled memories
    LLM-->>Backend: Structured diagnosis (JSON)
    Backend-->>Frontend: Diagnosis + failed approaches
    Frontend-->>Operator: Pattern match + warnings

    Note over Operator,LLM: Phase 2 — Feedback Loop
    Operator->>Frontend: Submit correction
    Frontend->>Backend: POST /api/feedback
    Backend->>Backend: Sanitize sensitive data
    Backend->>Hindsight: retain(correction, tags)
    Hindsight-->>Backend: Confirmation
    Backend-->>Frontend: Memory updated

    Note over Operator,LLM: Phase 3 — Future Recall
    Note right of Hindsight: Next time similar symptoms appear,<br/>the correction is recalled automatically
```

## Component Architecture

### 1. Frontend (Next.js + React)
- **Single-page application** with a split-panel Incident Workspace
- **Memory Toggle** — ON/OFF switch to demonstrate Hindsight's value
- **Chat-style interface** — Operator reports symptoms, agent responds with diagnosis
- **Feedback panel** — Corrections are submitted directly to the retain pipeline

### 2. API Gateway (FastAPI)
- **`POST /api/diagnose`** — Core diagnosis endpoint; orchestrates recall → reason → respond
- **`POST /api/feedback`** — Correction loop; retains new learnings in memory
- **`POST /api/incidents/{id}/resolve`** — Marks an incident as resolved and retains experience
- **`GET /api/incidents`** — Lists all incidents (seed data + runtime)
- **`GET /api/health`** — Health check with version info

### 3. Agent Orchestrator (`llm_agent.py`)
- Formats recalled memories into structured LLM context
- Uses **Groq** with `llama-3.3-70b-versatile` for fast inference
- Forces **JSON output** via `response_format={"type": "json_object"}`
- Enforces structured fields: `pattern_match`, `confidence_score`, `failed_approaches`, etc.

### 4. Hindsight Client (`hindsight_client.py`)
- **`retain(incident, tags)`** — Converts structured data to narrative format for better recall quality
- **`recall(query, max_results)`** — Semantic search against historical incidents
- **Data sanitization** — Strips API keys, tokens, IP addresses before retention
- **Graceful fallback** — If no API key, uses local in-memory keyword matching

## Data Flow

```mermaid
flowchart LR
    subgraph Input
        Symptoms["Incident Symptoms"]
    end

    subgraph Recall
        Query["Semantic Query"]
        Results["Top-K Similar Incidents"]
    end

    subgraph Reason
        Context["Symptoms + Memories"]
        LLM["LLM Diagnosis"]
    end

    subgraph Output
        RCA["Root Cause Analysis"]
        Fix["Recommended Fix"]
        Warn["Failed Approaches ⚠️"]
    end

    Symptoms --> Query
    Query --> Results
    Results --> Context
    Symptoms --> Context
    Context --> LLM
    LLM --> RCA
    LLM --> Fix
    LLM --> Warn
```

## Data Model (Pydantic v2)

| Model | Purpose | Key Fields |
|-------|---------|------------|
| `Incident` | Active/resolved incident record | `id`, `title`, `description`, `status`, `severity`, `root_cause`, `failed_approaches` |
| `IncidentReport` | Incoming diagnosis request | `description`, `services`, `memory_enabled` |
| `ResolvedIncident` | Data retained in memory | `root_cause`, `resolution_steps`, `failed_approaches`, `time_to_resolve_mins` |
| `IncidentFeedback` | User correction | `incident_id`, `is_correct`, `correction` |
| `DiagnosisResult` | Structured LLM output | `pattern_match`, `confidence_score`, `similar_incidents`, `recommended_fix`, `failed_approaches` |

## Fallback Mechanism

```mermaid
flowchart TD
    Start["API Call"] --> Check{"HINDSIGHT_API_KEY set?"}
    Check -->|Yes| Cloud["Hindsight Cloud API"]
    Check -->|No| Local["Local In-Memory Fallback"]
    Cloud -->|HTTP Error| Local
    Cloud -->|Timeout| Local
    Local --> Response["Return Results"]
    Cloud --> Response
```

If the `HINDSIGHT_API_KEY` is not present or the cloud API is unreachable, the `HindsightClient` gracefully falls back to an in-memory keyword-matching store. This ensures the demo **never crashes** due to environment configuration issues during a live presentation.

## Security Considerations

1. **Data Sanitization** — All incident data is sanitized before retention (API keys, tokens, IPs redacted)
2. **Environment Isolation** — Credentials stored in `.env`, excluded from version control
3. **HTTPS-only** — Hindsight API calls use TLS
4. **Graceful Degradation** — No data transmitted without valid credentials
5. **Input Validation** — Pydantic v2 enforces strict type validation on all API inputs

See [SECURITY.md](../SECURITY.md) for the full security policy.
