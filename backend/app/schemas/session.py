from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class SessionCreate(BaseModel):
    project_id: Optional[str] = None
    target_url: str = Field(..., description="Target web application URL")
    max_depth: int = Field(default=2, ge=1, le=5)
    max_pages: int = Field(default=15, ge=1, le=50)

class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    project_id: Optional[str] = None
    target_url: str
    status: str
    max_depth: int
    max_pages: int
    total_tests: int
    passed_tests: int
    failed_tests: int
    error_summary: Optional[str] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
