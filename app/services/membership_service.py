from app.db.models.membership_model import Membership
from app.db.repositories.membership.membership_repository import MembershipRepository

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.dtos.input.membership_input import CreateMembershipInput


def get_membership_service(db:AsyncSession = Depends(get_db)):
    repo = MembershipRepository(db)
    return MembershipService(repo)

class MembershipService:
    def __init__(self, repo:MembershipRepository):
        self.repo = repo

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

    # Créer un mandat
    async def create_membership(self, payload:CreateMembershipInput):
        user = await self.user_re
        membership = Membership(
            user_id = payload.user_id,
            organization_id = payload.organization_id,
            start_date = payload.start_date,
            end_date = payload.end_date,
            price = payload.price
        )
        return await self.repo.create_membership(membership)
