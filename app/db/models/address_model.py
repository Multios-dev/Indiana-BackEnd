from sqlalchemy import Column, Integer, String

from app.db.base import Base

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    box_number = Column(String, nullable=False)
    street = Column(String, nullable=False)
    post_name = Column(String, nullable=False)
    post_code = Column(String, nullable=False)
    country = Column(String, nullable=False)