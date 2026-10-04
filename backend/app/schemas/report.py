from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime

class ReportMetrics(BaseModel):
    total_tests: int
    passed_tests: int
    failed_tests: int
    pass_rate_percentage: int
    total_duration_ms: int
    critical_bugs: int
    high_bugs: int
    medium_bugs: int
    low_bugs: int

class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    session_id: str
    summary_markdown: str
    metrics_json: Dict[str, Any]
    file_path_html: Optional[str] = None
    file_path_json: Optional[str] = None
    generated_at: datetime
