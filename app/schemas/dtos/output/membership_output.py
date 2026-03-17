from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class MembershipOutput(BaseModel):
    id: int
    user_id: int
    organization_id: int
    role: str
    start_date: date
    end_date: date | None = None
    price: Decimal | None = None

    model_config = {"from_attributes": True}