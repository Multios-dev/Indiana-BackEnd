from uuid import UUID
from pydantic import BaseModel, field_validator
from decimal import Decimal

class ParticipationInvitationInput(BaseModel):
    user_id:UUID
    event_id:UUID
    role:str | None = "invited"
    price:Decimal | None = None

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v

class ParticipationUpdateInput(BaseModel):
    user_id:UUID | None = None
    event_id:UUID | None = None
    role:str | None = None
    price:Decimal | None = None

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v

class CreateParticipationInput(BaseModel):
    user_id:UUID
    event_id:UUID
    role:str | None = "inscribed"
    price:Decimal | None = None
    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v