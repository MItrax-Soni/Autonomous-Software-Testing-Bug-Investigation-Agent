from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class DiscoveredPageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    url: str
    title: Optional[str] = None
    http_status: Optional[int] = None
    depth: int
    screenshot_path: Optional[str] = None
    discovered_at: datetime

class DiscoveredElementResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    page_id: str
    tag_name: str
    element_type: Optional[str] = None
    selector: str
    semantic_label: Optional[str] = None
    attributes_json: Dict[str, Any] = Field(default_factory=dict)
    is_interactive: bool
    parent_form_id: Optional[str] = None
