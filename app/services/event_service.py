import traceback
from app.core.exceptions import EventNotFoundError, InvalidParentEventError, DatabaseError, EmptyUpdatePayloadError, \
    SelfParentEventError, ConflictingEventLocationError, UserInvitedNotFoundError, UserInviterNotFoundError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, BackgroundTasks
from app.db.repositories.address.address_repository import AddressRepository
from app.db.repositories.event.event_repository import EventRepository
from app.db.repositories.user.user_repository import UserRepository
from app.db.session import get_db
from app.mappers.event_mapper import EventMapper
from app.schemas.dtos.input.event_input import UpdateEventInput, CreateEventInput, InvitationEmailInput
from datetime import datetime
from uuid import UUID

from app.services.email_service import EmailService, get_email_service


def get_event_service(
        db: AsyncSession = Depends(get_db),
        email_service: EmailService = Depends(get_email_service),
):
    repo = EventRepository(db)
    address_repo = AddressRepository(db)
    user_repo = UserRepository(db)
    return EventService(repo, address_repo, user_repo, email_service)

def make_naive(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    # Si le datetime a tzinfo, on le retire
    return dt.replace(tzinfo=None)

class EventService:
    def __init__(
            self,
            repo:EventRepository,
            address_repo:AddressRepository,
            user_repo:UserRepository,
            email_service: EmailService
    ):
        self.repo = repo
        self.address_repo = address_repo
        self.user_repo = user_repo
        self.email_service = email_service

    async def get_all_events(self, skip:int, limit:int, filters:dict | None = None):
        events = await self.repo.get_all_events(skip, limit, filters)
        if not events:
            raise EventNotFoundError()
        return events

    async def get_event_by_id(self, event_id:UUID):
        event = await self.repo.get_event_by_id(event_id)
        if not event:
            raise EventNotFoundError()
        return event

    async def create_event(self, payload: CreateEventInput):
        parent_id = None if payload.parent_id is None else payload.parent_id
        if parent_id is not None:
            parent = await self.repo.get_event_by_id(parent_id)
            if not parent:
                raise InvalidParentEventError()

        try:
            if payload.address:
                address = EventMapper.to_address_entity(payload.address)
                created_address = await self.address_repo.create_address(address)
                address_id = created_address.id
            else:
                address_id = None

            event = EventMapper.to_event_entity(payload)
            event.address_id = address_id

            if payload.audiences:
                audience_ids = [a.id for a in payload.audiences]
                audiences = await self.repo.get_audiences_by_ids(audience_ids)
                event.audiences = audiences

            result = await self.repo.create_event(event)
            return result

        except Exception as e:
            print("ERROR:", e)
            raise DatabaseError(str(e))

    async def update_event(self, event_id:UUID, payload:UpdateEventInput):
        event = await self.repo.get_event_by_id(event_id)
        if not event:
            raise EventNotFoundError()

        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise EmptyUpdatePayloadError()

        if "parent_id" in data and data["parent_id"] == 0:
            data["parent_id"] = None

        if "parent_id" in data and data["parent_id"] is not None:
            parent = await self.repo.get_event_by_id(data["parent_id"])
            if not parent:
                raise InvalidParentEventError()
            if data["parent_id"] == parent.id:
                raise SelfParentEventError()

        audience_data = data.pop("audiences", None)
        if audience_data is not None:
            audience_ids = [a.id for a in audience_data]
            audiences = await self.repo.get_audiences_by_ids(audience_ids)
            event.audiences = audiences

        # Guard localisation exclusive
        if "address" in data and ("latitude" in data or "longitude" in data):
            raise ConflictingEventLocationError()
        if "address" in data and (event.latitude or event.longitude):
            raise ConflictingEventLocationError()
        if ("latitude" in data or "longitude" in data) and event.address_id:
            raise ConflictingEventLocationError()

        address_data = data.pop("address", None)
        if address_data is not None:
            new_address = EventMapper.to_address_entity(payload.address)
            created_address = await self.address_repo.create_address(new_address)
            data["address_id"] = created_address.id

        updated_event = await self.repo.update_event(event_id, data)
        if not updated_event:
            raise EventNotFoundError()
        return updated_event

    async def delete_event(self, event_id: UUID):
        deleted_event = await self.repo.get_event_by_id(event_id)
        if not deleted_event:
            raise EventNotFoundError()
        await self.repo.delete_event(event_id)
        return {"message": "Event deleted successfully"}

    async def count_events(self) -> int:
        return await self.repo.count_events()