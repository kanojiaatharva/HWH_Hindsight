from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

class Incident(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    description: str
    status: str = "active" # active, resolved
    created_at: datetime = datetime.now()
    severity: str = "High"
    affected_services: List[str] = []
    
    # Optional fields filled when resolved
    root_cause: Optional[str] = None
    resolution_steps: Optional[List[str]] = None
    failed_approaches: Optional[List[str]] = None

class IncidentReport(BaseModel):
    description: str
    services: List[str] = []
    memory_enabled: bool = True

class IncidentFeedback(BaseModel):
    incident_id: str
    is_correct: bool
    correction: Optional[str] = None

class ResolvedIncident(BaseModel):
    id: str
    root_cause: str
    resolution_steps: List[str]
    failed_approaches: List[str]
    time_to_resolve_mins: int

class DiagnosisResult(BaseModel):
    pattern_match: bool
    confidence_score: float
    similar_incidents: List[dict]
    recommended_fix: str
    failed_approaches: List[str]
    root_cause_analysis: str
