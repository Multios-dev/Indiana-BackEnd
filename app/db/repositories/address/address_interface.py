from app.db.models.address_model import Address
from abc import ABC, abstractmethod
from uuid import UUID

class AddressInterface(ABC):
    @abstractmethod
    async def create_address(self, address: Address) -> Address: ...
    @abstractmethod
    async def update_address(self, addres_id:UUID, data:dict) -> Address | None: ...
    @abstractmethod
    async def delete_address(self, address_id:UUID) -> bool: ...