from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

# We will implement these shortly
from models import Incident, ResolvedIncident, IncidentReport, IncidentFeedback
from hindsight_client import HindsightClient
from llm_agent import diagnose_incident

app = FastAPI(title="Incident Déjà Vu API")

# Add CORS middleware to allow the Next.js frontend to talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

hindsight = HindsightClient()

# In-memory storage for MVP
incidents_db: List[Incident] = []

@app.on_event("startup")
async def startup_event():
    # Load seed data
    from seed_data import load_seed_data
    global incidents_db
    incidents_db = load_seed_data()
    print(f"Loaded {len(incidents_db)} incidents from seed data.")

@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/incidents", response_model=List[Incident])
async def get_incidents():
    return incidents_db

@app.get("/api/incidents/{incident_id}")
async def get_incident(incident_id: str):
    """Get a specific incident by ID."""
    for inc in incidents_db:
        if inc.id == incident_id:
            return inc
    raise HTTPException(status_code=404, detail="Incident not found")

@app.post("/api/diagnose")
async def diagnose(report: IncidentReport):
    """Diagnose an incident with or without memory."""
    recalled_context = {"results": [], "mock": True}

    # 1. Use Hindsight to recall similar incidents if memory is enabled
    if report.memory_enabled:
        recalled_context = await hindsight.recall(query=report.description, max_results=5)

    # 2. Use LLM to diagnose based on recalled memories
    diagnosis = await diagnose_incident(report.description, recalled_context, report.memory_enabled)

    return {
        "diagnosis": diagnosis,
        "memory_used": report.memory_enabled,
        "results_count": len(recalled_context.get("results", [])),
        "is_mock": recalled_context.get("mock", False)
    }

@app.post("/api/feedback")
async def submit_feedback(feedback: IncidentFeedback):
    """Submit feedback/correction for a diagnosis."""
    if not feedback.is_correct and feedback.correction:
        mock_resolved = ResolvedIncident(
            id=feedback.incident_id,
            root_cause="User Correction",
            resolution_steps=[feedback.correction],
            failed_approaches=["Previous LLM suggestion"],
            time_to_resolve_mins=0
        )
        result = await hindsight.retain(incident=mock_resolved, tags=["correction", "feedback"])
        return {"status": "success", "retained": True, "result": result}
    return {"status": "success", "retained": False}

@app.post("/api/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: str, resolved_data: ResolvedIncident):
    """Resolve an incident and retain the experience in memory."""
    # 1. Update the incident in the database
    for inc in incidents_db:
        if inc.id == incident_id:
            inc.status = "resolved"
            inc.resolution_steps = resolved_data.resolution_steps
            inc.failed_approaches = resolved_data.failed_approaches
            inc.root_cause = resolved_data.root_cause
            break
    else:
        raise HTTPException(status_code=404, detail="Incident not found")

    # 2. Retain the experience in Hindsight
    result = await hindsight.retain(incident=resolved_data, tags=["resolved", "production"])

    return {
        "status": "success",
        "message": "Incident resolved and retained in memory.",
        "retention_result": result
    }

@app.post("/api/demo/reset")
async def reset_demo():
    """Reset the demo to initial state."""
    from seed_data import load_seed_data
    global incidents_db
    incidents_db = load_seed_data()
    # Reset local Hindsight memories
    hindsight.local_memories = []
    hindsight._seed_demo_memories()
    return {"status": "success", "message": "Demo reset complete"}

@app.post("/api/demo/seed")
async def seed_demo_memory():
    """Explicitly seed demo memories into Hindsight."""
    # The demo memories are already seeded in HindsightClient.__init__
    return {
        "status": "success",
        "message": "Demo memories already seeded",
        "memory_count": len(hindsight.local_memories)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
