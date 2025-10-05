from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from pathlib import Path


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
