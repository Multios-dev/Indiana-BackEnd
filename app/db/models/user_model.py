from sqlalchemy import Column, String, Date, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

# Represents a person in the system
class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_names = Column(JSON, nullable=False)                          #List of first names stored as JSON since some users have multiple first names
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    nationality = Column(JSON, nullable=False)
    totem = Column(String, nullable=True)                               # Scout totem
    quali = Column(String, nullable=True)                               # Qualification (internal role/status)
    is_legal_guardian = Column(Boolean, default=False, nullable=False)  # Indicates whether the user is a parent/legal guardian
    password = Column(String, nullable=True)
    # Reference to home address (required)
    home_address_id = Column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id"),
        nullable=False
    )

    # Reference to residential address (optional)
    residential_address_id = Column(
        UUID(as_uuid=True),
        ForeignKey("addresses.id"),
        nullable=True
    )

    # -------------------------
    # RELATIONSHIPS
    # -------------------------
    # 1-to-1 relationship with Contact
    # Each user/org can have only one contact
    contact = relationship(
        "Contact", back_populates="user",
        uselist=False,                              # means "single contact"
        passive_deletes=True                        # the db handles deletion if needed
    )

    # 1-to-N relationship with Membership
    # A user can belong to multiple organizations
    memberships = relationship(
        "Membership",
        back_populates="user",
        cascade="all, delete",  # if the user is deleted, their memberships are too
        passive_deletes=True
    )

    # Relationship to home address (required)
    # foreign_keys is required here beceause we have 2 FKs pointing to the same "addresses" table
    # Without it, SQLAlchemy cannot determine which FK to use for which relationship
    # uselist=False means "a single Address object" instead of a list
    home_address = relationship(
        "Address",
        foreign_keys=[home_address_id],
        uselist=False
    )

    # Relationship to residential address (optional)
    # Same logic as home_address
    residential_address = relationship(
        "Address",
        foreign_keys=[residential_address_id],
        uselist=False
    )

    children = relationship(
        "GuardianRelationship",
        foreign_keys="GuardianRelationship.guardian_id",
        back_populates="guardian",
        cascade="all, delete-orphan"
    )

    guardians = relationship(
        "GuardianRelationship",
        foreign_keys="GuardianRelationship.minor_id",
        back_populates="minor",
        cascade="all, delete-orphan"
    )

    participations = relationship("Participation", back_populates="user")


# Mapping table
class GuardianRelationship(Base):
    __tablename__ = "guardian_relationships"
    guardian_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    minor_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    # Relationships
    guardian = relationship(
        "User",
        foreign_keys=[guardian_id],
        back_populates="children"
    )
    minor = relationship(
        "User",
        foreign_keys=[minor_id],
        back_populates="guardians"
    )