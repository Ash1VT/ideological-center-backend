import uuid

from fastapi_users import FastAPIUsers

from db.sqlalchemy.models import User
from modules.users.auth.backend import auth_backend
from modules.users.manager.manager import get_user_manager

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
