from app.db.repositories.organization.organization_repository import OrganizationRepository

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

def get_organization_service(db:AsyncSession = Depends(get_db)):
    repo = OrganizationRepository(db)
    return OrganizationService(repo)

class OrganizationService:
    def __init__(self, repo:OrganizationRepository):
        self.repo = repo

    # Récupérer toutes les organisations
    async def get_all_organizations(self):
        organizations = await self.repo.get_all_organizations()
        if not organizations:
            raise ValueError("No organizations found")
        return organizations

    # Récupérer une organisation spécifique (par son id)
    async def get_organization_by_id(self, id:int):
        organization = await self.repo.get_organization_by_id(id)
        if not organization:
            raise ValueError("Organization not found")
        return organization