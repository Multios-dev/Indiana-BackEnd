from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.users import router as user_router
from app.api.routes.organizations import router as organization_router
from app.api.routes.memberships import router as memberships_router
from app.api.routes.events import router as events_router

from app.core.exceptions import AppException
from app.core.redis.exception_handlers import app_exception_handler

# Création de l'application FastAPI
app = FastAPI()

app.add_exception_handler(AppException, app_exception_handler)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers de l'application
app.include_router(user_router)
app.include_router(organization_router)
app.include_router(memberships_router)
app.include_router(events_router)