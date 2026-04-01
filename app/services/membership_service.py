import traceback
from app.db.models.membership_model import Membership
from app.db.repositories.membership.membership_repository import MembershipRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.organization.organization_repository import OrganizationRepository
from app.db.repositories.user.user_repository import UserRepository
from app.db.session import get_db
from app.mappers.membership_mapper import MembershipMapper
from app.schemas.dtos.input.membership_input import CreateMembershipInput, UpdateMembershipInput
from app.core.exceptions import (
    MembershipNotFoundError,
    UserNotFoundError,
    OrganizationNotFoundError,
    InvalidDateRangeError,
    EmptyUpdatePayloadError,
    DatabaseError,
)
from uuid import UUID

def get_membership_service(db: AsyncSession = Depends(get_db)):
    repo = MembershipRepository(db)
    user_repo = UserRepository(db)
    org_repo = OrganizationRepository(db)
    return MembershipService(repo, user_repo, org_repo)

class MembershipService:
    def __init__(
            self,
            repo: MembershipRepository,
            repo_user: UserRepository,
            repo_organization: OrganizationRepository
    ):
        self.repo = repo
        self.repo_user = repo_user
        self.repo_organization = repo_organization

    async def get_memberships(self, filters: dict | None = None) -> list[Membership]:
        memberships = await self.repo.get_memberships(filters)
        if not memberships:
            raise MembershipNotFoundError()
        return memberships

    async def get_membership_by_id(self, membership_id: UUID) -> Membership:
        membership = await self.repo.get_membership_by_id(membership_id)
        if not membership:
            raise MembershipNotFoundError()
        return membership

    async def create_membership(self, payload: CreateMembershipInput) -> Membership:
        user = await self.repo_user.get_user_by_id(payload.user_id)
        if not user:
            raise UserNotFoundError()

        organization = await self.repo_organization.get_organization_by_id(payload.organization_id)
        if not organization:
            raise OrganizationNotFoundError()

        if payload.end_date is not None and payload.end_date < payload.start_date:
            raise InvalidDateRangeError()

        try:
            membership = MembershipMapper.to_membership_entity(payload)
            return await self.repo.create_membership(membership)
        except Exception as e:
            print("DatabaseError : ", e)
            traceback.print_exc()
            raise DatabaseError() from e

    async def update_membership(self, membership_id: int, payload: UpdateMembershipInput):
        membership = await self.repo.get_membership_by_id(membership_id)
        if not membership:
            raise MembershipNotFoundError()

        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise EmptyUpdatePayloadError()

        new_start_date = data.get("start_date", membership.start_date)
        new_end_date = data.get("end_date", membership.end_date)

        if new_end_date and new_end_date < new_start_date:
            raise InvalidDateRangeError()

        updated = await self.repo.update_membership(membership_id, data)
        if not updated:
            raise MembershipNotFoundError()
        return updated

    async def delete_membership(self, membership_id: int):
        deleted = await self.repo.delete_membership(membership_id)
        if not deleted:
            raise MembershipNotFoundError()
        return { "message" : "Membership deleted successfully" }
