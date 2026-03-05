from fastapi import APIRouter, HTTPException

from app.schemas.dtos.input.user_input import UserLoginInput, UserRegisterInput
from app.schemas.dtos.output.user_output import UserOutput
router = APIRouter(prefix="/auth",tags=["auth"])

users=[]

@router.post("/login", summary="Connecter un utilisateur")
def login(user:UserLoginInput):
    for u in users:
        if u["email"] == user.email and u["password"] == user.password:
            return UserOutput(
                id=u["id"],
                email=u["email"]
            )

    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/register", summary="Inscrire un utilisateur")
def register(user:UserRegisterInput):
    new_user = {
        "id": len(user.email) + 1,
        "email":user.email,
        "password":user.password,
    }

    users.append(new_user)

    return UserOutput(
        id = new_user["id"],
        email = new_user["email"],
    )