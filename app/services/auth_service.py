from app.core.exceptions import UserNotFoundError, PasswordError
from app.db.repositories.auth.auth_repository import AuthRepository
from app.db.models.user_model import User

class AuthService:
    def __init__(self, repo:AuthRepository):
        self.repo = repo

    async def login(self, email: str, password: str) -> User:
        user = await self.repo.get_user_by_email(email)
        if not user:
            raise UserNotFoundError()

        if password != user.password:
            raise PasswordError()

        return user