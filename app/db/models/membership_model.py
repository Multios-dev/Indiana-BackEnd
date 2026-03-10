from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship

from app.db.base import Base

class Membership(Base):
    __tablename__ = "memberships"
    id = Column(Integer, primary_key=True)

    # Clés étrangères
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)

    start_date = Column(DateTime)
    end_date = Column(DateTime)

    price = Column(Numeric(10,2))

    user = relationship("User")
    organization = relationship("Organization")