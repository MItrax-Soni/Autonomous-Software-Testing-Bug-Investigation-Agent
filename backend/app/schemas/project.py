from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    target_url: str = Field(..., description="Target web application base URL")
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    target_url: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
