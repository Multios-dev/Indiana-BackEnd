from app.db.models.address_model import Address
from app.db.models.event_model import Event
from app.schemas.dtos.input.event_input import CreateEventInput
from datetime import datetime

def make_naive(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    return dt.replace(tzinfo=None)

class EventMapper:
    @staticmethod
    def to_event_entity(payload: CreateEventInput) -> Event:
        data = payload.model_dump(exclude_none=True, exclude={"audiences", "address"})
        data["start_date"] = make_naive(payload.start_date)
        data["end_date"] = make_naive(payload.end_date)
        return Event(**data)

    @staticmethod
    def to_address_entity(address_payload) -> Address | None:
        data = address_payload.model_dump(exclude_none=True)
        return Address(**data)