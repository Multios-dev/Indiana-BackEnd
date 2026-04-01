from datetime import datetime
from typing import List, Self
from pydantic import BaseModel, ConfigDict, model_validator, field_validator, UUID4

class AudienceInput(BaseModel):
    id: UUID4
    label: str | None = None
    model_config = ConfigDict(from_attributes=True)

class CreateEventInput(BaseModel):
    name: str
    description: str | None = None
    event_type: str
    start_date: datetime | None = None
    end_date: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None
    parent_id: UUID4 | None = None
    audiences: List[AudienceInput] | None = None

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

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Camp d'été",
                "description": "Camp annuel",
                "event_type": "camp",
                "start_date": "2026-07-01 09:00",
                "end_date": "2026-07-07 18:00",
                "latitude": 50.8503,
                "longitude": 4.3517,
                "audiences": [{"id": 1}]
            }
        }
    )

class UpdateEventInput(BaseModel):
    name: str | None = None
    description: str | None = None
    event_type: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    latitude: float | None = None
    longitude: float | None = None
    parent_id: int | None = None
    audiences: List[AudienceInput] | None = None

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

    model_config = ConfigDict(from_attributes=True)