from pydantic import BaseModel, UUID4, Field, ConfigDict
from datetime import date
from app.schemas.dtos.output.address_output import AddressOutput
from app.schemas.dtos.output.identifier_output import IdentifierOutput

class ContactOutput(BaseModel):
    id: UUID4
    email: str | None = Field(default=None, alias="cpsvap:email")
    phone: str | None = Field(default=None, alias="cpsvap:telephone")
    website: str | None = Field(default=None, alias="cpsvap:contactPage")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class UserOutput(BaseModel):
    identifiers: list[IdentifierOutput] = Field(alias="dcterms:identifier")
    first_names: list[str] = Field(alias="foaf:givenName")
    last_name: str = Field(alias="foaf:familyName")
    birth_date: date | None = Field(default=None, alias="cpsvap:birthDate")
    gender: str | None = Field(default=None, alias="cpsvap:gender")
    nationality: list[str] | None = Field(default=None, alias="sgp:nationality")
    totem: str | None = Field(default=None, alias="dcterms:alternative")
    quali: str | None = Field(default=None, alias="dcterms:description")
    is_legal_guardian: bool = Field(alias="sgp:isLegalGuardian")
    contact: ContactOutput | None = Field(default=None, alias="cpsvap:contactPoint")
    home_address: AddressOutput | None = Field(default=None, alias="cpsvap:domicile")
    residential_address: AddressOutput | None = Field(default=None, alias="VL:verblijfsadres")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class UserLoginOutput(BaseModel):
    id: UUID4
    email:str
