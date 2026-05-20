import uuid

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

# Represents contact information
# A contact can be associated with a user or an organization
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)

    # -------------------------
    # FOREIGN KEYS
    # -------------------------
    # Reference to a user (optional)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True
    )
    # Reference to an organization (optional)
    org_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True
    )

    # -------------------------
    # RELATIONSHIPS
    # -------------------------
    # Relationship to User
    # back_populates="contact" matches User.contact
    user = relationship(
        "User",
        back_populates="contact"
    )
    # Relationship to Organization
    # back_populates="contact" matches Organization.contact
    organization = relationship(
        "Organization",
        back_populates="contact"
    )