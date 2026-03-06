from datetime import date

from typing import Optional

from app.db.models.user_model import User
from app.db.repositories.person.user_repository import PersonRepository
from app.schemas.dtos.input.user_input import UserRegisterInput

"""
Service d'authentification

Son rôle est de :
- Appliquer les règles métiers liées à l'inscription et la connexion
- Créer les objets ORM et demander au repo de persister
"""
class AuthService:
    # Injection du repository
    def __init__(self, repo:PersonRepository):
        self.repo = repo

    """
    Enregistre une personne en DB (Inscription)

    L'API reçoit un DTO (Pydantic) permettant de valider le format
    Le service applique les règles métier (par ex, email unique)
    Le repo fait l'écriture en DB
    """
    async def register(
            self,
            first_names:list[str],
            last_name:str,
            birth_date:date,
            gender:str,
            nationality:str,
            street:str,
            zip_code:str,
            city:str,
            email:str,
            phone:str,
            password: Optional[str] = None
    ) -> Person:

        # Vérifier que l'email soit unique
        existing = await self.repo.get_person_by_email(email)
        if existing:
            # Pour l'instant, on relève une erreur simple
            # Plus tard, l'API convertira ça en HTTP 409
            raise ValueError("Email already exists")

        # Création de l'objet SQLAlchemy (Person) car SQLAlchemy persiste des modèles ORM, pas des DTO
        person = Person(
            firstNames = first_names,
            lastName = last_name,
            birthDate = birth_date,
            gender = gender,
            nationality = nationality,
            street = street,
            zip = zip_code,
            city = city,
            email = email,
            phone = phone,

            # Temporaire : pas de hash, on stocke le mdp tel quel
            password_hash = password
        )

        # Ajout à la DB via le repo
        created = await self.repo.create(person)

        # Retourner l'objet créé
        return created

    # Connexion
    async def login(
            self,
            email:str,
            password:str
    ) -> Person:
        # Chercher la personne
        person = await self.repo.get_person_by_email(email)
        if not person:
            raise ValueError("Invalid credentials")

        # Si le mdp n'est pas défini, le compte n'est pas activé ou l'invitation n'est pas complétée
        if not person.password_hash:
            raise ValueError("Password not activated")

        # Pas de hash pour l'instant, comparaison directe
        if password != person.password_hash:
            raise ValueError("Passwords do not match")

        return person