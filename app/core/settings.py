from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class CoreSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(".").rglob(".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )


class DataBase(CoreSettings):
    url: PostgresDsn


class Settings(CoreSettings):
    database: DataBase


config = Settings()
