from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, Date, UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
import uuid

# Represents a user's membership in an organization
class Membership(Base):
    __tablename__ = "memberships"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Foreign keys
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    organization_id = Column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False
    )

    role = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    price = Column(Numeric(10,2), nullable=True)

    # -------------------------
    # RELATIONSHIPS
    # -------------------------
    # Relation to the user
    user = relationship(
        "User",
        back_populates="memberships"
    )
    # Relationship to the organization
    organization = relationship(
        "Organization",
        back_populates="memberships"
    )