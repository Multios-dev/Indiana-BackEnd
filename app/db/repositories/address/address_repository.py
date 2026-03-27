from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.address_model import Address

class AddressRepository:
    """
    Repo pour gérer les adresses.
    Encapsule toutes les opérations DB sur Address.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_address(self, address: Address) -> Address:
        """
        Crée une adresse dans la DB et retourne l'entité avec ID.
        """
        self.session.add(address)
        await self.session.commit()
        await self.session.refresh(address)
        return address