from app.db.models.organization_model import Organization

from app.db.repositories.organization.organization_repository import OrganizationRepository

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

from app.schemas.dtos.input.organization_input import UpdateOrganizationInput, CreateOrganizationInput

def get_organization_service(db:AsyncSession = Depends(get_db)):
    repo = OrganizationRepository(db)
    return OrganizationService(repo)

class OrganizationService:
    def __init__(self, repo:OrganizationRepository):
        self.repo = repo

    # Récupérer toutes les organisations
    async def get_all_organizations(self, filters:dict | None = None):
        organizations = await self.repo.get_all_organizations(filters)
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
        parent_id = None if payload.parent_id == 0 else payload.parent_id

        if parent_id is not None:
            parent = await self.repo.get_organization_by_id(parent_id)
            if not parent:
                raise ValueError("Parent organization does not exist")

        organization = Organization(
            name=payload.name,
            acronym=payload.acronym,
            logo=payload.logo,
            parent_id=parent_id,
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

    # Modifier une organisation
    async def update_organization(self,organization_id: int, payload: UpdateOrganizationInput):
        data = payload.model_dump(exclude_unset=True)

        if not data:
            raise ValueError("No data provided for update")

        # Gérer parent_id = 0 comme absence de parent
        if "parent_id" in data and data["parent_id"] == 0:
            data["parent_id"] = None

        # Vérifier que le parent existe si un parent_id est fourni
        if "parent_id" in data and data["parent_id"] is not None:
            parent = await self.repo.get_organization_by_id(data["parent_id"])
            if not parent:
                raise ValueError("Parent organization does not exist")

            # Empêcher une organisation d'être son propre parent
            if data["parent_id"] == organization_id:
                raise ValueError("An organization cannot be its own parent")

        updated = await self.repo.update_organization(organization_id, data)

        if not updated:
            raise ValueError("Organization not found")

        return updated

    async def delete_organization(self, organization_id: int):
        deleted = await self.repo.delete_organization(organization_id)
        if not deleted:
            raise ValueError("Organization not found")
        return deleted