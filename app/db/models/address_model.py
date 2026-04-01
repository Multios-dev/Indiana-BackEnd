import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String
from app.db.base import Base

class Address(Base):
    __tablename__ = "addresses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    box_number = Column(String, nullable=False)
    street = Column(String, nullable=False)
    post_name = Column(String, nullable=False)
    post_code = Column(String, nullable=False)
    country = Column(String, nullable=False)