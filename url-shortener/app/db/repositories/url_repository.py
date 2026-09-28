from datetime import datetime, timezone
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.core.exceptions import AliasAlreadyExists
from app.db.models.url import URL


class URLRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        short_code: str,
        original_url: str,
        expires_at: datetime | None,
    ) -> URL:
        row = URL(
            short_code=short_code,
            original_url=original_url,
            expires_at=expires_at,
        )
        self.db.add(row)
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise AliasAlreadyExists("alias already exists") from exc
        self.db.refresh(row)
        return row

    def get_by_code(self, short_code: str) -> URL | None:
        return self.db.execute(
            select(URL).where(URL.short_code == short_code)
        ).scalar_one_or_none()

    def delete_expired(self, now: datetime | None = None) -> int:
        now = now or datetime.now(timezone.utc)
        result = self.db.execute(
            delete(URL).where(
                URL.expires_at.is_not(None),
                URL.expires_at <= now,
            )
        )
        self.db.commit()
        return result.rowcount or 0
