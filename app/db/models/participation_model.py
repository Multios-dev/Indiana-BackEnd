from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.orm import relationship

from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Participation(Base):
    __tablename__ = "participations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=False)
    role = Column(String, nullable=False)
    price = Column(Float, nullable=True)

    # Relationships
    user = relationship("User", back_populates="participations")
    event = relationship("Event", back_populates="participations")
