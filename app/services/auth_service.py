from app.core.exceptions import UserNotFoundError, PasswordError
from app.db.repositories.auth.auth_repository import AuthRepository
from app.db.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_db
from app.schemas.dtos.input.user_input import UserLoginInput


def get_auth_service(db: AsyncSession = Depends(get_db)):
    repo = AuthRepository(db)
    return AuthService(repo)

class AuthService:
    def __init__(self, repo:AuthRepository):
        self.repo = repo

    async def login(self, payload: UserLoginInput) -> User:
        user = await self.repo.get_user_by_email(payload.email)
        if not user:
            raise UserNotFoundError()

        if payload.password != user.password:
            raise PasswordError()
        return user