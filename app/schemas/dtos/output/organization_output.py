from pydantic import BaseModel

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
    contact_id: int | None = None

    model_config = {"from_attributes": True}