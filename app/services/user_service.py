from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.address.address_repository import AddressRepository
from app.db.repositories.user.user_repository import UserRepository
from app.db.repositories.contact.contact_repository import ContactRepository
from app.db.session import get_db

from app.db.models.user_model import User
from app.db.models.contact_model import Contact

from app.core.exceptions import (
    UserNotFoundError,
    EmptyUpdatePayloadError,
    DatabaseError
)
from app.mappers.user_mapper import UserMapper
from app.schemas.dtos.input.user_input import UserCreateInput, UserUpdateInput

import traceback

def get_user_service(db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    contact_repo = ContactRepository(db)
    address_repo = AddressRepository(db)
    return UserService(repo, contact_repo, address_repo)

class UserService:
    def __init__(self, repo:UserRepository, contact_repo:ContactRepository, address_repo:AddressRepository):
        # Injection du repository
        self.repo = repo
        self.contact_repo = contact_repo
        self.address_repo = address_repo

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
        return {"message": "User deleted successfully"}


    async def create_user(self, payload: UserCreateInput) -> User:
        try:
            if payload.home_address:
                home_address = UserMapper.to_address_entity(payload.home_address)
                created_home = await self.address_repo.create_address(home_address)
                home_id = created_home.id
            else:
                home_id = None

            if payload.residential_address:
                residential_address = UserMapper.to_address_entity(payload.residential_address)
                created_residential = await self.address_repo.create_address(residential_address)
                residential_id = created_residential.id
            else:
                residential_id = None

            user_entity = UserMapper.to_user_entity(payload)
            user_entity.home_address_id = home_id
            user_entity.residential_address_id = residential_id
            created_user = await self.repo.create_user(user_entity)

            contact = UserMapper.to_contact_entity(payload, created_user.id)
            if contact:
                await self.contact_repo.create_contact(contact)

            return await self.repo.get_user_by_id(created_user.id)

        except Exception as e:


            print("⚠️ DatabaseError:", e)

            traceback.print_exc()

            raise DatabaseError() from e