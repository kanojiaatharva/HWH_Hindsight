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

@app.get("/api/incidents", response_model=List[Incident])
async def get_incidents():
    return incidents_db

@app.post("/api/diagnose")
async def diagnose(report: IncidentReport):
    recalled_memories = {"memories": []}
    
    # 1. Use Hindsight to recall similar incidents if memory is enabled
    if report.memory_enabled:
        recalled_memories = await hindsight.recall(query=report.description)
    
    # 2. Use LLM to diagnose based on recalled memories
    diagnosis = await diagnose_incident(report.description, recalled_memories)
    
    return diagnosis

@app.post("/api/feedback")
async def submit_feedback(feedback: IncidentFeedback):
    # If the user corrects the agent, retain this correction as a new memory
    if not feedback.is_correct and feedback.correction:
        mock_resolved = ResolvedIncident(
            id=feedback.incident_id,
            root_cause="User Correction",
            resolution_steps=[feedback.correction],
            failed_approaches=["Previous LLM suggestion"],
            time_to_resolve_mins=0
        )
        await hindsight.retain(incident=mock_resolved)
    return {"status": "success"}

@app.post("/api/incidents/{incident_id}/resolve")
async def resolve_incident(incident_id: str, resolved_data: ResolvedIncident):
    # 1. Update the incident in the database
    for inc in incidents_db:
        if inc.id == incident_id:
            inc.status = "resolved"
            inc.resolution_steps = resolved_data.resolution_steps
            inc.failed_approaches = resolved_data.failed_approaches
            inc.root_cause = resolved_data.root_cause
            break
            
    # 2. Retain the experience in Hindsight
    await hindsight.retain(incident=resolved_data)
    
    return {"status": "success", "message": "Incident resolved and retained in memory."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
