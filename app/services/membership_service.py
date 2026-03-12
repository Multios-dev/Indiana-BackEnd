from app.db.models.membership_model import Membership
from app.db.repositories.membership.membership_repository import MembershipRepository

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.dtos.input.membership_input import CreateMembershipInput, UpdateMembershipInput

from datetime import datetime

def get_membership_service(db:AsyncSession = Depends(get_db)):
    repo = MembershipRepository(db)
    return MembershipService(repo)

class MembershipService:
    def __init__(self, repo:MembershipRepository):
        self.repo = repo

    def to_naive_datetime(self, dt: datetime | None) -> datetime | None:
        if dt is None:
            return None

        if dt.tzinfo is not None:
            return dt.replace(tzinfo=None)

        return dt

    # Récupérer les mandats
    async def get_memberships(self, filters:dict | None = None) -> list[Membership]:
        memberships = await self.repo.get_memberships(filters)
        if not memberships:
            raise ValueError("No memberships found")
        return memberships

    # Récupérer un mandat spécifique
    async def get_membership_by_id(self, membership_id:int) -> Membership:
        membership = await self.repo.get_membership_by_id(membership_id)
        if not membership:
            raise ValueError("No membership found")
        return membership

    async def create_membership(self, payload: CreateMembershipInput) -> Membership:
        start_date = self.to_naive_datetime(payload.start_date)
        end_date = self.to_naive_datetime(payload.end_date)

        # Vérifier la cohérence des dates
        if end_date is not None and end_date < start_date:
            raise ValueError("End date cannot be earlier than start date")

        membership = Membership(
            user_id=payload.user_id,
            organization_id=payload.organization_id,
            role=payload.role,
            start_date=payload.start_date,
            end_date=end_date,
            price=payload.price
        )
        return await self.repo.create_membership(membership)

    async def update_membership(self, membership_id:int, payload:UpdateMembershipInput):
        data = payload.model_dump(exclude_unset=True)

        if not data:
            raise ValueError("No data found")

        updated = await self.repo.update_membership(membership_id, data)

        if not updated:
            raise ValueError("No updated membership found")

        return updated