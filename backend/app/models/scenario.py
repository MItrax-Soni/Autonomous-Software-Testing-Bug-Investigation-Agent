from sqlalchemy import Column, String, Text, Boolean, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class TestScenario(Base):
    __test__ = False
    __tablename__ = "test_scenarios"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False) # POSITIVE, NEGATIVE, BOUNDARY, RESPONSIVENESS
    target_page_url = Column(Text, nullable=False)
    steps_json = Column(JSON, default=list, nullable=False)
    expected_result = Column(Text, nullable=False)
    is_approved = Column(Boolean, default=True, nullable=False)
    order_index = Column(Integer, default=0, nullable=False)

    # Relationships
    session = relationship("TestSession", back_populates="scenarios")
    executions = relationship("TestExecution", back_populates="scenario", cascade="all, delete-orphan")
