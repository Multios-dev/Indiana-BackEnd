from app.core.exceptions import UserNotFoundError, PasswordError
from app.db.repositories.auth.auth_repository import AuthRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_db
from app.schemas.dtos.input.user_input import UserLoginInput
from app.schemas.dtos.output.user_output import UserLoginOutput


def get_auth_service(db: AsyncSession = Depends(get_db)):
    repo = AuthRepository(db)
    return AuthService(repo)

class AuthService:
    def __init__(self, repo:AuthRepository):
        self.repo = repo

    async def login(self, payload: UserLoginInput) -> UserLoginOutput:
        user = await self.repo.get_user_by_email(payload.email)
        if not user:
            raise UserNotFoundError()

        if payload.password != user.password:
            raise PasswordError()

        if not user.contact or not user.contact.email:
            raise UserNotFoundError()

        return UserLoginOutput(
            id=user.id,
            email=user.contact.email,
        )
