from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from datetime import date
import re
import pycountry

from app.schemas.dtos.input.address_input import AddressCreateInput, AddressUpdateInput

class ContactInput(BaseModel):
    email: EmailStr | None = Field(default=None, alias="cpsvap:email")
    phone: str | None = Field(default=None, alias="cpsvap:telephone")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("phone")
    def validate_phone(cls, v):
        if v is None:
            return None
        if not re.match(r"^\+?[0-9]{8,15}$", v):
            raise ValueError("Invalid phone number")
        return v


class UserCreateInput(BaseModel):
    first_names: list[str] = Field(..., min_length=1, alias="foaf:givenName")
    last_name: str | None = Field(default=None, alias="foaf:familyName")
    birth_date: date | None = Field(default=None, alias="cpsvap:birthDate")
    gender: str | None = Field(default=None, alias="cpsvap:gender")
    nationality: list[str] = Field(..., min_length=1, alias="sgp:nationality")
    totem: str | None = Field(default=None, alias="dcterms:alternative")
    quali: str | None = Field(default=None, alias="dcterms:description")
    is_legal_guardian: bool = Field(default=False, alias="sgp:isLegalGuardian")
    password: str = Field(..., min_length=8)
    contact: ContactInput | None = Field(default=None, alias="cpsvap:contactPoint")
    home_address: AddressCreateInput = Field(..., alias="cpsvap:domicile")
    residential_address: AddressCreateInput | None = Field(default=None, alias="VL:verblijfsadres")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v):
        if v and v > date.today():
            raise ValueError("Invalid birth date")
        return v

    @field_validator("nationality", mode="before")
    @classmethod
    def validate_nationality(cls, v):
        if not isinstance(v, list):
            return v
        for code in v:
            if pycountry.countries.get(alpha_2=code) is None:
                raise ValueError(f"Invalid nationality code: {code}")
        return v


class UserUpdateInput(BaseModel):
    first_names: list[str] | None = Field(default=None, alias="foaf:givenName")
    last_name: str | None = Field(default=None, alias="foaf:familyName")
    birth_date: date | None = Field(default=None, alias="cpsvap:birthDate")
    gender: str | None = Field(default=None, alias="cpsvap:gender")
    nationality: list[str] | None = Field(default=None, alias="sgp:nationality")
    totem: str | None = Field(default=None, alias="dcterms:alternative")
    quali: str | None = Field(default=None, alias="dcterms:description")
    is_legal_guardian: bool | None = Field(default=None, alias="sgp:isLegalGuardian")
    contact: ContactInput | None = Field(default=None, alias="cpsvap:contactPoint")
    home_address: AddressUpdateInput | None = Field(default=None, alias="cpsvap:domicile")
    residential_address: AddressUpdateInput | None = Field(default=None, alias="VL:verblijfsadres")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v):
        if v and v > date.today():
            raise ValueError("Invalid birth date")
        return v

    @field_validator("nationality", mode="before")
    @classmethod
    def validate_nationality(cls, v):
        if v is None or not isinstance(v, list):
            return v
        for code in v:
            if pycountry.countries.get(alpha_2=code) is None:
                raise ValueError(f"Invalid nationality code: {code}")
        return v


class UserLoginInput(BaseModel):
    email: EmailStr
    password: str
