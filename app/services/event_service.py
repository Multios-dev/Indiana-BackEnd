from app.core.exceptions import EventNotFoundError

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.repositories.event.event_repository import EventRepository
from app.db.session import get_db

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