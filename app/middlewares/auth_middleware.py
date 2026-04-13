from fastapi import Request, HTTPException


async def auth_middleware(request: Request, call_next):
    # Public routes -> no authentication required
    public_paths = ("/docs", "/openapi.json", "/healthz")
    if request.url.path in public_paths:
        return await call_next(request)

    authorization = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization")

    # Dev mode (bypass token validation if KEYCLOAK_URL isn't set)
    if not settings.KEYCLOAK_URL:
        return await call_next(request)

    # TODO: validate token against Keycloak when configured

    return await call_next(request)