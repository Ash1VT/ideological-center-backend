from fastapi_users.authentication import JWTStrategy

from setup.settings.app import get_app_settings

settings = get_app_settings()


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_key, lifetime_seconds=3600)
