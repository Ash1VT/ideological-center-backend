from abc import ABC
from typing import Optional, List

from pydantic_settings import BaseSettings, SettingsConfigDict
from config.directories import BASE_DIRECTORY
from config.settings.db import PostgresSqlSettings, SqliteSettings


class ServerSettings(BaseSettings, ABC):
    web_app_host: str
    web_app_port: int

    email_host: str
    email_host_user: str
    email_host_password: str
    email_port: int
    email_use_ssl: bool
    email_use_tls: bool
    email_from: str
    email_from_name: str

    origins: List[str]
    reload: bool


class DevelopServerSettings(ServerSettings, PostgresSqlSettings):
    reload: bool = True
    origins: List[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")


class TestServerSettings(ServerSettings, SqliteSettings):
    reload: bool = False
    origins: List[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")


class ProductionServerSettings(ServerSettings, PostgresSqlSettings):
    reload: bool = False
    origins: List[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=BASE_DIRECTORY / ".env", extra="allow")
