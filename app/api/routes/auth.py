from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user.user_repository import UserRepository
from app.db.session import get_db

from app.schemas.dtos.input.user_input import UserLoginInput, UserRegisterInput
from app.schemas.dtos.output.user_output import UserOutput
from app.services.auth_service import AuthService

# Toutes les routes commenceront par /auth
router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register", summary="Inscrire un utilisateur")
async def register(payload:UserRegisterInput, db:AsyncSession = Depends(get_db)):
    """
    payloard : données envoyées par le client (dto)
    db : session de base de données fournie par FastAPI
    """

    # Création du repository avec la session DB
    repo = UserRepository(db)

    # Création du service métier
    service = AuthService(repo)

    try:
        person = await service.register(
            first_names = payload.firstNames,
            last_name = payload.lastName,
            birth_date = payload.birthDate,
            gender = payload.gender,
            nationality = payload.nationality,
            street = payload.street,
            zip_code = payload.zip,
            city = payload.city,
            email = payload.email,
            phone = payload.phone
        )

        return UserOutput(
            id=person.id,
            email=person.email
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", summary="Connecter un utilisateur")
async def login(payload:UserLoginInput, db:AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    service = AuthService(repo)

    try:
        person = await service.login(
            email = payload.email,
            password = payload.password
        )

        return UserOutput(
            id = person.id,
            email = person.email
        )

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))