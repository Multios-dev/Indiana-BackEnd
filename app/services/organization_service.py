from app.db.models.organization_model import Organization
from app.db.repositories.organization.organization_repository import OrganizationRepository

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.dtos.input.organization_input import UpdateOrganizationInput, CreateOrganizationInput

from app.core.exceptions import (
    OrganizationNotFoundError,
    EmptyUpdatePayloadError,
    BadRequestError,
    DatabaseError, InvalidParentOrganizationError, SelfParentOrganizationError,
)

def get_organization_service(db: AsyncSession = Depends(get_db)):
    repo = OrganizationRepository(db)
    return OrganizationService(repo)

class OrganizationService:
    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    async def get_all_organizations(self, filters: dict | None = None):
        organizations = await self.repo.get_all_organizations(filters)
        if not organizations:
            raise OrganizationNotFoundError()
        return organizations

    async def get_organization_by_id(self, id: int):
        organization = await self.repo.get_organization_by_id(id)
        if not organization:
            raise OrganizationNotFoundError()
        return organization

    async def create_organization(self, payload: CreateOrganizationInput) -> Organization:
        parent_id = None if payload.parent_id == 0 else payload.parent_id
        if parent_id is not None:
            parent = await self.repo.get_organization_by_id(parent_id)
            if not parent:
                raise InvalidParentOrganizationError()

        try:
            organization = Organization(
                name=payload.name,
                acronym=payload.acronym,
                logo=payload.logo,
                parent_id=parent_id,
                purpose=payload.purpose,
                org_type=payload.org_type,
                sgp_type=payload.sgp_type,
                billable=payload.billable,
                is_legal_entity=payload.is_legal_entity,
                contact_id=payload.contact_id,
            )
            return await self.repo.create_organization(organization)
        except Exception:
            raise DatabaseError()

    async def update_organization(self, organization_id: int, payload: UpdateOrganizationInput):
        data = payload.model_dump(exclude_unset=True)

        if not data:
            raise EmptyUpdatePayloadError()

        if "parent_id" in data and data["parent_id"] == 0:
            data["parent_id"] = None

        if "parent_id" in data and data["parent_id"] is not None:
            parent = await self.repo.get_organization_by_id(data["parent_id"])
            if not parent:
                raise InvalidParentOrganizationError()
            if data["parent_id"] == organization_id:
                raise SelfParentOrganizationError()

        updated = await self.repo.update_organization(organization_id, data)
        if not updated:
            raise OrganizationNotFoundError()
        return updated

    async def delete_organization(self, organization_id: int):
        deleted = await self.repo.delete_organization(organization_id)
        if not deleted:
            raise OrganizationNotFoundError()
        return deleted