from sqlalchemy import Column, String, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid


class Identifier(Base):
    __tablename__ = "identifiers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    entity_type = Column(String, nullable=False)   # "user", "organization", "event", "membership", "participation"
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    creator = Column(String, nullable=False)
    notation = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("entity_type", "entity_id", "creator"),
        Index("ix_identifiers_entity", "entity_type", "entity_id"),
    )
