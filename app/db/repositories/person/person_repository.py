from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.person import Person
from app.db.repositories.person.person_interface import PersonInterface


class PersonRepository(PersonInterface):
    def __init__(self, db:AsyncSession):
        # On garde une référence à la session db
        # Cette session permettra d'exécuter les requêtes
        self.db = db

    async def get_person_by_email(self, email: str):
        # Construction de la requête
        stmt = select(Person).where(Person.email == email)

        # execute est async, donc il faut await
        result = await self.db.execute(stmt)

        # scalar_one_or_none renvoie l'objet Person ou None si aucune ligne
        return result.scalar_one_or_none()

    async def create(self, person:Person):
        # On ajoute l'objet dans la session
        self.db.add(person)

        # On écrit dans la db
        await self.db.commit()

        # refresh recharge l'objet dans la db
        await self.db.refresh(person)

        return person