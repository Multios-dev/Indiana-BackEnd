from abc import ABC, abstractmethod
from typing import Optional

from app.db.models.user_model import User


class PersonInterface(ABC):
    # Récupérer une personne par son email
    @abstractmethod
    async def get_person_by_email(self, email: str) -> Optional[User]: ...

    # Créer une personne (lors de l'inscription, par ex)
    @abstractmethod
    async def create(self, person: User) -> User: ...