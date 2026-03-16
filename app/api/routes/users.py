from fastapi import APIRouter, Depends, HTTPException, Request

from app.schemas.dtos.input.user_input import UserCreateInput, UserUpdateInput
from app.schemas.dtos.output.user_output import UserOutput
from app.services.user_service import UserService, get_user_service
from app.core.exceptions import UserNotFoundError

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", summary="Créer un utilisateur")
async def create_user(
        payload: UserCreateInput,
        service: UserService = Depends(get_user_service),
):
    try:
        user = await service.create_user(
            first_names=payload.first_names,
            last_name=payload.last_name,
            birth_date=payload.birth_date,
            gender=payload.gender,
            totem=payload.totem,
            quali=payload.quali,
            is_legal_guardian=payload.is_legal_guardian,
        )
        return UserOutput.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", summary="Récupérer les utilisateurs")
async def get_users(
        request: Request,
        service: UserService = Depends(get_user_service),
):
    try:
        filters = dict(request.query_params)
        users = await service.get_users(filters if filters else None)
        return [UserOutput.model_validate(u) for u in users]
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{user_id}", summary="Récupérer un utilisateur spécifique")
async def get_user(
        user_id: int,
        service: UserService = Depends(get_user_service)
):
    try:
        user = await service.get_user_by_id(user_id)
        return UserOutput.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{user_id}", summary="Modifier les données d'un utilisateur")
async def update_user(
        user_id: int,
        payload: UserUpdateInput,
        service: UserService = Depends(get_user_service),
):
    try:
        user = await service.update_user(user_id, payload.model_dump(exclude_unset=True))
        return UserOutput.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{user_id}", summary="Supprimer un utilisateur")
async def delete_user(
        user_id: int,
        service: UserService = Depends(get_user_service),
):
    try:
        user = await service.delete_user(user_id)
        return UserOutput.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))