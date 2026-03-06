from fastapi import APIRouter, HTTPException, Depends

from app.schemas.dtos.input.user_input import UserLoginInput, UserRegisterInput
from app.schemas.dtos.output.user_output import UserOutput
from app.services.auth_service import AuthService, get_auth_service

# Toutes les routes commenceront par /auth
router = APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register", summary="Inscrire un utilisateur")
async def register(
        payload:UserRegisterInput,
        service:AuthService = Depends(get_auth_service)
):
    """
    payloard : données envoyées par le client (dto)
    service : service d'authentification injecté
    """
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
async def login(
        payload:UserLoginInput,
        service:AuthService = Depends(get_auth_service)
):
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