from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class GetMembershipOutput(BaseModel):
    id:int
    user_id:int
    organization_id:int
    start_date:datetime
    end_date:Optional[datetime] = None
    price:Optional[Decimal] = None