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
        users = await self.repo.get_all()
        if not users:
            raise ValueError("Users not found")
        return users

    # Récupérer un utilisateur spécifique
    async def get_user_by_id(self, user_id):
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    # Modifier les données d'un utilisateur
    async def update_user(self, user_id, data:dict):
        updated_user = await self.repo.update_user(user_id, data)
        if not updated_user:
            raise ValueError("User not found")
        return updated_user

    # Supprimer un utilisateur
    async def delete_user(self, user_id):
        deleted_user = await self.repo.delete_user(user_id)
        if not deleted_user:
            raise ValueError("User not found")
        return deleted_user