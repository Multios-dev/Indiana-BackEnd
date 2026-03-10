from abc import ABC, abstractmethod
from typing import Optional, List

from app.db.models.user_model import User


class UserInterface(ABC):
    # Récupérer une personne par son email
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[User]: ...
    # Créer une personne (lors de l'inscription, par ex)
    @abstractmethod
    async def create_user(self, person: User) -> User: ...
    # Récupérer tous les utilisateurs
    @abstractmethod
    async def get_users(self) -> List[User]: ...
    # Récupérer un utilisateur par son id
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]: ...
    # Modifier/Mettre à jour un utilisateur
    @abstractmethod
    async def update_user(self, id_user:int, data:dict) -> Optional[User]: ...
    # Supprimer un utilisateur
    async def delete_user(self, id_user:int) -> Optional[User]: ...