from pydantic import BaseModel

class ContactOutput(BaseModel):
    id: int
    email: str | None = None
    phone: str | None = None
    website: str | None = None

    model_config = {"from_attributes": True}

class OrganizationOutput(BaseModel):
    id: int
    name: str
    acronym: str | None = None
    purpose: str
    org_type: str
    sgp_type: str | None = None
    billable: bool
    is_legal_entity: bool
    parent_id: int | None = None
    contact: ContactOutput | None = None

    model_config = {"from_attributes": True}