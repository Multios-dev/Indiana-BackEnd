from psycopg2.extensions import JSON
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.db.models.user_model import User
from app.db.models.address_model import Address
from app.db.models.contact_model import Contact
from app.db.repositories.user.user_interface import UserInterface
from uuid import UUID
from datetime import date

class UserRepository(UserInterface):
    ALLOWED_FILTERS = { "first_names", "last_name", "birth_date", "gender", "nationality", "totem", "quali", "is_legal_guardian" }
    TYPE_MAP = {
        "first_names": JSON,
        "last_name": str,
        "birth_date": date,
        "gender": str,
        "nationality": JSON,
        "totem": str,
        "quali": str,
        "is_legal_guardian": bool,
    }

    def __init__(self, db:AsyncSession):
        # Keep a reference to the db session
        # This session will be used to execute queries
        self.db = db

    async def create_user(
            self,
            person: User,
            home_address: Address,
            residential_address: Address | None = None,
            contact: Contact | None = None,
    ) -> User:
        if home_address:
            self.db.add(home_address)
            await self.db.flush()  # generate home address id
            person.home_address_id = home_address.id

        if residential_address:
            self.db.add(residential_address)
            await self.db.flush()  # generate residential address id
            person.residential_address_id = residential_address.id

        self.db.add(person)
        await self.db.flush()  # generate person id before assigning to contact

        if contact:
            contact.user_id = person.id
            self.db.add(contact)

        await self.db.commit()  # single commit — rollback everything if any step fails

        stmt = (
            select(User)
            .where(User.id == person.id)
            .options(
                selectinload(User.contact),
                selectinload(User.home_address),
                selectinload(User.residential_address)
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_users(self, skip: int, limit: int, filters: dict | None = None) -> list[User]:
        stmt = select(User).options(
            selectinload(User.contact),
            selectinload(User.home_address),
            selectinload(User.residential_address)
        )

        # Store all SQL filter conditions
        conditions = []

        # Only allow filtering on safe and expected fields
        if filters:

            # Iterate through all provided filters
            for key, value in filters.items():

                # Ignore unknown or unauthorized fields
                if key not in self.ALLOWED_FILTERS or not hasattr(User, key):
                    continue
                try:
                    # Cast the value to the expected Python type
                    casted = self.TYPE_MAP[key](value)
                    # Add the SQL condition
                    conditions.append(getattr(User, key) == casted)
                except (ValueError, TypeError):
                    # Ignore invalid filter values
                    continue

        # Apply all conditions using SQL AND
        if conditions:
            stmt = stmt.where(and_(*conditions))

        # Apply pagination
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)

        # scalars() retrieves only Organization objects
        # all converts the result to a Python list
        return result.scalars().all()

    async def get_user_by_id(self, user_id:UUID):
        stmt = (select(User)
                .where(User.id == user_id)
                .options(
            selectinload(User.contact),
                    selectinload(User.home_address),
                    selectinload(User.residential_address)
                )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def update_user(self, user_id:UUID, data:dict):
        stmt = (select(User)
                .where(User.id == user_id)
                .options(
            selectinload(User.contact),
                    selectinload(User.home_address),
                    selectinload(User.residential_address)
                )
        )
        result = await self.db.execute(stmt)
        user_found = result.scalar_one_or_none()

        if not user_found:
            return None

        # Update the fields
        for key, value in data.items():
            if hasattr(user_found, key):        # Skip non-existent fields
                setattr(user_found, key, value)

        # Save
        await self.db.commit()
        await self.db.refresh(user_found)
        return user_found

    async def delete_user(self, user_id:UUID):
        stmt = (select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.contact),
            selectinload(User.home_address),
            selectinload(User.residential_address)
        )
        )
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        await self.db.delete(user)
        await self.db.commit()
        return True
