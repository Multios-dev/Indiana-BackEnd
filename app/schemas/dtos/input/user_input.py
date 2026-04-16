from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date
import re

from app.schemas.dtos.input.address_input import AddressCreateInput, AddressUpdateInput

class ContactInput(BaseModel):
    # Email automatically validated by Pydantic
    email:EmailStr | None = None

    phone: str | None = None
    @field_validator("phone")
    def validate_phone(cls, v):
        # If no phone number, OK since it's an optional field
        if v is None:
            return None

        # Format check (digits + optional "+")
        if not re.match(r"^\+?[0-9]{8,15}$", v):
            raise ValueError("Invalid phone number")
        return v

    # website not included (people don't have web pages)

class UserCreateInput(BaseModel):
    # List of first names (at least 1)
    first_names: list[str] = Field(..., min_length=1)
    last_name: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    nationality: list[str] = Field(..., min_length=1)
    totem: str | None = None
    quali: str | None = None
    is_legal_guardian: bool = False
    password:str
    contact:ContactInput | None = None
    home_address:AddressCreateInput
    residential_address:AddressCreateInput | None = None

    @field_validator("birth_date")
    def validate_birth_date(cls, v):
        # Prevents a date in the future
        if v and v > date.today():
            raise ValueError("Invalid birth date")
        return v

class UserUpdateInput(BaseModel):
    first_names: list[str] | None = None
    last_name: str | None = None
    birth_date: date | None = None
    gender: str | None = None
    nationality: list[str] | None = None
    totem: str | None = None
    quali: str | None = None
    is_legal_guardian: bool | None = None
    contact:ContactInput | None = None
    home_address:AddressUpdateInput | None = None
    residential_address:AddressUpdateInput | None = None

    @field_validator("birth_date")
    def validate_birth_date(cls, v):
        if v and v > date.today():
            raise ValueError("Invalid birth date")
        return v

class UserLoginInput(BaseModel):
    email: str | None = None
    password: str | None = None