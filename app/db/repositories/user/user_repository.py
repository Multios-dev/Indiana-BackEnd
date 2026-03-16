from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.db.models.user_model import User
from app.db.repositories.user.user_interface import UserInterface

class UserRepository(UserInterface):
    def __init__(self, db:AsyncSession):
        # On garde une référence à la session db
        # Cette session permettra d'exécuter les requêtes
        self.db = db

    # Créer un utilisateur / Ajouter un utilisateur à la db
    async def create_user(self, person:User):
        # On ajoute l'objet dans la session
        self.db.add(person)

        # On écrit dans la db
        await self.db.commit()

        # refresh recharge l'objet dans la db
        await self.db.refresh(person)

        return person

    # Récupérer tous les utilisateurs, avec ou sans filtres
    async def get_users(self, filters: dict | None = None) -> list[User]:
        stmt = select(User)

        # Initialiser une liste vide
        conditions = []

        # Liste des champs autorisés pour le filtrage
        # Ca permet d'éviter que l'utilisateur puisse filtrer sur n'importe quelle coloonne
        # ou sur un champ sensible (par ex, l'id)
        if filters:
            allowed_filters = {
                "first_names",
                "last_name",
                "birth_date",
                "gender",
                "totem",
                "quali",
                "is_legal_guardian",
            }

            # Parcours de tous les filtres envoyés dans la requête
            for key, value in filters.items():

                # Vérifie que le filtre est autorisé
                # et que l'attribut existe réellement dans le modèle SQL
                if key in allowed_filters and hasattr(User, key):

                    # Construction dynamique d'une condition SQL
                    # ex : Organization.city == "Mons"
                    conditions.append(getattr(User, key) == value)

        # Si au moins un condition existe
        if conditions:
            # Application des conditions dans la requête SQL
            # and_ permet de combiner plusieurs filtres
            stmt = stmt.where(and_(*conditions))

        result = await self.db.execute(stmt)

        # scalars() récupère uniquement les objets Organization
        # all transforme le résultat en liste Python
        return result.scalars().all()

    # Récupérer un utilisateur spécifique
    async def get_user_by_id(self, user_id:int):
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    # Modifier les données d'un utilisateur
    async def update_user(self, user_id:int, data:dict):
        stmt = select(User).where(User.id == user_id)
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
    async def delete_user(self, user_id:int):
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            return None

        await self.db.delete(user)
        await self.db.commit()
        return user