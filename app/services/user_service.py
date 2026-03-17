from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db
from app.db.repositories.user.user_repository import UserRepository
from app.db.repositories.contact.contact_repository import ContactRepository
from app.db.session import get_db

from app.db.models.user_model import User
from app.db.models.contact_model import Contact

from datetime import date

from app.core.exceptions import (
    UserNotFoundError,
    EmptyUpdatePayloadError,
    DatabaseError
)
from app.schemas.dtos.input.user_input import UserCreateInput, UserUpdateInput


def get_user_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    contact_repo = ContactRepository(db)
    return UserService(repo, contact_repo)

class UserService:
    def __init__(self, repo:UserRepository, contact_repo:ContactRepository):
        # Injection du repository
        self.repo = repo
        self.contact_repo = contact_repo

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

    async def update_user(self, user_id: int, payload: UserUpdateInput):
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise EmptyUpdatePayloadError()

        # Gérer le contact séparément
        contact_data = data.pop("contact", None)

        if contact_data:
            if user.contact:
                # Modifier le contact existant
                await self.contact_repo.update_contact(user.contact.id, contact_data)
            else:
                # Créer un nouveau contact
                contact = Contact(
                    email=contact_data.get("email"),
                    phone=contact_data.get("phone"),
                    user_id=user_id,
                )
                await self.contact_repo.create_contact(contact)

        # Mettre à jour les champs du user
        if data:
            updated = await self.repo.update_user(user_id, data)
            if not updated:
                raise UserNotFoundError()
            return updated

        return user

    async def delete_user(self, user_id: int):
        deleted = await self.repo.delete_user(user_id)
        if not deleted:
            raise UserNotFoundError()
        return deleted

    # Créer un utilisateur
    async def create_user(self, payload: UserCreateInput) -> User:
        try:
            person = User(
                first_names=payload.first_names,
                last_name=payload.last_name,
                birth_date=payload.birth_date,
                gender=payload.gender,
                totem=payload.totem,
                quali=payload.quali,
                is_legal_guardian=payload.is_legal_guardian,
            )
            created = await self.repo.create_user(person)

            # Créer le contact si fourni
            if payload.contact:
                contact = Contact(
                    email=payload.contact.email,
                    phone=payload.contact.phone,
                    user_id=created.id,
                )
                await self.contact_repo.create_contact(contact)

            # Recharger le user avec ses relations
            created = await self.repo.get_user_by_id(created.id)

            return created
        except Exception:
            raise DatabaseError()