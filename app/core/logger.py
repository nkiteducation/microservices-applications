import logging
import logging.handlers
import re
from logging.config import dictConfig
from pathlib import Path

import orjson
from app.core.settings import config

B = 1
KB = 1024 * B
MB = 1024 * KB
GB = 1024 * MB


class JSONFormatter(logging.Formatter):
    def __init__(self, parameters: list, **kwargs):
        super().__init__(**kwargs)
        self.parameters = parameters

    def format(self, record: logging.LogRecord):
        log_entry = {
            key: value
            for key, value in record.__dict__.items()
            if key in self.parameters
        }
        return orjson.dumps(log_entry).decode()


class BaseFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        return super().format(record)


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": JSONFormatter,
            "parameters": [
                "asctime",
                "created",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "message",
                "module",
                "msecs",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "thread",
                "threadName",
                "taskName",
            ],
            "datefmt": config.logger.datefmt,
        },
        "base": {
            "()": BaseFormatter,
            "fmt": config.logger.fmt,
            "datefmt": config.logger.datefmt,
        },
    },
    "handlers": {
        "console": {
            "class": logging.StreamHandler,
            "formatter": "base",
            "stream": "ext://sys.stdout",
            "level": config.logger.level,
        },
        "file": {
            "class": logging.handlers.RotatingFileHandler,
            "formatter": "json",
            "filename": "logs/app.log",
            "maxBytes": 5 * GB,
            "backupCount": 3,
            "encoding": "utf-8",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "NOTSET",
        }
    },
}


def setup_logging():
    Path("./logs").mkdir(exist_ok=True)
    dictConfig(LOGGING_CONFIG)
