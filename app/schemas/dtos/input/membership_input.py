from datetime import date
from pydantic import BaseModel, ConfigDict, Field, UUID4, field_validator, model_validator
from decimal import Decimal
from typing import Self


class CreateMembershipInput(BaseModel):
    user_id: UUID4 = Field(..., alias="org:member")
    organization_id: UUID4 = Field(..., alias="org:organization")
    role: str = Field(..., alias="org:role")
    start_date: date
    end_date: date | None = None
    price: Decimal | None = Field(default=None, alias="cac:LegalMonetaryTotal")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be less than start date")
        return self


class UpdateMembershipInput(BaseModel):
    role: str | None = Field(default=None, alias="org:role")
    start_date: date | None = None
    end_date: date | None = None
    price: Decimal | None = Field(default=None, alias="cac:LegalMonetaryTotal")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v

    @model_validator(mode="after")
    def validate_dates(self) -> Self:
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValueError("End date cannot be less than start date")
        return self
