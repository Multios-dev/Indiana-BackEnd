from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date
import re

class ContactInput(BaseModel):
    # Email validé automatiquement par Pydantic
    email:EmailStr | None = None

    phone: str | None = None
    @field_validator("phone")
    def validate_phone(cls, v):
        # Si pas de téléphone, OK car champ optionnel
        if v is None:
            return None

        # Vérification du format (chiffres + option "+")
        if not re.match(r"^\+?[0-9]{8,15}$", v):
            raise ValueError("Invalid phone number")
        return v

    # website pas inclus (les personnes n'ont pas de page web)

class UserCreateInput(BaseModel):
    # Liste de prénoms (au moins 1 prénom)
    first_names: list[str] = Field(..., min_length=1)
    last_name: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    totem: str | None = None
    quali: str | None = None
    is_legal_guardian: bool = False
    contact:ContactInput | None = None

    @field_validator("birth_date")
    def validate_birth_date(cls, v):
        # Empêche une date dans le futur
        if v and v > date.today():
            raise ValueError("Invalid birth date")
        return v

class UserUpdateInput(BaseModel):
    first_names: list[str] | None = None
    last_name: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    totem: str | None = None
    quali: str | None = None
    is_legal_guardian: bool | None = None
    contact:ContactInput | None = None

    @field_validator("birth_date")
    def validate_birth_date(cls, v):
        # Empêche une date dans le futur
        if v and v > date.today():
            raise ValueError("Invalid birth date")
        return v