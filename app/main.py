from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as user_router
from app.api.routes.organizations import router as organization_router
from app.api.routes.memberships import router as memberships_router

# Création de l'application FastAPI
app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers de l'application
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(organization_router)
app.include_router(memberships_router)