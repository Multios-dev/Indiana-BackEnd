from datetime import datetime
from typing import List
from pydantic import BaseModel, UUID4
from app.schemas.dtos.output.address_output import AddressOutput

class AudienceOutput(BaseModel):
    id:UUID4
    label:str | None = None

    model_config = {"from_attributes": True}

class EventOutput(BaseModel):
    id:UUID4
    name:str
    description:str | None = None
    event_type:str
    start_date:datetime | None = None
    end_date:datetime | None = None
    latitude:float | None = None
    longitude:float | None = None
    parent_id:UUID4 | None = None
    max_participants:int
    audiences:List[AudienceOutput]=[]
    address:AddressOutput | None = None

    model_config = {"from_attributes": True}