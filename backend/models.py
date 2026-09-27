from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Incident(BaseModel):
    id: str = str(uuid.uuid4())
    title: str
    description: str
    status: str = "active"  # active, resolved, mitigating
    created_at: datetime = Field(default_factory=datetime.now)
    severity: str = "Medium"  # Low, Medium, High, Critical
    affected_services: List[str] = Field(default_factory=list)
    symptoms: Optional[str] = None

    # Optional fields filled when resolved
    root_cause: Optional[str] = None
    resolution_steps: Optional[List[str]] = Field(default_factory=list)
    failed_approaches: Optional[List[str]] = Field(default_factory=list)
    time_to_resolve_mins: Optional[int] = None
    environment: Optional[str] = None

class IncidentReport(BaseModel):
    description: str
    services: List[str] = Field(default_factory=list)
    memory_enabled: bool = True
    environment: Optional[str] = None

class IncidentFeedback(BaseModel):
    incident_id: str
    is_correct: bool
    correction: Optional[str] = None
    feedback_notes: Optional[str] = None

class ResolvedIncident(BaseModel):
    id: str
    root_cause: str
    resolution_steps: List[str] = Field(default_factory=list)
    failed_approaches: List[str] = Field(default_factory=list)
    time_to_resolve_mins: int = 0
    environment: Optional[str] = None
    lessons_learned: Optional[str] = None

class DiagnosisResult(BaseModel):
    pattern_match: bool = False
    confidence_score: float = 0.0
    similar_incidents: List[dict] = Field(default_factory=list)
    recommended_fix: str = ""
    failed_approaches: List[str] = Field(default_factory=list)
    root_cause_analysis: str = ""
    historical_context_used: bool = False
