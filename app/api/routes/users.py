from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user.user_repository import UserRepository
from app.db.session import get_db
from app.schemas.dtos.output.get_user_output import GetUserOutput
from app.services.user_service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", summary="Récupérer tous les utilisateurs")
async def get_users(service:UserService=Depends(get_user_service)):

    try:
        users = await service.get_all_users()

        # Retourne tous les utilisateurs sous forme de liste
        return [
            GetUserOutput(
                id=user.id,
                firstNames=user.firstNames,
                lastName=user.lastName,
                birthDate=user.birthDate,
                gender=user.gender,
                nationality=user.nationality,
                street=user.street,
                zip=user.zip,
                city=user.city,
                email=user.email,
                phone=user.phone
            )
            for user in users
        ]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{user_id}", summary="Récupérer un utilisateur spécifique")
async def get_user(
        user_id:int,
        service:UserService=Depends(get_user_service)
):

    try:
        user = await service.get_user_by_id(user_id)

        return GetUserOutput(
            id=user.id,
            firstNames=user.firstNames,
            lastName=user.lastName,
            birthDate=user.birthDate,
            gender=user.gender,
            nationality=user.nationality,
            street=user.street,
            zip=user.zip,
            city=user.city,
            email=user.email,
            phone=user.phone
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))