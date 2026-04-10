from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.db.models.address_model import Address
from app.db.repositories import address
from app.db.repositories.address.address_interface import AddressInterface
from uuid import UUID

class AddressRepository(AddressInterface):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_address(self, address: Address) -> Address:
        self.db.add(address)
        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def update_address(self, address_id:UUID, data:dict) -> Address | None:
        stmt = select(Address).where(Address.id == address_id)
        result = await self.db.execute(stmt)
        address = result.scalar_one_or_none()

        if not address:
            return None

        for key, value in data.items():
            if hasattr(address, key):
                setattr(address, key, value)

        await self.db.commit()
        await self.db.refresh(address)
        return address

    async def delete_address(self, address_id: UUID) -> bool:
        stmt = select(Address).where(Address.id == address_id)
        result = await self.db.execute(stmt)
        address = result.scalar_one_or_none()

        if not address:
            return None

        await self.db.delete(address)
        await self.db.commit()
        return True

    async def get_all_addresses(self, skip:int, limit:int, filters:dict | None = None) -> List[Address]:
        stmt = select(Address)

        conditions = []

        if filters:
            allowed_filters = {"thoroughfare", "box_number", "post_name", "post_code", "country"}
            for key, value in filters.items():
                if key in allowed_filters and hasattr(Address, key):
                    conditions.append(getattr(Address, key) == value)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()