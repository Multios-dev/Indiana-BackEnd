from datetime import date
from pydantic import BaseModel, field_validator, model_validator
from decimal import Decimal
from typing import Self

class CreateMembershipInput(BaseModel):
    user_id: int
    organization_id: int
    role: str
    start_date: date
    end_date: date | None = None
    price:Decimal | None = None

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v

    # model_validator permet de valider plusieurs champs ensemble
    # ici, on compare start_date et end_date entre eux
    # "self" = l'objet complet avec tous ses champs accessibles via self.xxx
    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be less than start date")
        return self

class UpdateMembershipInput(BaseModel):
    role: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    price: Decimal | None = None

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v
    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.end_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be less than start date")
        return self