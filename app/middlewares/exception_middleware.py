from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.exceptions import AppException


def add_cors_headers(response: JSONResponse, origin: str | None) -> JSONResponse:
    # Add CORS headers to the response if an origin is present
    if origin:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Vary"] = "Origin"
    return response

async def exception_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except AppException as e:
        resp = JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
        return add_cors_headers(resp, request.headers.get("origin"))
    except HTTPException as e:
        # Handle known HTTP exceptions (401, 403, 404, etc.)
        resp = JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
        return add_cors_headers(resp, request.headers.get("origin"))
    except Exception as e:
        # Handle unexpected server errors
        resp =  JSONResponse(
            status_code=500,
            content={"detail": f"Unexpected server error: {str(e)}"}
        )
        return add_cors_headers(resp, request.headers.get("origin"))