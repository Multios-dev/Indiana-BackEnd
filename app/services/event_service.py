from app.core.exceptions import EventNotFoundError, InvalidParentEventError, DatabaseError, EmptyUpdatePayloadError, \
    SelfParentEventError
from app.db.models.event_model import Event
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.repositories.event.event_repository import EventRepository
from app.db.session import get_db
from app.schemas.dtos.input.event_input import UpdateEventInput, CreateEventInput


def get_event_service(db: AsyncSession = Depends(get_db)):
    repo = EventRepository(db)
    return EventService(repo)

class EventService:
    def __init__(self, repo):
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
        # Vérif parent
        parent_id = None if payload.parent_id is None else payload.parent_id
        if parent_id is not None:
            parent = await self.repo.get_event_by_id(parent_id)
            if not parent:
                raise InvalidParentEventError()

        try:
            # Créer l'événement sans audiences d'abord
            event = Event(
                name = payload.name,
                description = payload.description,
                event_type = payload.event_type,
                start_date = payload.start_date,
                end_date = payload.end_date,
                latitude = payload.latitude,
                longitude = payload.longitude,
                parent_id = parent_id
            )

            # Gérer les audiences
            if payload.audiences:
                audience_ids = [a.id for a in payload.audiences]
                audiences = await self.repo.get_event_audiences_by_id(audience_ids)
                event.audiences = audiences
            return await self.repo.create_event(event)

        except Exception:
            raise DatabaseError()

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
        return deleted_event