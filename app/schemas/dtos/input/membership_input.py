from datetime import datetime
from pydantic import BaseModel
from decimal import Decimal

class CreateMembershipInput(BaseModel):
    user_id:int
    organization_id: int
    role:str
    start_date: datetime
    end_date: datetime | None = None
    price: Decimal | None = None

class UpdateMembershipInput(BaseModel):
    user_id:int | None = None
    organization_id: int | None = None
    role:str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    price: Decimal | None = None