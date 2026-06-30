from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from app.db.models.identifier_model import Identifier
from app.db.repositories.identifier.identifier_interface import IdentifierInterface


class IdentifierRepository(IdentifierInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_identifier(
        self,
        entity_type: str,
        entity_id: UUID,
        creator: str,
        notation: str,
    ) -> Identifier:
        identifier = Identifier(
            entity_type=entity_type,
            entity_id=entity_id,
            creator=creator,
            notation=notation,
        )
        self.db.add(identifier)
        await self.db.commit()
        await self.db.refresh(identifier)
        return identifier

    async def get_identifiers_for_entity(
        self,
        entity_type: str,
        entity_id: UUID,
    ) -> list[Identifier]:
        stmt = select(Identifier).where(
            Identifier.entity_type == entity_type,
            Identifier.entity_id == entity_id,
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
