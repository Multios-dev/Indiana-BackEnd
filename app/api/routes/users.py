from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user.user_repository import UserRepository
from app.db.session import get_db
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", summary="Récupérer tous les utilisateurs")
async def get_users(db:AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.get_all_users()

@router.get("/{id}", summary="Récupérer un utilisateur spécifique")
async def get_user(user_id:int,db:AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    service = UserService(repo)
    return await service.get_user_by_id(user_id)