from abc import ABC, abstractmethod
from typing import Optional, List
from app.db.models.organization_model import Organization


class OrganizationInterface(ABC):
    # Récupérer toutes les organisations
    @abstractmethod
    async def get_all_organizations(self)->Optional[List[Organization]]:...

    @abstractmethod
    async def get_organization_by_id(self, id:int)->Optional[Organization]:...