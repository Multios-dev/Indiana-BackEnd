from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class CreateMembershipInput(BaseModel):
    user_id:int
    organization_id: int
    role:str
    start_date: datetime
    end_date: Optional[datetime] | None = None
    price: Optional[Decimal] | None = None