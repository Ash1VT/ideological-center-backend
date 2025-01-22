from typing import Callable, List

from pydantic_settings import BaseSettings, SettingsConfigDict

from config.directories import BASE_DIRECTORY
from core.uow.generic import GenericUnitOfWork
from setup.sqlalchemy.uow import get_sqlalchemy_uow


class AppSettings(BaseSettings):
    secret_key: str
    firebase_storage_bucket: str
    cors_origins: List[str]

    get_uow: Callable[[], GenericUnitOfWork] = get_sqlalchemy_uow

    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")
