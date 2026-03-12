from pydantic import BaseModel
from app.db.models.enums.organization_type import OrganizationType


class CreateOrganizationInput(BaseModel):

    name: str
    acronym:str | None = None
    logo:str | None = None
    parent_id:int | None = None

    email:str | None = None
    phone:str | None = None
    website:str | None = None

    street:str | None = None
    city:str | None = None
    zip:str | None = None
    country:str | None = None

    identifiers:dict | None = None

    legal_form: str
    purpose: str
    billable: bool

    type: OrganizationType

class UpdateOrganizationInput(BaseModel):
    name:str | None = None
    acronym:str | None = None
    logo:str | None = None

    parent_id:int | None = None

    email:str | None = None
    phone:str | None = None
    website:str | None = None

    street:str | None = None
    city:str | None = None
    zip:str | None = None
    country:str | None = None

    legal_form:str | None = None
    purpose:str | None = None
    billable:bool | None = None

    type:OrganizationType | None = None