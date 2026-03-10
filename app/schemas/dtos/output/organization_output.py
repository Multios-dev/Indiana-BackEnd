from pydantic import BaseModel
from typing import Optional

class GetOrganizationOutput(BaseModel):
    id: int
    name: str
    acronym: Optional[str]
    type: str

    parent_id: Optional[int]

    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]

    street: Optional[str]
    city: Optional[str]
    zip: Optional[str]
    country: Optional[str]

    legal_form: str
    purpose: str
    billable: bool