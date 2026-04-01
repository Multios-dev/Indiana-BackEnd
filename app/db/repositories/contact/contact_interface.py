from abc import ABC, abstractmethod
from uuid import UUID
from app.db.models.contact_model import Contact

class ContactInterface(ABC):
    @abstractmethod
    async def create_contact(self, contact: Contact) -> Contact: ...
    @abstractmethod
    async def update_contact(self, contact_id:UUID, data: dict) -> Contact | None: ...
    @abstractmethod
    async def delete_contact(self, contact_id:UUID) -> Contact | None: ...