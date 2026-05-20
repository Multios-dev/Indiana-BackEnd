from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.models.user_model import User
from app.db.models.contact_model import Contact
from app.db.repositories.auth.auth_interface import AuthInterface

class AuthRepository(AuthInterface):
    def __init__(self, db:AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        if not email:
            return None

        stmt = (
            select(User)
            .join(User.contact)
            .where(Contact.email == email)
            .options(selectinload(User.contact))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
