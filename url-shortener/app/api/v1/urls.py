from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.repositories.url_repository import URLRepository
from app.db.session import get_db
from app.middleware.rate_limit import check_create_rate_limit
from app.schemas.url import CreateURLRequest, CreateURLResponse
from app.services.redirect_service import RedirectService
from app.services.url_service import URLService

router = APIRouter(tags=["URLs"])


@router.post("/urls", response_model=CreateURLResponse, status_code=status.HTTP_201_CREATED)
def create_url(
    payload: CreateURLRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    check_create_rate_limit(request)

    row = URLService(URLRepository(db)).create(
        original_url=str(payload.original_url),
        custom_alias=payload.custom_alias,
        expires_in_days=payload.expires_in_days,
    )

    settings = get_settings()
    return CreateURLResponse(
        short_code=row.short_code,
        short_url=f"{settings.base_url.rstrip('/')}/{row.short_code}",
        original_url=row.original_url,
        created_at=row.created_at,
        expires_at=row.expires_at,
    )


@router.get("/{short_code}", include_in_schema=False)
def redirect(short_code: str, db: Session = Depends(get_db)):
    result = RedirectService(db).resolve(short_code)
    return RedirectResponse(url=result.original_url, status_code=302)
