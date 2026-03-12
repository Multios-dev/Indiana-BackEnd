from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.models.enums.organization_type import OrganizationType

class Organization(Base):
    __tablename__ = "organizations"

    # Identification
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    acronym = Column(String, nullable=True)
    logo = Column(String, nullable=True)

    # Hiérarchie
    parent_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)

    # Contact
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)

    # Adresse
    street = Column(String, nullable=True)
    city = Column(String, nullable=True)
    zip = Column(String, nullable=True)
    country = Column(String, nullable=True)

    # Forme légale de l'organisation
    legal_form = Column(String, nullable=False)

    # Finalité/objectif de l'organisation
    purpose = Column(String, nullable=False)

    # Indique si l'organisation peut être facturée par la fédération
    billable = Column(Boolean, nullable=False)

    # Relation SQLAlchemy permettant de naviguer dans la hiérarchie de navigation
    parent = relationship("Organization", remote_side=[id])

    # Type de l'organisation
    type = Column(
        Enum(OrganizationType, name="organization_type_enum"),
        nullable=False
    )