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