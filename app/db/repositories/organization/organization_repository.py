from app.db.models.organization_model import Organization
from app.db.repositories.organization.organization_interface import OrganizationInterface

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class OrganizationRepository(OrganizationInterface):
    def __init__(self, db:AsyncSession):
        # On garde une référence à la session db
        # Cette session permettra d'exécuter les requêtes
        self.db = db

    # Récupérer toutes les organisations
    async def get_all_organizations(self):
        stmt = select(Organization)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # Récupérer une organisation par son id
    async def get_organization_by_id(self, id:int):
        stmt = select(Organization).where(Organization.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # Créer une organisation
    async def create_organization(self, organization:Organization):
        self.db.add(organization)
        await self.db.commit()
        await self.db.refresh(organization)
        return organization