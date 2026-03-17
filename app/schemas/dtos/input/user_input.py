from pydantic import BaseModel
from datetime import date

class ContactInput(BaseModel):
    email:str | None = None
    phone: str | None = None
    # website pas inclus (les personnes n'ont pas de page web)

class UserCreateInput(BaseModel):
    first_names: list[str]
    last_name: str
    birth_date: date | None = None
    gender: str | None = None
    totem: str | None = None
    quali: str | None = None
    is_legal_guardian: bool = False
    contact:ContactInput | None = None

class UserUpdateInput(BaseModel):
    first_names: list[str] | None = None
    last_name: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    totem: str | None = None
    quali: str | None = None
    is_legal_guardian: bool | None = None
    contact:ContactInput | None = None