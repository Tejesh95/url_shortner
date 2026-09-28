from datetime import datetime
from app.db.repositories.url_repository import URLRepository
from app.utils.validators import validate_alias


class AliasService:
    def __init__(self, repository: URLRepository):
        self.repository = repository

    def create(self, *, alias: str, original_url: str, expires_at: datetime | None):
        validated = validate_alias(alias)
        # PostgreSQL supplies the internal row ID; the public identifier is the alias.
        return self.repository.create(
short_code=validated,
            original_url=original_url,
            expires_at=expires_at,
        )
