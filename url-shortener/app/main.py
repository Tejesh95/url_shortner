from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import (
    AliasAlreadyExists,
    InvalidAlias,
    InvalidURL,
    RateLimitExceeded,
    URLExpired,
    URLNotFound,
)
from app.core.logging import configure_logging
from app.middleware.request_id import RequestIDMiddleware

configure_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-style URL shortener",
)

app.add_middleware(RequestIDMiddleware)
app.include_router(api_router)


def _error_handler(status_code: int):
    async def handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=status_code,
            content={"detail": str(exc)},
        )
    return handler


app.add_exception_handler(InvalidURL, _error_handler(400))
app.add_exception_handler(InvalidAlias, _error_handler(400))
app.add_exception_handler(URLNotFound, _error_handler(404))
app.add_exception_handler(URLExpired, _error_handler(410))
app.add_exception_handler(AliasAlreadyExists, _error_handler(409))
app.add_exception_handler(RateLimitExceeded, _error_handler(429))


@app.get("/", include_in_schema=False)
def root():
    return {
        "service": settings.app_name,
        "status": "running",
        "docs": "/docs",
    }
