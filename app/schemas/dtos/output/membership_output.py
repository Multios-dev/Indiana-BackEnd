from pydantic import BaseModel, UUID4
from datetime import date
from decimal import Decimal

class MembershipOutput(BaseModel):
    id: UUID4
    user_id: UUID4
    organization_id: UUID4
    role: str
    start_date: date
    end_date: date | None = None
    price: Decimal | None = None

    model_config = {"from_attributes": True}