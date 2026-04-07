import re
from pydantic import BaseModel, field_validator, EmailStr, UUID4
from app.db.models.enums.organization_type import OrganizationType

class ContactInput(BaseModel):
    email:EmailStr | None = None
    phone:str | None = None
    website:str | None = None

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
        # Accepts http:// or https://
        if not re.match(r"^https?://", v):
            raise ValueError("website must start with http:// or https://")
        return v

class CreateOrganizationInput(BaseModel):
    name: str
    acronym: str | None = None
    logo: str | None = None
    parent_id: UUID4 | None = None
    purpose: str
    org_type: OrganizationType | None = None
    sgp_type: str | None = None
    billable: bool
    is_legal_entity: bool = False
    contact:ContactInput | None = None

class UpdateOrganizationInput(BaseModel):
    name: str | None = None
    acronym: str | None = None
    logo: str | None = None
    parent_id: UUID4 | None = None
    purpose: str | None = None
    org_type: OrganizationType | None = None
    sgp_type: str | None = None
    billable: bool | None = None
    is_legal_entity: bool | None = None
    contact:ContactInput | None = None