from abc import abstractmethod, ABC
from uuid import UUID

from app.db.models.participation_model import Participation

class ParticipationInterface(ABC):
    @abstractmethod
    async def get_participation(self, user_id:UUID, event_id:UUID) -> Participation:...
    @abstractmethod
    async def invite_to_event(self, participation:Participation)->bool:...