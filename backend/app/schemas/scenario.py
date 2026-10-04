from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Literal

ActionType = Literal[
    "navigate",
    "click",
    "fill",
    "select",
    "check",
    "press",
    "assert_visible",
    "assert_hidden",
    "assert_text",
    "assert_url"
]

class TestStepDSL(BaseModel):
    step_index: int
    action: ActionType
    selector: Optional[str] = None
    value: Optional[str] = None
    expected: Optional[str] = None
    timeout_ms: Optional[int] = 5000

class ScenarioCreate(BaseModel):
    title: str = Field(..., max_length=255)
    description: str
    category: Literal["POSITIVE", "NEGATIVE", "BOUNDARY", "RESPONSIVENESS"]
    target_page_url: str
    steps_json: List[TestStepDSL]
    expected_result: str
    is_approved: bool = True
    order_index: int = 0

class ScenarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    title: str
    description: str
    category: str
    target_page_url: str
    steps_json: List[TestStepDSL]
    expected_result: str
    is_approved: bool
    order_index: int

class ScenarioUpdate(BaseModel):
    is_approved: Optional[bool] = None
    order_index: Optional[int] = None
    title: Optional[str] = None
    steps_json: Optional[List[TestStepDSL]] = None
