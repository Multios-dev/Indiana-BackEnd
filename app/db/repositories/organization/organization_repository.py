from app.db.models.organization_model import Organization
from app.db.repositories.organization.organization_interface import OrganizationInterface

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

class OrganizationRepository(OrganizationInterface):
    def __init__(self, db:AsyncSession):
        # On garde une référence à la session db
        # Cette session permettra d'exécuter les requêtes
        self.db = db

    # Récupérer toutes les organisations
    async def get_all_organizations(self, filters:dict | None = None):
        stmt = select(Organization).options(selectinload(Organization.contact))
        conditions=[]

        if filters:
            allowed_filters = {
                "name",
                "acronym",
                "parent_id",
                "purpose",
                "org_type",
                "sgp_type",
                "billable",
                "is_legal_entity",
            }

            for key, value in filters.items():
                if key in allowed_filters and hasattr(Organization, key):
                    conditions.append(getattr(Organization, key) == value)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    # Récupérer une organisation par son id
    async def get_organization_by_id(self, id:int):
        stmt = select(Organization).where(Organization.id == id).options(selectinload(Organization.contact))
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # Créer une organisation
    async def create_organization(self, organization: Organization):
        self.db.add(organization)
        await self.db.commit()
        await self.db.refresh(organization)

        stmt = select(Organization).where(Organization.id == organization.id).options(
            selectinload(Organization.contact))
        result = await self.db.execute(stmt)
        return result.scalar_one()

    # Modifier une organisation
    async def update_organization(self, organization_id: int, data: dict):
        try:
            stmt = select(Organization).where(Organization.id == organization_id)
            result = await self.db.execute(stmt)
            organization_found = result.scalar_one_or_none()

            if not organization_found:
                return None

            for key, value in data.items():
                if key != "id" and hasattr(organization_found, key):
                    setattr(organization_found, key, value)

            await self.db.commit()
            await self.db.refresh(organization_found)
            return organization_found

        except Exception:
            await self.db.rollback()
            raise

    # Supprimer une organisation
    async def delete_organization(self, organization_id: int):
        try:
            stmt = select(Organization).where(Organization.id == organization_id).options(selectinload(Organization.contact))
            result = await self.db.execute(stmt)
            organization_found = result.scalar_one_or_none()

            if not organization_found:
                return None

            await self.db.delete(organization_found)
            await self.db.commit()
            return organization_found
        except Exception:
            await self.db.rollback()
            raise