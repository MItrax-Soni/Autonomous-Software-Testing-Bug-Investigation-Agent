from sqlalchemy import Column, String, Text, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.database import Base

class DiscoveredElement(Base):
    __tablename__ = "discovered_elements"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    page_id = Column(String(36), ForeignKey("discovered_pages.id", ondelete="CASCADE"), nullable=False)
    tag_name = Column(String(50), nullable=False)
    element_type = Column(String(50), nullable=True) # button, input, select, link, checkbox, modal
    selector = Column(Text, nullable=False)
    semantic_label = Column(String(255), nullable=True)
    attributes_json = Column(JSON, default=dict, nullable=False)
    is_interactive = Column(Boolean, default=True, nullable=False)
    parent_form_id = Column(String(36), nullable=True)

    # Relationships
    page = relationship("DiscoveredPage", back_populates="elements")
