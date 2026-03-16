from sqlalchemy import Column, Integer, String, Date, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.contact_model import Contact

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_names = Column(JSON, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    totem = Column(String, nullable = True)
    quali = Column(String, nullable = True)
    is_legal_guardian = Column(Boolean, default=False, nullable=False)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=True)

    contact = relationship("Contact", cascade="all, delete")