from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from decimal import Decimal


class ParticipationInvitationInput(BaseModel):
    user_id: UUID = Field(..., alias="cpsvap:hasParticipant")
    event_id: UUID
    role: str | None = Field(default="invited", alias="cpsvap:role")
    price: Decimal | None = Field(default=None, alias="cac:LegalMonetaryTotal")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v


class ParticipationUpdateInput(BaseModel):
    user_id: UUID | None = Field(default=None, alias="cpsvap:hasParticipant")
    event_id: UUID | None = None
    role: str | None = Field(default=None, alias="cpsvap:role")
    price: Decimal | None = Field(default=None, alias="cac:LegalMonetaryTotal")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v


class CreateParticipationInput(BaseModel):
    user_id: UUID = Field(..., alias="cpsvap:hasParticipant")
    event_id: UUID
    role: str | None = Field(default="inscribed", alias="cpsvap:role")
    price: Decimal | None = Field(default=None, alias="cac:LegalMonetaryTotal")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v
