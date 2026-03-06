from fastapi import APIRouter, Depends, HTTPException

from app.schemas.dtos.input.user_update_input import UserUpdateInput
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

@router.put("/{user_id}", summary="Modifier les données d'un utilisateur")
async def update_user(
        user_id:int,
        payload: UserUpdateInput,
        service:UserService=Depends(get_user_service),
):
    try:
        user = await service.update_user(
            user_id,
            payload.model_dump()    # Permet de convertir un modèle de données en un dictionnaire
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", summary="Supprimer un utilisateur")
async def delete_user(
        user_id:int,
        service:UserService=Depends(get_user_service),
):
    try:
        user = await service.delete_user(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))