from abc import ABC, abstractmethod
from typing import List, Optional

from app.db.models.membership_model import Membership


class MembershipInterface(ABC):
    # Récupérer tous les mandats
    @abstractmethod
    async def get_all_memberships(self)->Optional[List[Membership]]:...
    # Récupérer un mandat spécifique
    @abstractmethod
    async def get_membership_by_id(self)->Optional[Membership]:...