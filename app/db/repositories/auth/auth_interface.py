from abc import ABC, abstractmethod
from app.db.models.user_model import User

class AuthInterface(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str)-> User | None: ...