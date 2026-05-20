from decimal import Decimal
from pydantic import BaseModel
from uuid import UUID

class ParticipationOutput(BaseModel):
    id: UUID
    user_id: UUID
    event_id: UUID
    role:str
    price: Decimal | None = None