from pydantic import BaseModel

class CreateOrganizationInput(BaseModel):
    name: str
    acronym: str | None = None
    logo: str | None = None
    parent_id: int | None = None
    purpose: str
    org_type: str
    sgp_type: str | None = None
    billable: bool
    is_legal_entity: bool = False
    contact_id: int | None = None

class UpdateOrganizationInput(BaseModel):
    name: str | None = None
    acronym: str | None = None
    logo: str | None = None
    parent_id: int | None = None
    purpose: str | None = None
    org_type: str | None = None
    sgp_type: str | None = None
    billable: bool | None = None
    is_legal_entity: bool | None = None
    contact_id: int | None = None