from app.core.exceptions import AddressNotFoundError
from app.db.repositories.address.address_repository import AddressRepository
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

def get_address_service(db:AsyncSession = Depends(get_db)):
    address_repo = AddressRepository(db)
    return AddressService(address_repo)

class AddressService:
    def __init__(self, address_repo: AddressRepository):
        self.address_repo = address_repo

    async def get_all_addresses(self, skip:int, limit:int, filters:dict):
        addresses = await self.address_repo.get_all_addresses(skip, limit, filters)
        if not addresses:
            raise AddressNotFoundError()
        return addresses