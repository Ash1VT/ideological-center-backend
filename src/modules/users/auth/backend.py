from fastapi_users.authentication import AuthenticationBackend

from modules.users.auth.jwt import get_jwt_strategy
from modules.users.auth.transport import transport

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=transport,
    get_strategy=get_jwt_strategy,
)
