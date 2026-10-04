from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class TestExecution(Base):
    __test__ = False
    __tablename__ = "test_executions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    scenario_id = Column(String(36), ForeignKey("test_scenarios.id", ondelete="CASCADE"), nullable=False)
    session_id = Column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), nullable=False) # PASSED, FAILED, TIMED_OUT, SKIPPED
    duration_ms = Column(Integer, default=0, nullable=False)
    error_message = Column(Text, nullable=True)
    error_step_index = Column(Integer, nullable=True)
    executed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    scenario = relationship("TestScenario", back_populates="executions")
    session = relationship("TestSession", back_populates="executions")
    steps = relationship("ExecutionStep", back_populates="execution", cascade="all, delete-orphan")
    bug = relationship("Bug", back_populates="execution", uselist=False, cascade="all, delete-orphan")
    evidence_items = relationship("EvidenceItem", back_populates="execution", cascade="all, delete-orphan")

class ExecutionStep(Base):
    __tablename__ = "execution_steps"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    execution_id = Column(String(36), ForeignKey("test_executions.id", ondelete="CASCADE"), nullable=False)
    step_index = Column(Integer, nullable=False)
    action = Column(String(50), nullable=False)
    selector = Column(Text, nullable=True)
    value = Column(Text, nullable=True)
    status = Column(String(50), nullable=False) # PASSED, FAILED
    duration_ms = Column(Integer, default=0, nullable=False)
    error_log = Column(Text, nullable=True)
    screenshot_path = Column(Text, nullable=True)

    # Relationships
    execution = relationship("TestExecution", back_populates="steps")
