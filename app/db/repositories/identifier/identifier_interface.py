from abc import ABC, abstractmethod
from uuid import UUID
from app.db.models.identifier_model import Identifier


class IdentifierInterface(ABC):
    @abstractmethod
    async def create_identifier(
        self,
        entity_type: str,
        entity_id: UUID,
        creator: str,
        notation: str,
    ) -> Identifier: ...

    @abstractmethod
    async def get_identifiers_for_entity(
        self,
        entity_type: str,
        entity_id: UUID,
    ) -> list[Identifier]: ...
