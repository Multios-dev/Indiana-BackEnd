from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, Date
from sqlalchemy.orm import relationship

from app.db.base import Base

# Représente l'appartenance d'un utilisateur à une organisation
class Membership(Base):
    __tablename__ = "memberships"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Clés étrangères
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)

    role = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    price = Column(Numeric(10,2), nullable=True)

    # -------------------------
    # RELATIONS
    # -------------------------
    # Relation vers l'utilisateur
    user = relationship(
        "User",
        back_populates="memberships"
    )

    # Relation vers l'organisation
    organization = relationship(
        "Organization",
        back_populates="memberships"
    )