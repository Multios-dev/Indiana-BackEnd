from app.db.models.address_model import Address
from abc import ABC, abstractmethod
from uuid import UUID
from typing import List

class AddressInterface(ABC):
    @abstractmethod
    async def create_address(self, address: Address) -> Address: ...
    @abstractmethod
    async def update_address(self, address_id:UUID, data:dict) -> Address | None: ...
    @abstractmethod
    async def delete_address(self, address_id:UUID) -> bool: ...
    @abstractmethod
    async def get_all_addresses(self, skip:int, limit:int, filters:dict | None = None) -> List[Address] | None: ...