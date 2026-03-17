from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.contact_model import Contact
from app.db.repositories.contact.contact_interface import ContactInterface


class ContactRepository(ContactInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_contact(self, contact: Contact) -> Contact:
        self.db.add(contact)
        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def update_contact(self, contact_id: int, data: dict) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id)
        result = await self.db.execute(stmt)
        contact = result.scalar_one_or_none()

        if not contact:
            return None

        for key, value in data.items():
            if hasattr(contact, key):
                setattr(contact, key, value)

        await self.db.commit()
        await self.db.refresh(contact)
        return contact

    async def delete_contact(self, contact_id: int) -> Contact | None:
        stmt = select(Contact).where(Contact.id == contact_id)
        result = await self.db.execute(stmt)
        contact = result.scalar_one_or_none()

        if not contact:
            return None

        await self.db.delete(contact)
        await self.db.commit()
        return contact