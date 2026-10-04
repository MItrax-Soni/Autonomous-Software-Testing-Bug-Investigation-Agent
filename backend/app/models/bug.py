from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class Bug(Base):
    __tablename__ = "bugs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id = Column(String(36), ForeignKey("test_executions.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    severity = Column(String(50), nullable=False) # CRITICAL, HIGH, MEDIUM, LOW
    verified_evidence_json = Column(JSON, default=dict, nullable=False) # Grounded facts
    ai_hypothesis_json = Column(JSON, default=dict, nullable=False)     # Gemini deductive reasoning
    remediation_advice = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    execution = relationship("TestExecution", back_populates="bug")
    session = relationship("TestSession", back_populates="bugs")
    evidence_items = relationship("EvidenceItem", back_populates="bug")
