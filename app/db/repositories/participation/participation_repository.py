from typing import List
from uuid import UUID
from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.participation_model import Participation
from app.db.repositories.participation.participation_interface import ParticipationInterface

class ParticipationRepository(ParticipationInterface):
    def __init__(self, db:AsyncSession):
        self.db = db

    async def invite_to_event(self, participation:Participation) ->bool:
        self.db.add(participation)
        await self.db.commit()
        await self.db.refresh(participation)
        return True

    async def get_participation_by_user_and_event(self, user_id:UUID, event_id:UUID) -> Participation:
        stmt = (select(Participation)
                .where(Participation.user_id == user_id, Participation.event_id == event_id))

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_participation_by_id(self, participation_id:UUID)->Participation:
        stmt = (select(Participation)
                .where(Participation.id == participation_id)
                )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_participation(self, participation_id: UUID, data: dict) -> Participation | None:
        stmt = (
            update(Participation)
            .where(Participation.id == participation_id)
            .values(**data)
            .returning(Participation)
        )
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def get_all_participations(self, filters:dict | None = None)->List[Participation]:
        stmt = select(Participation)

        conditions = []

        if filters:
            allowed_filters = {
                "event_id",
                "user_id"
            }

            for key, value in filters.items():
                if key in allowed_filters and hasattr(Participation, key):
                    conditions.append(getattr(Participation, key) == value)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def delete_participation(self, participation_id:UUID):
        participation_found = await self.get_participation_by_id(participation_id)
        if not participation_found:
            return None

        await self.db.delete(participation_found)
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

        return True

    async def create_participation(self, participation:Participation) ->Participation:
        self.db.add(participation)
        await self.db.commit()
        await self.db.refresh(participation)
        return participation