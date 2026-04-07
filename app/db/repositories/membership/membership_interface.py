from abc import ABC, abstractmethod
from typing import List
from app.db.models.membership_model import Membership
from uuid import UUID

class MembershipInterface(ABC):
    # Récupérer tous les mandats
    @abstractmethod
    async def get_memberships(self, skip:int, limit:int, filters:dict | None = None)->List[Membership] | None:...
    # Récupérer un mandat spécifique
    @abstractmethod
    async def get_membership_by_id(self, membership_id:UUID)->Membership | None:...
    # Créer un mandat
    @abstractmethod
    async def create_membership(self, membership:Membership)->Membership:...
    # Modifier un mandat
    @abstractmethod
    async def update_membership(self, membership_id:UUID, data:dict)->Membership:...
    # Supprimer un mandat
    @abstractmethod
    async def delete_membership(self, membership_id:UUID)->bool:...