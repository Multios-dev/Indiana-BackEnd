from datetime import datetime
from typing import List, Self
from pydantic import BaseModel, model_validator

class AudienceInput(BaseModel):
    id:int
    label:str | None = None

    model_config = {"from_attributes": True}

class CreateEventInput(BaseModel):
    name:str
    description:str | None = None
    event_type:str
    start_date:datetime | None = None
    end_date:datetime | None = None
    latitude:float | None = None
    longitude:float | None = None
    parent_id:int | None = None
    audiences:List[AudienceInput] | None = None

    # model_validator car on compare plusieurs champs entre eux
    @model_validator(mode="after")
    def validate_event_rules(self) -> Self:
        # Cohérence temporelle : end_date doit être après start_date
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self

    model_config = {"from_attributes": True}

class UpdateEventInput(BaseModel):
    name:str | None = None
    description:str | None = None
    event_type:str | None = None
    start_date:datetime | None = None
    end_date:datetime | None = None
    latitude:float | None = None
    longitude:float | None = None
    parent_id:int | None = None
    audiences:List[AudienceInput] | None = None

    # model_validator car on compare plusieurs champs entre eux
    @model_validator(mode="after")
    def validate_event_rules(self) -> Self:
        # Cohérence temporelle : end_date doit être après start_date
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")

        return self

    model_config = {"from_attributes": True}