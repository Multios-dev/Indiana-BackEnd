import traceback
from app.db.models.organization_model import Organization
from app.db.models.contact_model import Contact
from app.db.repositories.address.address_repository import AddressRepository
from app.db.repositories.organization.organization_repository import OrganizationRepository
from app.db.repositories.contact.contact_repository import ContactRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.mappers.organization_mapper import OrganizationMapper
from app.schemas.dtos.input.organization_input import UpdateOrganizationInput, CreateOrganizationInput
from app.core.exceptions import (
    OrganizationNotFoundError,
    EmptyUpdatePayloadError,
    DatabaseError,
    InvalidParentOrganizationError,
    SelfParentOrganizationError,
)
from uuid import UUID

def get_organization_service(db: AsyncSession = Depends(get_db)):
    repo = OrganizationRepository(db)
    contact_repo = ContactRepository(db)
    address_repo = AddressRepository(db)
    return OrganizationService(repo, contact_repo, address_repo)

class OrganizationService:
    def __init__(self, repo: OrganizationRepository, contact_repo: ContactRepository, address_repo: AddressRepository):
        self.repo = repo
        self.contact_repo = contact_repo
        self.address_repo = address_repo

    async def get_all_organizations(self, skip:int, limit:int, filters: dict | None = None):
        organizations = await self.repo.get_all_organizations(skip, limit, filters)
        if not organizations:
            raise OrganizationNotFoundError()
        return organizations

    async def get_organization_by_id(self, org_id: UUID):
        organization = await self.repo.get_organization_by_id(org_id)
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
            if payload.address:
                address = OrganizationMapper.to_address_entity(payload.address)
                created_address = await self.address_repo.create_address(address)
                address_id = created_address.id
            else:
                address_id = None

            organization = OrganizationMapper.to_organization_entity(payload)
            organization.address_id = address_id
            created = await self.repo.create_organization(organization)

            contact = OrganizationMapper.to_contact_entity(payload, created.id)
            if contact:
                await self.contact_repo.create_contact(contact)
                created = await self.repo.get_organization_by_id(created.id)

            return created
        except Exception as e:
            print ("DatabaseError : ", e)
            traceback.print_exc()
            raise DatabaseError() from e

    async def update_organization(self, organization_id: UUID, payload: UpdateOrganizationInput):
        organization = await self.repo.get_organization_by_id(organization_id)
        if not organization:
            raise OrganizationNotFoundError()

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

        # Handle contact separately
        contact_data = data.pop("contact", None)

        if contact_data:
            if organization.contact:
                # Update the existing contact
                await self.contact_repo.update_contact(organization.contact.id, contact_data)
            else:
                # Crate a new contact
                contact = Contact(
                    email=contact_data.get("email"),
                    phone=contact_data.get("phone"),
                    website=contact_data.get("website"),
                    org_id=organization_id,
                )
                await self.contact_repo.create_contact(contact)

        # Update the organization's fields
        if data:
            updated = await self.repo.update_organization(organization_id, data)
            if not updated:
                raise OrganizationNotFoundError()
            return updated

        return organization

    async def delete_organization(self, organization_id:UUID):
        deleted = await self.repo.delete_organization(organization_id)
        if not deleted:
            raise OrganizationNotFoundError()
        return {"message": "Organization deleted successfully"}