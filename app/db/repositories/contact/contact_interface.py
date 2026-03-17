from abc import ABC, abstractmethod
from app.db.models.contact_model import Contact


class ContactInterface(ABC):
    @abstractmethod
    async def create_contact(self, contact: Contact) -> Contact: ...
    @abstractmethod
    async def update_contact(self, contact_id: int, data: dict) -> Contact | None: ...
    @abstractmethod
    async def delete_contact(self, contact_id: int) -> Contact | None: ...