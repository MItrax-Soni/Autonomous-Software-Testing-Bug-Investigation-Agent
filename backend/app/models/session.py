from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class TestSession(Base):
    __test__ = False
    __tablename__ = "test_sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = Column(String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)
    target_url = Column(Text, nullable=False)
    status = Column(String(50), default="DRAFT", nullable=False) # DRAFT, SCANNING, SCANNED, PLANNING, PLANNED, EXECUTING, INVESTIGATING, COMPLETED, FAILED
    max_depth = Column(Integer, default=2, nullable=False)
    max_pages = Column(Integer, default=15, nullable=False)
    total_tests = Column(Integer, default=0, nullable=False)
    passed_tests = Column(Integer, default=0, nullable=False)
    failed_tests = Column(Integer, default=0, nullable=False)
    error_summary = Column(Text, nullable=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="sessions")
    pages = relationship("DiscoveredPage", back_populates="session", cascade="all, delete-orphan")
    scenarios = relationship("TestScenario", back_populates="session", cascade="all, delete-orphan")
    executions = relationship("TestExecution", back_populates="session", cascade="all, delete-orphan")
    bugs = relationship("Bug", back_populates="session", cascade="all, delete-orphan")
    report = relationship("Report", back_populates="session", uselist=False, cascade="all, delete-orphan")
