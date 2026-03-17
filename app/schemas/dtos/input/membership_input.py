from datetime import date
from pydantic import BaseModel
from decimal import Decimal

class CreateMembershipInput(BaseModel):
    user_id: int
    organization_id: int
    role: str
    start_date: date
    end_date: date | None = None
    price:Decimal | None = None

class UpdateMembershipInput(BaseModel):
    role: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    price: Decimal | None = None