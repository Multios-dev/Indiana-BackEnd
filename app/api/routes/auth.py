from fastapi import APIRouter, Depends
from app.schemas.dtos.input.user_input import UserLoginInput
from app.schemas.dtos.output.user_output import UserOutput, UserLoginOutput
from app.services.auth_service import AuthService, get_auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=UserLoginOutput)
async def login(
        payload: UserLoginInput,
        service: AuthService = Depends(get_auth_service),
):
    return await service.login(payload)