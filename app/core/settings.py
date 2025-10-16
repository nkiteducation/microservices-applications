from pathlib import Path
from typing import Literal

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


class Logger(CoreSettings):
    fmt: str = (
        "%(asctime)s[%(levelname)8s|%(name)s:%(funcName)s:%(levelno)s]  %(message)s"
    )
    datefmt: str = "%Y-%m-%d %H:%M:%S"
    level: Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


class Settings(CoreSettings):
    root_path: str

    database: DataBase
    logger: Logger


config = Settings()
