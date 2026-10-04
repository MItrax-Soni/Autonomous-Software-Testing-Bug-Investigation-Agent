from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
from app.database import Base

class DiscoveredPage(Base):
    __tablename__ = "discovered_pages"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), ForeignKey("test_sessions.id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=False)
    title = Column(String(500), nullable=True)
    http_status = Column(Integer, nullable=True)
    depth = Column(Integer, default=0, nullable=False)
    screenshot_path = Column(Text, nullable=True)
    discovered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    session = relationship("TestSession", back_populates="pages")
    elements = relationship("DiscoveredElement", back_populates="page", cascade="all, delete-orphan")
