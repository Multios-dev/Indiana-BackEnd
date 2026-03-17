from fastapi import APIRouter, Depends, Request

from app.schemas.dtos.input.user_input import UserCreateInput, UserUpdateInput
from app.schemas.dtos.output.user_output import UserOutput
from app.services.user_service import UserService, get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", summary="Créer un utilisateur")
async def create_user(
        payload: UserCreateInput,
        service: UserService = Depends(get_user_service),
):
    user = await service.create_user(payload)
    # model_validate permet de convertir un objet SQLAlchemy en objet Pydantic
    return UserOutput.model_validate(user)

@router.get("/", summary="Récupérer les utilisateurs")
async def get_users(
        request: Request,
        service: UserService = Depends(get_user_service),
):
    filters = dict(request.query_params)
    users = await service.get_users(filters if filters else None)
    return [UserOutput.model_validate(u) for u in users]

@router.get("/{user_id}", summary="Récupérer un utilisateur spécifique")
async def get_user(
        user_id: int,
        service: UserService = Depends(get_user_service)
):
    user = await service.get_user_by_id(user_id)
    return UserOutput.model_validate(user)

@router.put("/{user_id}", summary="Modifier les données d'un utilisateur")
async def update_user(
        user_id: int,
        payload: UserUpdateInput,
        service: UserService = Depends(get_user_service),
):
    user = await service.update_user(user_id, payload)
    return UserOutput.model_validate(user)

@router.delete("/{user_id}", summary="Supprimer un utilisateur")
async def delete_user(
        user_id: int,
        service: UserService = Depends(get_user_service),
):
    user = await service.delete_user(user_id)
    return UserOutput.model_validate(user)