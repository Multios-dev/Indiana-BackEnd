from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

# Représente une organisation (unité, groupe, etc.)
class Organization(Base):
    __tablename__ = "organizations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    acronym = Column(String, nullable=True)
    logo = Column(String, nullable=True)
    purpose = Column(String, nullable=False)
    org_type = Column(String, nullable=False)
    sgp_type = Column(String, nullable=True)
    billable = Column(Boolean, nullable=False, default=False)
    is_legal_entity = Column(Boolean, nullable=False, default=False)

    # Référence vers l'organisation parent
    parent_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True
    )

    # -------------------------
    # RELATIONS HIERARCHIQUES
    # -------------------------
    # Organisation parent
    parent = relationship(
        "Organization",
        remote_side=lambda: [Organization.id],
        back_populates="children"
    )

    # Sous-organisations
    children = relationship(
        "Organization",
        back_populates="parent",
        cascade="all, delete",
        passive_deletes=True
    )

    # -------------------------
    # AUTRES RELATIONS
    # -------------------------
    # Contact de l'organisation
    contact = relationship(
        "Contact",
        back_populates="organization",
        uselist=False,
        passive_deletes=True
    )

    # Membres de l'organisation
    memberships = relationship(
        "Membership",
        back_populates="organization",
        cascade="all, delete-orphan",
        passive_deletes=True
    )