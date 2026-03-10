from pydantic import BaseModel
from typing import Optional
from app.db.models.enums.organization_type import OrganizationType


class CreateOrganizationInput(BaseModel):

    name: str
    acronym: Optional[str] = None
    logo: Optional[str] = None

    parent_id: Optional[int] = None

    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None

    street: Optional[str] = None
    city: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None

    identifiers: Optional[dict] = None

    legal_form: str
    purpose: str
    billable: bool

    type: OrganizationType