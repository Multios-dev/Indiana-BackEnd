from app.db.models.organization_model import Organization
from app.db.repositories.organization.organization_interface import OrganizationInterface
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from uuid import UUID

class OrganizationRepository(OrganizationInterface):
    ALLOWED_FILTERS = { "name", "acronym", "parent_id", "purpose", "org_type", "sgp_type", "billable", "is_legal_entity" }
    TYPE_MAP = {
        "name":str,
        "acronym":str,
        "parent_id": UUID,
        "purpose":str,
        "org_type": str,
        "sgp_type": str,
        "billable":bool,
        "is_legal_entity":bool
    }

    def __init__(self, db:AsyncSession):
        # Keep a reference to the db session
        # This session will be used to execute queries
        self.db = db

    async def get_all_organizations(self, skip:int, limit:int, filters:dict | None = None):
        stmt = (select(Organization)
                .options(
                    selectinload(Organization.contact),
                    selectinload(Organization.address)
                    )
                )
        conditions=[]

        if filters:
            for key, value in filters.items():
                if key not in self.ALLOWED_FILTERS or not hasattr(Organization, key):
                    continue
                try:
                    casted = self.TYPE_MAP[key](value)
                    conditions.append(getattr(Organization, key) == casted)
                except (ValueError, TypeError):
                    continue

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_organization_by_id(self, org_id:UUID):
        stmt = (select(Organization)
                .where(Organization.id == org_id)
                .options(
                    selectinload(Organization.contact),
                    selectinload(Organization.address)
                    )
                )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create_organization(self, organization: Organization):
        self.db.add(organization)
        await self.db.commit()
        await self.db.refresh(organization)

        stmt = (select(Organization)
                .where(Organization.id == organization.id)
                .options(
                    selectinload(Organization.contact),
                    selectinload(Organization.address)
                    )
                )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def update_organization(self, organization_id: UUID, data: dict):
        try:
            stmt = (select(Organization)
            .where(Organization.id == organization_id)
            .options(
                selectinload(Organization.contact),
                selectinload(Organization.address)
            )
            )
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

    async def delete_organization(self, organization_id:UUID):
        try:
            stmt = (select(Organization)
            .where(Organization.id == organization_id)
            .options(
                selectinload(Organization.contact),
                selectinload(Organization.address)
            )
            )
            result = await self.db.execute(stmt)
            organization_found = result.scalar_one_or_none()

            if not organization_found:
                return None

            await self.db.delete(organization_found)
            await self.db.commit()
            return True
        except Exception:
            await self.db.rollback()
            raise