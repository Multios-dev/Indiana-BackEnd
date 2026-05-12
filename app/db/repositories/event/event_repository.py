from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.participation_model import Participation
from app.db.repositories.event.event_interface import EventInterface
from app.db.models.event_model import Event, Audience
from sqlalchemy.orm import selectinload
from sqlalchemy import select, and_, func
from uuid import UUID
from datetime import datetime

class EventRepository(EventInterface):
    ALLOWED_FILTERS = {"name", "event_type", "start_date", "end_date"}
    TYPE_MAP = {
        "name": str,
        "event_type": str,
        "start_date": datetime,
        "end_date": datetime,
    }

    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_all_events(self, skip:int, limit:int, filters:dict | None = None):
        stmt = (select(Event)
                .options(
            selectinload(Event.audiences),
                    selectinload(Event.address)
                )
        )
        conditions=[]

        if filters:
            for key, value in filters.items():
                if key not in self.ALLOWED_FILTERS or not hasattr(Event, key):
                    continue
                try:
                    casted = self.TYPE_MAP[key](value)
                    conditions.append(getattr(Event, key) == casted)
                except (ValueError, TypeError):
                    continue

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_event_by_id(self, event_id:UUID):
        stmt = (select(Event)
                .where(Event.id == event_id)
                .options(selectinload(Event.audiences), selectinload(Event.address))
                )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_event(self, event: Event):
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)

        # Reload with audiences
        stmt = (select(Event)
                .where(Event.id == event.id)
                .options(selectinload(Event.audiences), selectinload(Event.address))
                )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def update_event(self, event_id:UUID, data: dict):
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

            # Reload with audiences and addresses
            stmt = (select(Event)
                    .where(Event.id == event_id)
                    .options(selectinload(Event.audiences), selectinload(Event.address))
                    )
            result = await self.db.execute(stmt)
            return result.scalar_one()

        except Exception:
            await self.db.rollback()
            raise

    async def delete_event(self, event_id: UUID):
        stmt = (
            select(Event)
            .where(Event.id == event_id)
            .options(selectinload(Event.audiences), selectinload(Event.address))
        )
        result = await self.db.execute(stmt)
        event_found = result.scalar_one_or_none()

        if not event_found:
            return None

        await self.db.delete(event_found)
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        return True

    async def count_events(self) -> int:
        stmt = select(func.count()).select_from(Event)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_participant_count(self, event_id: UUID) -> int:
        stmt = select(func.count(Participation.id)).where(
            Participation.event_id == event_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_audiences_by_ids(self, audience_ids: list[int]):
        stmt = select(Audience).where(Audience.id.in_(audience_ids))
        result = await self.db.execute(stmt)
        return result.scalars().all()