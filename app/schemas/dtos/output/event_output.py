from datetime import datetime
from typing import List
from pydantic import BaseModel, UUID4

class AudienceOutput(BaseModel):
    id:UUID4
    label:str | None = None

    model_config = {"from_attributes": True}

class AddressOutput(BaseModel):
    id: UUID4
    thoroughfare: str
    box_number: str | None = None
    post_name: str
    post_code: str
    country: str

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
    audiences:List[AudienceOutput]=[]
    address:AddressOutput | None = None

    model_config = {"from_attributes": True}