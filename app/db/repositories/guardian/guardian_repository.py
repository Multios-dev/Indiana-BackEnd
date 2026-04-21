from uuid import UUID
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.user_model import GuardianRelationship
from app.db.repositories.guardian.guardian_interface import GuardianInterface
from app.db.models.user_model import User
from sqlalchemy import select

class GuardianRepository(GuardianInterface):
    def __init__(self, db:AsyncSession):
        # Keep a reference to the db session
        # This session will be used to execute queries
        self.db = db

    async def add_guardian_relationship(self, guardian_id:UUID, minor_id:UUID):
        relation = GuardianRelationship(
            guardian_id=guardian_id,
            minor_id=minor_id
        )
        self.db.add(relation)
        await self.db.commit()
        return relation

    async def get_minors_by_guardian(self, guardian_id:UUID) -> List[User]:
        stmt = (
            select(User)
            .join(GuardianRelationship, User.id == GuardianRelationship.minor_id)
            .where(GuardianRelationship.guardian_id == guardian_id)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_guardians_by_minor(self, minor_id: UUID):
        stmt = (
            select(User)
            .join(GuardianRelationship, User.id == GuardianRelationship.guardian_id)
            .where(GuardianRelationship.minor_id == minor_id)
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_relationship(self, guardian_id:UUID, minor_id:UUID) -> GuardianRelationship:
        stmt = select(GuardianRelationship).where(
            GuardianRelationship.guardian_id == guardian_id,
            GuardianRelationship.minor_id == minor_id
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()