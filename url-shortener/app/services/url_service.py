from app.cache.counter import Counter
from app.cache.redis import get_redis
from app.db.repositories.url_repository import URLRepository
from app.services.alias_service import AliasService
from app.services.code_generator import CodeGenerator
from app.utils.time import expiry_from_days
from app.utils.validators import validate_url


class URLService:
    def __init__(self, repository: URLRepository):
        self.repository = repository
        self.code_generator = CodeGenerator(Counter(get_redis()))

    def create(
        self,
        *,
        original_url: str,
        custom_alias: str | None,
        expires_in_days: int | None,
    ):
        original_url = validate_url(original_url)
        expires_at = expiry_from_days(expires_in_days)

        if custom_alias:
            return AliasService(self.repository).create(
                alias=custom_alias,
                original_url=original_url,
                expires_at=expires_at,
            )

        short_code, _generated_id = self.code_generator.generate()
        return self.repository.create(
            short_code=short_code,
            original_url=original_url,
            expires_at=expires_at,
        )
