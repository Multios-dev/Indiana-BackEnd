from sqlalchemy import Column, Integer, String, Date, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

# Représente une personne dans le système
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_names = Column(JSON, nullable=False)                          #Liste des prénoms stockée en JSON car certains utilisateurs ont plusieurs prénoms
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    totem = Column(String, nullable=True)                               # Totem scout
    quali = Column(String, nullable=True)                               # Qualification (fonction/statut interne)
    is_legal_guardian = Column(Boolean, default=False, nullable=False)  # Indique si l'utilisateur est un parent/responsable légal


    # -------------------------
    # RELATIONS
    # -------------------------

    # Relation 1-à-1 avec Contact
    # Chaque utilisateur/orga peut avoir qu'un seul contact
    contact = relationship(
        "Contact", back_populates="user",
        uselist=False,          # signifie "un seul contact"
        passive_deletes=True    # la db gère la suppression si nécessaire
    )

    # Relation 1-à-N avec Membership (Mandat)
    # Un utilisateur peut appartenir à plusieurs organisations
    memberships = relationship(
        "Membership",
        back_populates="user",
        cascade="all, delete",  # si on supprime l'utilisateur, ses memberships aussi
        passive_deletes=True
    )