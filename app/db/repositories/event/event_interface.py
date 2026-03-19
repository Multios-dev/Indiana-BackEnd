from abc import ABC, abstractmethod
from typing import List
from app.db.models.event_model import Event

class EventInterface(ABC):
    # Récupérer tous les événements
    @abstractmethod
    async def get_all_events(self, filters:dict | None = None) -> List[Event] | None:...
    # Récupérer un événement spécifique
    @abstractmethod
    async def get_event_by_id(self, event_id: int) -> Event | None:...
    # Créer un événement
    @abstractmethod
    async def create_event(self, event: Event) -> Event:...
    # Modifier un événement
    async def update_event(self, event_id:int, data:dict) -> Event:...
    # Supprimer un événement
    async def delete_event(self, event_id:int) -> None:...