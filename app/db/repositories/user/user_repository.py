from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from app.db.models.user_model import User
from app.db.repositories.user.user_interface import UserInterface
from uuid import UUID

class UserRepository(UserInterface):
    def __init__(self, db:AsyncSession):
        # Keep a reference to the db session
        # This session will be used to execute queries
        self.db = db

    async def create_user(self, person: User):
        self.db.add(person)
        await self.db.commit()
        await self.db.refresh(person)

        stmt = (select(User)
                .where(User.id == person.id)
                .options(
                    selectinload(User.contact),
                    selectinload(User.home_address),
                    selectinload(User.residential_address)
                    )
                )
        result = await self.db.execute(stmt)
        return result.scalar_one()

    async def get_users(self, skip:int, limit:int, filters: dict | None = None) -> list[User]:
        stmt = select(User).options(
    selectinload(User.contact),
            selectinload(User.home_address),
            selectinload(User.residential_address)
        )

        # Initialize empty list
        conditions = []

        # List of allowed filter fields
        # This prevents filtering on arbitrary columns or on sensitives fiels
        if filters:
            allowed_filters = {
                "first_names",
                "last_name",
                "birth_date",
                "gender",
                "nationality",
                "totem",
                "quali",
                "is_legal_guardian",
            }

            # Iterate over all filters sent in the request
            for key, value in filters.items():

                # Check that the filter is allowed
                # and that the attribut actually exists in the SQL model
                if key in allowed_filters and hasattr(User, key):

                    # Dynamically build a SQL condition
                    # e.g. : Organization.city == "Mons"
                    conditions.append(getattr(User, key) == value)

        if conditions:
            # Apply conditions to the SQL query
            # and_ combines multiple filters
            stmt = stmt.where(and_(*conditions))

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
            selectinload(User.residence_address)
        )
        )
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        await self.db.delete(user)
        await self.db.commit()
        return True