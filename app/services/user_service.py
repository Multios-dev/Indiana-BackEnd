from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user.user_repository import UserRepository
from app.db.session import get_db


def get_user_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)

class UserService:
    def __init__(self, repo:UserRepository):
        # Injection du repository
        self.repo = repo

    # Récupérer tous les utilisateurs
    async def get_all_users(self):
        existing = await self.repo.get_all()
        if not existing:
            raise ValueError("Users not found")
        return existing

    # Récupérer un utilisateur spécifique
    async def get_user_by_id(self, user_id):
        existing = await self.repo.get_user_by_id(user_id)
        if not existing:
            raise ValueError("User not found")
        return existing

    # Modifier les données d'un utilisateur
    async def update_user(self, user_id, data:dict):
        existing = await self.repo.get_user_by_id(user_id)
        if not existing:
            raise ValueError("User not found")

        existing = await self.repo.update_user(user_id, data)
        return existing