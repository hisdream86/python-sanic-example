import os
import sys
import multiprocessing
import tomlkit


def app_name():
    with open(file="pyproject.toml") as f:
        return tomlkit.parse(string=f.read())["tool"]["poetry"]["name"]


def app_version():
    with open(file="pyproject.toml") as f:
        return tomlkit.parse(string=f.read())["tool"]["poetry"]["version"]


class BaseConfig:
    APP_NAME = app_name()
    APP_VERSION = app_version()
    HOST = "0.0.0.0"
    PORT = 80
    ACCESS_LOG = False
    DEBUG = False
    NUM_WORKERS = max(int(multiprocessing.cpu_count()), 2)
    AUTO_RELOAD = True
    LOG_CONFIG = {
        "version": 1,
        "disable_existing_loggers": True,
        "loggers": {
            "sanic.root": {"level": "INFO", "handlers": ["console"]},
            "sanic.error": {
                "level": "INFO",
                "handlers": ["error_console"],
                "propagate": False,
                "qualname": "sanic.error",
            },
            "sanic.access": {
                "level": "INFO",
                "handlers": ["access_console"],
                "propagate": False,
                "qualname": "sanic.access",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "message",
                "stream": sys.stdout,
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "message",
                "stream": sys.stderr,
            },
            "access_console": {
                "class": "logging.StreamHandler",
                "formatter": "message",
                "stream": sys.stdout,
            },
        },
        "formatters": {
            "message": {
                "format": "%(message)s",
            }
        },
    }
    PG_HOST = os.environ.get("DATABASE_HOST")
    PG_USER = os.environ.get("DATABASE_USER")
    PG_PASSWORD = os.environ.get("DATABASE_PASSWORD")
    PG_PORT = 5432
    PG_POOL_SIZE = 10
    PG_POOL_MAX_OVERFLOW = 10
    PG_DEBUG = False
