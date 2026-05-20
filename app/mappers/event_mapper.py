from app.db.models.address_model import Address
from app.db.models.event_model import Event
from app.schemas.dtos.input.event_input import CreateEventInput, InvitationEmailInput
from datetime import datetime
from uuid import UUID

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

    @staticmethod
    def to_invitation_input(event_id: UUID, invited_id: UUID, inviter_id: UUID) -> InvitationEmailInput:
        return InvitationEmailInput(event_id=event_id, invited_id=invited_id, inviter_id=inviter_id)