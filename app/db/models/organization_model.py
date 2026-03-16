from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    acronym = Column(String, nullable=True)
    logo = Column(String, nullable=True)
    purpose = Column(String, nullable=False)
    org_type = Column(String, nullable=False)
    sgp_type = Column(String, nullable=True)
    billable = Column(Boolean, nullable=False, default=False)
    is_legal_entity = Column(Boolean, nullable=False, default=False)

    parent_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)

    parent = relationship("Organization", remote_side=[id])
    contact = relationship("Contact")