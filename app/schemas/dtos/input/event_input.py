from datetime import datetime
from typing import List, Self
from pydantic import BaseModel, ConfigDict, Field, UUID4, field_validator, model_validator
from app.schemas.dtos.input.address_input import AddressCreateInput, AddressUpdateInput


class AudienceInput(BaseModel):
    id: UUID4
    label: str | None = Field(default=None, alias="skos:prefLabel")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CreateEventInput(BaseModel):
    name: str = Field(..., alias="dcterms:name")
    description: str | None = Field(default=None, alias="dcterms:description")
    event_type: str = Field(..., alias="dcterms:type")
    start_date: datetime | None = None
    end_date: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None
    parent_id: UUID4 | None = Field(default=None, alias="cpsvap:parentEvent")
    max_participants: int = Field(default=50, gt=0, le=100, alias="sgp:maxParticipants")
    audiences: List[AudienceInput] | None = Field(default=None, alias="cpsvap:audience")
    address: AddressCreateInput | None = Field(default=None, alias="locn:address")
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%d %H:%M")
        return v

    @model_validator(mode="after")
    def validate_event_rules(self) -> Self:
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self

    @model_validator(mode="after")
    def validate_location(self) -> Self:
        has_address = self.address is not None
        has_latitude = self.latitude is not None
        has_longitude = self.longitude is not None

        if has_latitude != has_longitude:
            raise ValueError("Latitude and longitude muse both be provided together")
        has_gps = has_latitude and has_longitude
        if has_address and has_gps:
            raise ValueError("GPS and address fields cannot be both at the same time")
        return self


class UpdateEventInput(BaseModel):
    name: str | None = Field(default=None, alias="dcterms:name")
    description: str | None = Field(default=None, alias="dcterms:description")
    event_type: str | None = Field(default=None, alias="dcterms:type")
    start_date: datetime | None = None
    end_date: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None
    parent_id: UUID4 | None = Field(default=None, alias="cpsvap:parentEvent")
    max_participants: int | None = Field(default=None, gt=0, le=100, alias="sgp:maxParticipants")
    audiences: List[AudienceInput] | None = Field(default=None, alias="cpsvap:audience")
    address: AddressUpdateInput | None = Field(default=None, alias="locn:address")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def parse_date(cls, v):
        if isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%d %H:%M")
        return v

    @model_validator(mode="after")
    def validate_event_rules(self) -> Self:
        if self.start_date and self.end_date and self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class InvitationEmailInput(BaseModel):
    event_id: UUID4
    invited_id: UUID4
    inviter_id: UUID4
