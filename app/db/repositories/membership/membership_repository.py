from sqlalchemy.exc import SQLAlchemyError

from app.db.models.membership_model import Membership
from app.db.repositories.membership.membership_interface import MembershipInterface

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

class MembershipRepository(MembershipInterface):
    def __init__(self, db:AsyncSession):
        # On garde une référence à la session db
        # Cette session permettra d'exécuter les requêtes
        self.db = db

    async def get_memberships(self, filters:dict | None = None):
        stmt = select(Membership)
        conditions = []

        if filters:
            allowed_filters = {
                "user_id",
                "organization_id",
                "role",
                "start_date",
                "end_date"
            }

            for key, value in filters.items():
                if key in allowed_filters and hasattr(Membership, key):
                    conditions.append(getattr(Membership, key) == value)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    # Récupérer un mandat spécifique
    async def get_membership_by_id(self, membership_id:int):
        stmt = select(Membership).where(Membership.id == membership_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # Créer un mandat
    async def create_membership(self, membership: Membership) -> Membership:
        try:
            self.db.add(membership)
            await self.db.commit()
            await self.db.refresh(membership)
            return membership
        except SQLAlchemyError as e:
            await self.db.rollback()
            print("DB ERROR:", e)
            raise

    # Modifier un mandat
    async def update_membership(self, membership_id:int, data:dict):
        try:
            stmt = select(Membership).where(Membership.id == membership_id)
            result = await self.db.execute(stmt)
            membership_found = result.scalar_one_or_none()

            if not membership_found:
                return None

            for key, value in data.items():
                if key != "id" and hasattr(membership_found, key):
                    setattr(membership_found, key, value)

            await self.db.commit()
            await self.db.refresh(membership_found)
            return membership_found

        except Exception:
            await self.db.rollback()
            raise

    # Supprimer un mandat
    async def delete_membership(self, membership_id:int)->None:
        try:
            stmt = select(Membership).where(Membership.id == membership_id)
            result = await self.db.execute(stmt)
            membership_found = result.scalar_one_or_none()

            if not membership_found:
                return None

            await self.db.delete(membership_found)
            await self.db.commit()
            return membership_found
        except Exception:
            await self.db.rollback()
            raise