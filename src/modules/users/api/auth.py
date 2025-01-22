from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import BaseUserManager, schemas
from fastapi_users.exceptions import UserAlreadyExists

from db.sqlalchemy.models import User
from modules.users.auth import fastapi_users, auth_backend
from modules.users.schemas.user import UserRead, UserUpdate, SuperuserCreate

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)

# auth_router.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )

# auth_router.include_router(
#     fastapi_users.get_reset_password_router(),
#     prefix="/auth",
#     tags=["auth"],
# )

# auth_router.include_router(
#     fastapi_users.get_verify_router(UserRead),
#     prefix="/auth",
#     tags=["auth"],
# )

auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@auth_router.post("/users/superuser", tags=["users"], response_model=UserRead)
async def create_superuser(
    user_data: SuperuserCreate,
    user_manager: BaseUserManager = Depends(fastapi_users.get_user_manager),
    current_user: User = Depends(fastapi_users.current_user(superuser=True)),
):
    """
    Эндпоинт для создания суперпользователя.
    Доступен только для авторизованных суперпользователей.
    """
    user_data.is_verified = True
    user_data.is_superuser = True
    user_data.is_active = True

    try:
        user = await user_manager.create(user_data, safe=False)
        return schemas.model_validate(UserRead, user)
    except UserAlreadyExists:
        raise HTTPException(
            status_code=400, detail="User with this email already exists"
        )
