from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback
from starlette.middleware.cors import CORSMiddleware
from app.api.routes.users import router as user_router
from app.api.routes.organizations import router as organization_router
from app.api.routes.memberships import router as memberships_router
from app.api.routes.events import router as events_router

from app.core.exceptions import AppException
from app.core.redis.exception_handlers import app_exception_handler
from app.db.init_db import init_db
from app.db.model_loader import load_all_models
from app.db.session import engine
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # startup
    yield
    await engine.dispose()

# FastAPI application creation
app = FastAPI(lifespan=lifespan)

app.add_exception_handler(AppException, app_exception_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Application routers
app.include_router(user_router)
app.include_router(organization_router)
app.include_router(memberships_router)
app.include_router(events_router)