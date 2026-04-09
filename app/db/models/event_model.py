from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class Event(Base):
    __tablename__ = "events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    event_type = Column(String, nullable=False)

    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    # Geographic coordinates
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Reference to the parent event
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("events.id"),
        nullable=True
    )
    # Reference to the address
    address_id = Column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id"),
        nullable=True
    )

    # -------------------------
    # RELATIONSHIPS
    # -------------------------
    # Parent organization
    parent = relationship(
        "Event",
        remote_side=lambda: [Event.id],
        back_populates="children"
    )
    # Sub-organizations
    children = relationship(
        "Event",
        back_populates="parent",
        cascade="all, delete",
        passive_deletes=True
    )
    # N-N relationshop with Audience
    audiences = relationship(
        "Audience",
        secondary="event_audience",
        back_populates="events"
    )
    address = relationship(
        "Address",
        foreign_keys=[address_id],
        back_populates="events",
        uselist=False
    )

class Audience(Base):
    __tablename__ = "audiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    label = Column(String, nullable=False, unique=True)

    # Inverse relationship
    events = relationship(
        "Event",
        secondary="event_audience",
        back_populates="audiences"
    )

# Association table
event_audience = Table(
    "event_audience",
    Base.metadata,
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("audience_id", ForeignKey("audiences.id", ondelete="CASCADE"), primary_key=True),
)