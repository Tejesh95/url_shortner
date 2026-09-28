from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, field_validator


class CreateURLRequest(BaseModel):
    original_url: HttpUrl
    custom_alias: str | None = Field(default=None, min_length=3, max_length=20)
    expires_in_days: int | None = Field(default=None, ge=1, le=3650)

    @field_validator("custom_alias")
    @classmethod
    def normalize_alias(cls, value: str | None) -> str | None:
        return value.strip() if value else value


class CreateURLResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str
    created_at: datetime
    expires_at: datetime | None
