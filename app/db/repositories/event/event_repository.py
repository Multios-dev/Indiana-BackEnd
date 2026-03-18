from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.event.event_interface import EventInterface

from app.db.models.event_model import Event

from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_

class EventRepository(EventInterface):
    def __init__(self, db:AsyncSession):
        self.db = db

    # Récupérer tous les événements
    async def get_all_events(self, filters:dict | None = None):
        stmt = select(Event).options(selectinload(Event.audiences))
        conditions=[]

        if filters:
            allowed_filters = {
                "name",
                "event_type",
                "start_date",
                "end_date"
            }

            for key, value in filters.items():
                if key in allowed_filters and hasattr(Event, key):
                    conditions.append(getattr(Event, key) == value)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    # Récupérer un événement spécifique
    async def get_event_by_id(self, event_id:int):
        stmt = select(Event).where(Event.id == event_id).options(selectinload(Event.audiences))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()