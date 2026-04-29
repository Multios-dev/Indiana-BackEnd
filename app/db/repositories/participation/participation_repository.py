from uuid import UUID
from sqlalchemy import select, update
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

    async def get_participation(self, user_id:UUID, event_id:UUID) -> Participation:
        stmt = (select(Participation)
                .where(Participation.user_id == user_id, Participation.event_id == event_id))

        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_participation(self, participation_id: UUID, data: dict) -> Participation | None:
        async with self.db.begin():
            stmt = (
                update(Participation)
                .where(Participation.id == participation_id)
                .values(**data)
                .returning(Participation)
            )
            result = await self.db.execute(stmt)
            return result.scalar_one_or_none()