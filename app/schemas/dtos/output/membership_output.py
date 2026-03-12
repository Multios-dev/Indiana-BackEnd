from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal


class GetMembershipOutput(BaseModel):
    id:int
    user_id:int
    organization_id:int
    role:str
    start_date:datetime
    end_date:datetime | None = None
    price:Decimal | None = None