from pydantic import BaseModel
from datetime import date

class ContactOutput(BaseModel):
    id: int
    email:str | None = None
    phone:str | None = None
    website:str | None = None

    # Permet à Pydantic de lire les attributs d'un objet SQLAlchemy directement
    # sans ça, Pydantic ne sait pas convertir un objet ORM en modèle Pydantic
    model_config = {"from_attributes": True}

class UserOutput(BaseModel):
    id: int
    first_names: list[str]
    last_name: str
    birth_date: date | None = None
    gender: str | None = None
    totem: str | None = None
    quali: str | None = None
    is_legal_guardian: bool
    contact: ContactOutput | None = None

    model_config = {"from_attributes": True}