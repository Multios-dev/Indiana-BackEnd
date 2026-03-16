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
            first_names:list[str],
            last_name: str,
            birth_date: date,
            gender: str,
            nationality: str,
            street: str,
            zip_code: str,
            city: str,
            email: str,
            phone: str,
            password:str | None = None
    )-> User:
        # Vérifier que l'email soit unique
        existing = await self.repo.get_user_by_email(email)
        if existing:
            # Pour l'instant, on relève une erreur simple
            # Plus tard, l'API convertira ça en HTTP 409
            raise ValueError("Email already exists")

        # Création de l'objet SQLAlchemy (Person) car SQLAlchemy persiste des modèles ORM, pas des DTO
        person = User(
            firstNames = first_names,
            lastName = last_name,
            birthDate = birth_date,
            gender = gender,
            nationality = nationality,
            street = street,
            zip = zip_code,
            city = city,
            email = email,
            phone = phone,

            # Temporaire : pas de hash, on stocke le mdp tel quel
            password_hash = password
        )

        # Ajout à la DB via le repo
        created = await self.repo.create_user(person)

        # Retourner l'objet créé
        return created