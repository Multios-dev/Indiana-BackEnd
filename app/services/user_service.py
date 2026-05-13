from fastapi import Depends, BackgroundTasks
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.repositories.address.address_repository import AddressRepository
from app.db.repositories.user.user_repository import UserRepository
from app.db.repositories.contact.contact_repository import ContactRepository
from app.db.repositories.guardian.guardian_repository import GuardianRepository
from app.db.session import get_db
from app.db.models.user_model import User
from app.db.models.contact_model import Contact
from app.core.exceptions import (
    UserNotFoundError,
    EmptyUpdatePayloadError,
    DatabaseError, NotAllowedGuardianError, MaxGuardiansReachedError, RelationshipAlreadyExistsError
)
from app.mappers.user_mapper import UserMapper
from app.schemas.dtos.input.user_input import UserCreateInput, UserUpdateInput
from uuid import UUID
import traceback
from app.services.email_service import EmailService, get_email_service

def get_user_service(
        db: AsyncSession = Depends(get_db),
        email_service: EmailService = Depends(get_email_service)
):
    repo = UserRepository(db)
    contact_repo = ContactRepository(db)
    address_repo = AddressRepository(db)
    guardian_repo = GuardianRepository(db)
    return UserService(repo, contact_repo, address_repo, guardian_repo, email_service)

class UserService:
    def __init__(
            self,
            repo:UserRepository,
            contact_repo:ContactRepository,
            address_repo:AddressRepository,
            guardian_repo:GuardianRepository,
            email_service:EmailService
    ):
        # Repository injection
        self.repo = repo
        self.contact_repo = contact_repo
        self.address_repo = address_repo
        self.guardian_repo = guardian_repo
        self.email_service = email_service

    async def get_users(self, skip:int, limit:int, filters:dict | None = None):
        users = await self.repo.get_users(skip, limit, filters)
        if not users:
            raise UserNotFoundError()
        return users

    async def get_user_by_id(self, user_id:UUID):
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user

    async def update_user(self, user_id: UUID, payload: UserUpdateInput):
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError()

        data = payload.model_dump(exclude_unset=True)
        if not data:
            raise EmptyUpdatePayloadError()

        # Handle contact separately
        contact_data = data.pop("contact", None)
        if contact_data:
            if user.contact:
                # Update the existing contact
                await self.contact_repo.update_contact(user.contact.id, contact_data)
            else:
                # Create a new contact
                contact = Contact(
                    email=contact_data.get("email"),
                    phone=contact_data.get("phone"),
                    user_id=user_id,
                )
                await self.contact_repo.create_contact(contact)

        home_address_data = data.pop("home_address", None)
        if home_address_data is not None:
            new_address = UserMapper.to_address_entity(payload.home_address)
            created = await self.address_repo.create_address(new_address)
            data["home_address_id"] = created.id

        residential_address_data = data.pop("residential_address", None)
        if residential_address_data is not None:
            new_address = UserMapper.to_address_entity(payload.residential_address)
            created = await self.address_repo.create_address(new_address)
            data["residential_address_id"] = created.id

        # Update the user's fields
        if data:
            updated = await self.repo.update_user(user_id, data)
            if not updated:
                raise UserNotFoundError()
            return updated

        return user

    async def delete_user(self, user_id:UUID):
        deleted = await self.repo.delete_user(user_id)
        if not deleted:
            raise UserNotFoundError()
        return {"message": "User deleted successfully"}

    async def create_user(
            self,
            payload: UserCreateInput,
            background_tasks: BackgroundTasks,
    ) -> User:

        home_address = (
            UserMapper.to_address_entity(payload.home_address)
            if payload.home_address
            else None
        )

        residential_address = (
            UserMapper.to_address_entity(payload.residential_address)
            if payload.residential_address
            else None
        )

        user_entity = UserMapper.to_user_entity(payload)

        try:
            if home_address:
                created_home = await self.address_repo.create_address(home_address)
                user_entity.home_address_id = created_home.id

            if residential_address:
                created_residential = await self.address_repo.create_address(residential_address)
                user_entity.residential_address_id = created_residential.id

            created_user = await self.repo.create_user(user_entity)

            contact = UserMapper.to_contact_entity(payload, created_user.id)

            if contact:
                await self.contact_repo.create_contact(contact)

            full_user = await self.repo.get_user_by_id(created_user.id)

        except SQLAlchemyError as e:
            raise DatabaseError() from e

        email = payload.contact.email if payload.contact and payload.contact.email else None

        if email:
            background_tasks.add_task(
                self.email_service.send_registration_email,
                to=email,
                last_name=created_user.last_name,
                first_name=created_user.first_names[0],
            )

        return full_user

    async def add_guardian(self, guardian_id: UUID, minor_id: UUID):
        existing = await self.guardian_repo.get_relationship(guardian_id, minor_id)
        if existing:
            raise RelationshipAlreadyExistsError()
        # check guardian validity
        guardian = await self.repo.get_user_by_id(guardian_id)

        if not guardian.is_legal_guardian:
            raise NotAllowedGuardianError()

        # check max 2 guardians
        guardians = await self.guardian_repo.get_guardians_by_minor(minor_id)

        if len(guardians) >= 2:
            raise MaxGuardiansReachedError()

        return await self.guardian_repo.add_guardian_relationship(
            guardian_id, minor_id
        )

    async def get_minors(self, guardian_id: UUID):
        return await self.guardian_repo.get_minors_by_guardian(guardian_id)

    async def get_guardians(self, minor_id:UUID):
        return await self.guardian_repo.get_guardians_by_minor(minor_id)