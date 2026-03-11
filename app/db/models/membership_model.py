from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String
from sqlalchemy.orm import relationship

from app.db.base import Base

class Membership(Base):
    __tablename__ = "memberships"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Clés étrangères
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    role = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    price = Column(Numeric(10,2), nullable=False)

    user = relationship("User")
    organization = relationship("Organization")