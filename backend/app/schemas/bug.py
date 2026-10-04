from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class VerifiedEvidence(BaseModel):
    http_errors: List[Dict[str, Any]] = Field(default_factory=list)
    console_errors: List[Dict[str, Any]] = Field(default_factory=list)
    failing_selector: Optional[str] = None
    exception_trace: Optional[str] = None
    dom_snippet: Optional[str] = None

class AIHypothesis(BaseModel):
    summary: str
    probable_root_cause: str
    impact_analysis: str
    confidence_score: float = 0.9

class BugResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    execution_id: str
    session_id: str
    title: str
    category: str
    severity: str
    verified_evidence_json: Dict[str, Any]
    ai_hypothesis_json: Dict[str, Any]
    remediation_advice: Optional[str] = None
    screenshot_url: Optional[str] = None
    created_at: datetime
