from abc import ABC, abstractmethod
from typing import Optional, List
from app.db.models.organization_model import Organization


class OrganizationInterface(ABC):
    # Récupérer une organisation par son id
    @abstractmethod
    async def get_all_organizations(self)->Optional[List[Organization]]:...