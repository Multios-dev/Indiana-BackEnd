from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from app.api.routes.users import router as user_router
from app.api.routes.organizations import router as organization_router
from app.api.routes.memberships import router as memberships_router
from app.api.routes.events import router as events_router
from app.api.routes.addresses import router as address_router
from app.api.routes.auth import router as auth_router
from app.db.init_db import init_db
from app.db.session import engine
from contextlib import asynccontextmanager
from app.middlewares.auth_middleware import auth_middleware
from app.middlewares.exception_middleware import exception_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # startup
    yield
    await engine.dispose()

# FastAPI application creation
app = FastAPI(lifespan=lifespan)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Indiana API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middlewares
app.middleware("http")(auth_middleware)
app.middleware("http")(exception_middleware)

# Application routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(organization_router)
app.include_router(memberships_router)
app.include_router(events_router)
app.include_router(address_router)