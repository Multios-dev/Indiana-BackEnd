from fastapi import APIRouter, Depends, Request
from app.schemas.dtos.input.user_input import UserCreateInput, UserUpdateInput
from app.schemas.dtos.output.user_output import UserOutput
from app.schemas.pagination import PaginationParams
from app.services.user_service import UserService, get_user_service
from uuid import UUID

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserOutput, summary="Créer un utilisateur")
async def create_user(
        payload: UserCreateInput,
        service: UserService = Depends(get_user_service),
):
    return await service.create_user(payload)

@router.get("/", response_model = list[UserOutput], summary="Récupérer les utilisateurs")
async def get_users(
        request: Request,
        pagination: PaginationParams = Depends(),
        service: UserService = Depends(get_user_service),
):
    filters = {
        key: value
        for key, value in request.query_params.items()
        if key not in {"skip", "limit"}
    }
    return await service.get_users(pagination.skip, pagination.limit, filters)

@router.get("/{user_id}", response_model=UserOutput, summary="Récupérer un utilisateur spécifique")
async def get_user(
        user_id: UUID,
        service: UserService = Depends(get_user_service)
):
    return await service.get_user_by_id(user_id)

@router.put("/{user_id}", response_model=UserOutput, summary="Modifier les données d'un utilisateur")
async def update_user(
        user_id: UUID,
        payload: UserUpdateInput,
        service: UserService = Depends(get_user_service),
):
    return await service.update_user(user_id, payload)

@router.delete("/{user_id}", status_code=200, response_model=dict, summary="Supprimer un utilisateur")
async def delete_user(
        user_id: UUID,
        service: UserService = Depends(get_user_service),
):
    return await service.delete_user(user_id)