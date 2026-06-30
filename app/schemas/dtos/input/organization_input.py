import re
from pydantic import BaseModel, ConfigDict, EmailStr, Field, UUID4, field_validator
from app.db.models.enums.organization_type import OrganizationType
from app.schemas.dtos.input.address_input import AddressCreateInput, AddressUpdateInput


class ContactInput(BaseModel):
    email: EmailStr | None = Field(default=None, alias="cpsvap:email")
    phone: str | None = Field(default=None, alias="cpsvap:telephone")
    website: str | None = Field(default=None, alias="cpsvap:contactPage")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("phone")
    def validate_phone(cls, v):
        if v is None:
            return None
        if not re.match(r"^\+?[0-9]{8,15}$", v):
            raise ValueError("Invalid phone number")
        return v

    @field_validator("website")
    def validate_website(cls, v):
        if v is None:
            return None
        if not re.match(r"^https?://", v):
            raise ValueError("website must start with http:// or https://")
        return v


class CreateOrganizationInput(BaseModel):
    name: str = Field(..., alias="skos:prefLabel")
    acronym: str | None = Field(default=None, alias="skos:altLabel")
    logo: str | None = None
    parent_id: UUID4 | None = Field(default=None, alias="org:suborganizationOf")
    purpose: str = Field(..., alias="org:purpose")
    org_type: OrganizationType | None = Field(default=None, alias="rov:orgType")
    sgp_type: str | None = Field(default=None, alias="dcterms:type")
    billable: bool = Field(..., alias="sgp:billable")
    is_legal_entity: bool = Field(default=False, alias="sgp:isLegalEntity")
    contact: ContactInput | None = Field(default=None, alias="cpsvap:contactPoint")
    address: AddressCreateInput | None = Field(default=None, alias="cpsvap:hasAddress")
    model_config = ConfigDict(populate_by_name=True)


class UpdateOrganizationInput(BaseModel):
    name: str | None = Field(default=None, alias="skos:prefLabel")
    acronym: str | None = Field(default=None, alias="skos:altLabel")
    logo: str | None = None
    parent_id: UUID4 | None = Field(default=None, alias="org:suborganizationOf")
    purpose: str | None = Field(default=None, alias="org:purpose")
    org_type: OrganizationType | None = Field(default=None, alias="rov:orgType")
    sgp_type: str | None = Field(default=None, alias="dcterms:type")
    billable: bool | None = Field(default=None, alias="sgp:billable")
    is_legal_entity: bool | None = Field(default=None, alias="sgp:isLegalEntity")
    contact: ContactInput | None = Field(default=None, alias="cpsvap:contactPoint")
    address: AddressUpdateInput | None = Field(default=None, alias="cpsvap:hasAddress")
    model_config = ConfigDict(populate_by_name=True)
