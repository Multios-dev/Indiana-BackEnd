from pydantic import BaseModel

class GetOrganizationOutput(BaseModel):
    id: int
    name: str
    acronym:str | None = None
    type: str

    parent_id:int | None = None

    email:str | None = None
    phone:str | None = None
    website:str | None = None

    street:str | None = None
    city:str| None = None
    zip:str | None = None
    country:str | None = None

    legal_form: str
    purpose: str
    billable: bool