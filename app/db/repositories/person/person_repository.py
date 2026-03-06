from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.models.person import Person
from app.db.repositories.person.person_interface import PersonInterface


class PersonRepository(PersonInterface):
    def __init__(self, db:AsyncSession):
        # On garde une référence à la session db
        # Cette session permettra d'exécuter les requêtes
        self.db = db

    # Récupérer un utilisateur par son email
    async def get_person_by_email(self, email: str):
        # Construction de la requête
        stmt = select(Person).where(Person.email == email)

        # execute est async, donc il faut await
        result = await self.db.execute(stmt)

        # scalar_one_or_none renvoie l'objet Person ou None si aucune ligne
        return result.scalar_one_or_none()

    # Créer un utilisateur / Ajouter un utilisateur à la db
    async def create(self, person:Person):
        # On ajoute l'objet dans la session
        self.db.add(person)

        # On écrit dans la db
        await self.db.commit()

        # refresh recharge l'objet dans la db
        await self.db.refresh(person)

        return person

    # Récupérer tous les utilisateurs
    async def get_all(self):
        stmt = select(Person)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    # Récupérer un utilisateur spécifique
    async def get_user_by_id(self, id_user:int):
        stmt = select(Person).where(Person.id == id_user)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # Modifier les données d'un utilisateur
    async def update_user(self, id_user:int, data:dict):
        stmt = select(Person).where(Person.id == id_user)
        result = await self.db.execute(stmt)
        user_found = result.scalar_one_or_none()

        if not user_found:
            return None

        # Modifier les champs
        for key, value in data.items():
            if hasattr(user_found, key): # Eviter les champs inexistants
                setattr(user_found, key, value)

        # Sauvegarder
        await self.db.commit()
        await self.db.refresh(user_found)
        return user_found

    # Supprimer un utilisateur
    async def delete_user(self, id_user:int):
        stmt = select(Person).where(Person.id == id_user)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        await self.db.delete(user)
        await self.db.commit()
        return user

    # Récupérer les membres filtrés
    async def get_users_filtered(self, filters:dict):
        stmt = select(Person)

        if filters:
            conditions=[]
            for key, value in filters.items():
                if hasattr(Person, key):    # Vérifie que le champ existe dans le modèle
                    conditions.append(getattr(Person, key) == value)
            if conditions:
                stmt = stmt.where(and_(*conditions)) # Combien tous les filtres

        result = await self.db.execute(stmt)
        return result.scalars.all()