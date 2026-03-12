from abc import ABC, abstractmethod
from typing import List, Optional

from app.db.models.membership_model import Membership


class MembershipInterface(ABC):
    # Récupérer tous les mandats
    @abstractmethod
    async def get_memberships(self, filters:dict | None = None)->Optional[List[Membership]]:...
    # Récupérer un mandat spécifique
    @abstractmethod
    async def get_membership_by_id(self, membership_id:int)->Optional[Membership]:...
    # Créer un mandat
    @abstractmethod
    async def create_membership(self, membership:Membership)->Membership:...
    # Modifier un mandat
    @abstractmethod
    async def update_membership(self, membership_id:int)->Membership:...
    # Supprimer un mandat
    async def delete_membership(self, membership_id:int)->None:...