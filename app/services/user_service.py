from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user.user_repository import UserRepository
from app.db.session import get_db

from app.db.models.user_model import User

from datetime import date

from app.core.exceptions import (
    UserNotFoundError,
    MembershipNotFoundError,
    OrganizationNotFoundError,
    InvalidDateRangeError,
    EmptyUpdatePayloadError
)

def get_user_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

class UserService:
    def __init__(self, repo:UserRepository):
        # Injection du repository
        self.repo = repo

    # Récupérer tous les utilisateurs
    async def get_users(self, filters:dict | None = None):
        users = await self.repo.get_users(filters)
        if not users:
            raise UserNotFoundError()
        return users

    # Récupérer un utilisateur spécifique
    async def get_user_by_id(self, user_id):
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    # Modifier les données d'un utilisateur
    async def update_user(self, user_id, data:dict):
        updated_user = await self.repo.update_user(user_id, data)
        if not updated_user:
            raise UserNotFoundError()
        return updated_user

    # Supprimer un utilisateur
    async def delete_user(self, user_id):
        deleted_user = await self.repo.delete_user(user_id)
        if not deleted_user:
            UserNotFoundError()
        return deleted_user

    # Créer un utilisateur
    async def create_user(
            self,
            first_names: list[str],
            last_name: str,
            birth_date: date | None = None,
            gender: str | None = None,
            totem: str | None = None,
            quali: str | None = None,
            is_legal_guardian: bool = False,
    ) -> User:
        person = User(
            first_names=first_names,
            last_name=last_name,
            birth_date=birth_date,
            gender=gender,
            totem=totem,
            quali=quali,
            is_legal_guardian=is_legal_guardian,
        )

        return await self.repo.create_user(person)