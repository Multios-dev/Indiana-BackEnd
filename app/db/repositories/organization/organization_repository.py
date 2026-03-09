from app.db.models.organization_model import Organization
from app.db.repositories.organization.organization_interface import OrganizationInterface

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class OrganizationRepository(OrganizationInterface):
    def __init__(self, db:AsyncSession):
        # On garde une référence à la session db
        # Cette session permettra d'exécuter les requêtes
        self.db = db

    async def get_all_organizations(self):
        stmt = select(Organization)
        result = await self.db.execute(stmt)
        return result.scalars().all()