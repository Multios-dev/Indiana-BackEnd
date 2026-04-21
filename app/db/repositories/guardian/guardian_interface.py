from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.db.models.user_model import User

class GuardianInterface(ABC):
    @abstractmethod
    async def add_guardian_relationship(self, guardian_id:UUID, minor_id:UUID): ...
    @abstractmethod
    async def get_minors_by_guardian(self, guardian_id:UUID) -> List[User]: ...
    @abstractmethod
    async def get_guardians_by_minor(self, minor_id:UUID) -> List[User]: ...