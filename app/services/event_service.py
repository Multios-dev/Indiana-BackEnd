from app.core.exceptions import EventNotFoundError, InvalidParentEventError, DatabaseError, EmptyUpdatePayloadError, \
    SelfParentEventError
from app.db.models.event_model import Event
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.repositories.event.event_repository import EventRepository
from app.db.session import get_db
from app.mappers.event_mapper import EventMapper
from app.schemas.dtos.input.event_input import UpdateEventInput, CreateEventInput
from datetime import datetime

def get_event_service(db: AsyncSession = Depends(get_db)):
    repo = EventRepository(db)
    return EventService(repo)

def make_naive(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    # Si le datetime a tzinfo, on le retire
    return dt.replace(tzinfo=None)

class EventService:
    def __init__(self, repo:EventRepository):
        self.repo = repo

    async def get_all_events(self, filters:dict | None = None):
        events = await self.repo.get_all_events(filters)
        if not events:
            raise EventNotFoundError()
        return events

    async def get_event_by_id(self, event_id:int):
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
            event = EventMapper.to_event_entity(payload)

            if payload.audiences:
                audience_ids = [a.id for a in payload.audiences]
                audiences = await self.repo.get_audiences_by_ids(audience_ids)
                event.audiences = audiences

            result = await self.repo.create_event(event)
            return result

        except Exception as e:
            print("ERROR:", e)
            raise DatabaseError(str(e))

    async def update_event(self, event_id:int, payload:UpdateEventInput):
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

        # -------------------------
        # GESTION AUDIENCES
        # -------------------------
        audience_data = data.pop("audiences", None)

        if audience_data is not None:
            audience_ids = [a.id for a in audience_data]

            audiences = await self.repo.get_audiences_by_ids(audience_ids)

            # Remplacer complètement la relation
            event.audiences = audiences

        updated_event = await self.repo.update_event(event_id, data)
        if not updated_event:
            raise EventNotFoundError()
        return updated_event

    async def delete_event(self, event_id:int):
        deleted_event = await self.repo.get_event_by_id(event_id)
        if not deleted_event:
            raise EventNotFoundError()
        await self.repo.delete_event(event_id)
        return { "message" : "Event deleted successfully" }
