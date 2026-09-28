class AppError(Exception):
    pass


class InvalidURL(AppError):
    pass


class InvalidAlias(AppError):
    pass


class AliasAlreadyExists(AppError):
    pass


class URLNotFound(AppError):
    pass


class URLExpired(AppError):
    pass


class RateLimitExceeded(AppError):
    pass
