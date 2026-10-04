from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), unique=True, nullable=False)
    summary_markdown = Column(Text, nullable=False)
    metrics_json = Column(JSON, default=dict, nullable=False)
    file_path_html = Column(Text, nullable=True)
    file_path_json = Column(Text, nullable=True)
    generated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    session = relationship("TestSession", back_populates="report")
