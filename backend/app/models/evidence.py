from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class EvidenceItem(Base):
    __tablename__ = "evidence_items"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id = Column(String(36), ForeignKey("test_executions.id", ondelete="CASCADE"), nullable=False)
    bug_id = Column(String(36), ForeignKey("bugs.id", ondelete="SET NULL"), nullable=True)
    evidence_type = Column(String(50), nullable=False) # SCREENSHOT, CONSOLE_LOG, NETWORK_FAILURE, DOM_SNAPSHOT
    file_path = Column(Text, nullable=False)
    metadata_json = Column(JSON, default=dict, nullable=False)
    captured_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    execution = relationship("TestExecution", back_populates="evidence_items")
    bug = relationship("Bug", back_populates="evidence_items")
