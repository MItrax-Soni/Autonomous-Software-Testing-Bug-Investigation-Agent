from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ExecutionStepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    step_index: int
    action: str
    selector: Optional[str] = None
    value: Optional[str] = None
    status: str
    duration_ms: int
    error_log: Optional[str] = None
    screenshot_path: Optional[str] = None

class TestExecutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    scenario_id: str
    session_id: str
    scenario_title: Optional[str] = None
    status: str
    duration_ms: int
    error_message: Optional[str] = None
    error_step_index: Optional[int] = None
    executed_at: datetime
    steps: List[ExecutionStepResponse] = []
