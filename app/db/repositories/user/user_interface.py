from abc import ABC, abstractmethod
from typing import List
from app.db.models.user_model import User
from uuid import UUID

class UserInterface(ABC):
    # Créer une personne (lors de l'inscription, par ex)
    @abstractmethod
    async def create_user(self, person: User) -> User: ...
    # Récupérer tous les utilisateurs (avec ou sans filtres)
    @abstractmethod
    async def get_users(self, filters:dict | None = None) -> List[User]: ...
    # Récupérer un utilisateur par son id
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> User | None: ...
    # Modifier/Mettre à jour un utilisateur
    @abstractmethod
    async def update_user(self, user_id:UUID, data:dict) -> User: ...
    # Supprimer un utilisateur
    async def delete_user(self, user_id:int) -> bool: ...