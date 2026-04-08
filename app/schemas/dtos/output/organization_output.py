from pydantic import BaseModel, UUID4
from app.db.models.enums.organization_type import OrganizationType


class ContactOutput(BaseModel):
    id: UUID4
    email: str | None = None
    phone: str | None = None
    website: str | None = None

    model_config = {"from_attributes": True}

class AddressOutput(BaseModel):
    id: UUID4
    thoroughfare: str
    box_number: str | None = None
    post_name: str
    post_code: str
    country: str

    model_config = {"from_attributes": True}

class OrganizationOutput(BaseModel):
    id: UUID4
    name: str
    acronym: str | None = None
    purpose: str
    org_type: OrganizationType
    sgp_type: str | None = None
    billable: bool
    is_legal_entity: bool
    parent_id: UUID4 | None = None
    contact: ContactOutput | None = None
    address: AddressOutput | None = None

    model_config = {"from_attributes": True}