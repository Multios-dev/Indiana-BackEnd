from datetime import datetime
from typing import List
from pydantic import BaseModel

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

    model_config = {"from_attributes": True}