from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    org_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=True)

    user = relationship("User", back_populates="contact")
    organization = relationship("Organization", back_populates="contact")