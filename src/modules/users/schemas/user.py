import uuid

from pydantic import BaseModel, Field, EmailStr
from fastapi_users import schemas
from pydantic.json_schema import SkipJsonSchema


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class SuperuserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_active: SkipJsonSchema[bool] = True
    is_superuser: SkipJsonSchema[bool] = True
    is_verified: SkipJsonSchema[bool] = True
