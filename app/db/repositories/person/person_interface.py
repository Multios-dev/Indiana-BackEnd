from abc import ABC, abstractmethod
from typing import Optional

from app.db.models.person import Person


class PersonInterface(ABC):
    # Récupérer une personne par son email
    @abstractmethod
    async def get_person_by_email(self, email: str) -> Optional[Person]: ...

    # Créer une personne (lors de l'inscription, par ex)
    @abstractmethod
    async def create(self, person: Person) -> Person: ...