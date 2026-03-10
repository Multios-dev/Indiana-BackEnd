from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.db.models.enums.organization_type import OrganizationType


class UpdateOrganizationInput(BaseModel):
    name: Optional[str] = None
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

    identifiers: Optional[Dict[str, Any]] = None

    legal_form: Optional[str] = None
    purpose: Optional[str] = None
    billable: Optional[bool] = None

    type: Optional[OrganizationType] = None