from pydantic import BaseModel

class ContactInput(BaseModel):
    email:str | None = None
    phone:str | None = None
    website:str | None = None

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
    contact:ContactInput | None = None

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
    contact:ContactInput | None = None