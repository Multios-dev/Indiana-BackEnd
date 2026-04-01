import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

# Représente les informations de contact
# Un contact peut être associé à un utilisateur ou une organisation
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)

    # -------------------------
    # CLÉS ÉTRANGÈRES
    # -------------------------
    # Référence vers un utilisateur (optionnel)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    # Référence vers une organisation (optionnel)
    org_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True
    )

    # -------------------------
    # RELATIONS
    # -------------------------
    # Relation vers User
    # back_populates="contact" correspond à User.contact
    user = relationship(
        "User",
        back_populates="contact"
    )
    # Relation vers Organization
    # back_populates="contact" correspond à Organization.contact
    organization = relationship(
        "Organization",
        back_populates="contact"
    )