from abc import ABC, abstractmethod
from typing import List
from app.db.models.organization_model import Organization


class OrganizationInterface(ABC):
    # Récupérer toutes les organisations (avec ou sans filtres)
    @abstractmethod
    async def get_all_organizations(self, filters:dict | None = None)->List[Organization] | None:...
    # Récupérer une organisation spécifique
    @abstractmethod
    async def get_organization_by_id(self, id:int)->Organization | None:...
    # Créer une organisation
    @abstractmethod
    async def create_organization(self, organization:Organization)->Organization:...
    # Modifier une organisation
    @abstractmethod
    async def update_organization(self, id_organization:int, data:dict)->Organization:...
    # Supprimer une organisation
    async def delete_organization(self, id_organization:int, data:dict)->None:...