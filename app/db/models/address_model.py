import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class Address(Base):
    __tablename__ = "addresses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thoroughfare = Column(String, nullable=False)  # rue + numéro
    box_number = Column(String, nullable=True)
    post_name = Column(String, nullable=False)
    post_code = Column(String, nullable=False)
    country = Column(String, nullable=False)
    # add the BeSt id later

    organization = relationship(
        "Organization",
        back_populates="address",
        uselist=False
    )
    home_users = relationship(
        "User",
        foreign_keys="User.home_address_id",
        back_populates="home_address"
    )
    residential_users = relationship(
        "User",
        foreign_keys="User.residential_address_id",
        back_populates="residential_address"
    )
    events = relationship(
        "Event",
        back_populates="address"
    )