from app.db.models.organization_model import Organization
from app.db.repositories.organization.organization_repository import OrganizationRepository

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.dtos.input.create_organization_input import CreateOrganizationInput


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

    # Créer une organisation
    async def create_organization(self, payload: CreateOrganizationInput) -> Organization:
        organization = Organization(
            name=payload.name,
            acronym=payload.acronym,
            logo=payload.logo,
            parent_id=None if payload.parent_id == 0 else payload.parent_id,
            email=payload.email,
            phone=payload.phone,
            website=payload.website,
            street=payload.street,
            city=payload.city,
            zip=payload.zip,
            country=payload.country,
            identifiers=payload.identifiers,
            legal_form=payload.legal_form,
            purpose=payload.purpose,
            billable=payload.billable,
            type=payload.type
        )

        return await self.repo.create_organization(organization)