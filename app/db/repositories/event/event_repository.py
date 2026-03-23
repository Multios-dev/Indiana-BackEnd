from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.event.event_interface import EventInterface

from app.db.models.event_model import Event, Audience

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

    # Créer un événement
    async def create_event(self, event: Event):
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)

        # Recharger avec les audiences
        stmt = select(Event).where(Event.id == event.id).options(selectinload(Event.audiences))
        result = await self.db.execute(stmt)
        return result.scalar_one()

    # Modifier un événement
    async def update_event(self, event_id, data:dict):
        try:
            stmt = select(Event).where(Event.id == event_id)
            result = await self.db.execute(stmt)
            event_found = result.scalar_one_or_none()

            if not event_found:
                return None

            for key, value in data.items():
                if key != "id" and hasattr(event_found, key):
                    setattr(event_found, key, value)

            await self.db.commit()
            await self.db.refresh(event_found)
            return event_found

        except Exception:
            await self.db.rollback()
            raise

    # Supprimer une organisation
    async def delete_event(self, event_id:int):
        try:
            stmt = select(Event).where(Event.id == event_id).options(selectinload(Event.audiences))
            result = await self.db.execute(stmt)
            event_found = result.scalar_one_or_none()

            if not event_found:
                return None

            await self.db.delete(event_found)
            await self.db.commit()
            return event_found

        except Exception:
            await self.db.rollback()
            raise

    async def get_audiences_by_ids(self, audience_ids: list[int]):
        stmt = select(Audience).where(Audience.id.in_(audience_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()