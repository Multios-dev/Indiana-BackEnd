from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base import Base

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    event_type = Column(String, nullable=False)

    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Référence vers l'événement parent
    parent_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=True
    )

    # -------------------------
    # RELATIONS HIERARCHIQUES
    # -------------------------
    # Organisation parent
    parent = relationship(
        "Event",
        remote_side=[id],
        back_populates="children"
    )

    # Sous-organisations
    children = relationship(
        "Event",
        back_populates="parent",
        cascade="all, delete",
        passive_deletes=True
    )

    # Relation N-N avec Audience
    audiences = relationship(
        "Audience",
        secondary="event_audience",
        back_populates="events"
    )

class Audience(Base):
    __tablename__ = "audiences"

    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String, nullable=False, unique=True)

    # relation inverse
    events = relationship(
        "Event",
        secondary="event_audience",
        back_populates="audiences"
    )

# Table d'association
event_audience = Table(
    "event_audience",
    Base.metadata,
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
    Column("audience_id", ForeignKey("audiences.id", ondelete="CASCADE"), primary_key=True),
)