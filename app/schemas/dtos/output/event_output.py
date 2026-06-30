from datetime import datetime
from typing import List
from pydantic import BaseModel, UUID4, Field, ConfigDict
from app.schemas.dtos.output.address_output import AddressOutput
from app.schemas.dtos.output.identifier_output import IdentifierOutput

class AudienceOutput(BaseModel):
    id: UUID4
    label: str | None = Field(default=None, alias="skos:prefLabel")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

class EventOutput(BaseModel):
    identifiers: list[IdentifierOutput] = Field(alias="dcterms:identifier")
    name: str = Field(alias="dcterms:name")
    description: str | None = Field(default=None, alias="dcterms:description")
    event_type: str = Field(alias="dcterms:type")
    # start_date and end_date are structural (should be time:Interval), to be addressed in a later pass
    start_date: datetime | None = None
    end_date: datetime | None = None
    # latitude and longitude are structural (should be locn:Geometry), to be addressed in a later pass
    latitude: float | None = None
    longitude: float | None = None
    parent_id: UUID4 | None = Field(default=None, alias="cpsvap:parentEvent")
    max_participants: int = Field(alias="sgp:maxParticipants")
    audiences: List[AudienceOutput] = Field(default=[], alias="cpsvap:audience")
    address: AddressOutput | None = Field(default=None, alias="locn:address")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)