from sqlalchemy import Column, Integer, String, Date, JSON

from app.db.base import Base

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)

    firstNames = Column(JSON, nullable=False)
    lastName = Column(String, nullable=False)

    birthDate = Column(Date, nullable=False)
    gender = Column(String, nullable=False)

    nationality = Column(String, nullable=False)

    street = Column(String, nullable=False)
    zip = Column(String, nullable=False)
    city = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    phone = Column(String, nullable=False)

    password_hash = Column(String, nullable=True)