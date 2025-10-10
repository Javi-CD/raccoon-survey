from __future__ import annotations

import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv(
        dotenv_path=Path(__file__).resolve().parents[2] / ".env", override=False
    )

from typing import Any, ClassVar


class BaseConfig:
    """Base configuration for the Raccoon Survey backend."""

    # General
    ENV: ClassVar[str] = os.getenv("FLASK_ENV", "development")
    DEBUG: ClassVar[bool] = os.getenv("FLASK_DEBUG", "1") == "1"
    TESTING: ClassVar[bool] = False
    JSON_SORT_KEYS: ClassVar[bool] = False

    # JWT
    JWT_TOKEN_LOCATION: ClassVar[tuple[str, ...]] = ("headers",)
    JWT_HEADER_NAME: ClassVar[str] = "Authorization"
    JWT_HEADER_TYPE: ClassVar[str] = "Bearer"
    JWT_SECRET_KEY: ClassVar[str] = os.getenv("JWT_SECRET_KEY", None)
    JWT_ACCESS_TOKEN_EXPIRES: ClassVar[int] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "900"))
    JWT_REFRESH_TOKEN_EXPIRES: ClassVar[int] = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "2592000"))

    # CORS
    CORS_ORIGINS: ClassVar[tuple[str, ...]] = tuple(
        os.getenv("CORS_ORIGINS", "*").split(",")
    )

    # Database
    DATABASE_URL: ClassVar[str | None] = os.getenv("DATABASE_URL", None)
    DATABASE_ECHO: ClassVar[bool] = os.getenv("DATABASE_ECHO", "0") == "1"

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI: ClassVar[str | None] = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS: ClassVar[bool] = False
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict[str, Any]] = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
        "echo": DATABASE_ECHO,
    }

    # Default Admin User (used by seed script)
    DEFAULT_USER_ADMIN_EMAIL: ClassVar[str] = os.getenv("DEFAULT_USER_ADMIN_EMAIL", None)
    DEFAULT_USER_ADMIN_PASSWORD: ClassVar[str] = os.getenv("DEFAULT_USER_ADMIN_PASSWORD", None)
    DEFAULT_USER_ADMIN_NAME: ClassVar[str] = os.getenv("DEFAULT_USER_ADMIN_NAME", None)

    if not JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY must be set")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL must be set")
    if not DEFAULT_USER_ADMIN_EMAIL:
        raise ValueError("DEFAULT_USER_ADMIN_EMAIL must be set")
    if not DEFAULT_USER_ADMIN_PASSWORD:
        raise ValueError("DEFAULT_USER_ADMIN_PASSWORD must be set")
    if not DEFAULT_USER_ADMIN_NAME:
        raise ValueError("DEFAULT_USER_ADMIN_NAME must be set")


class DevConfig(BaseConfig):
    ENV = "development"
    DEBUG = True


class ProdConfig(BaseConfig):
    ENV = "production"
    DEBUG = False


class TestConfig(BaseConfig):
    ENV = "testing"
    DEBUG = False
    TESTING = True


def get_config_class(env: str | None = None) -> type[BaseConfig]:
    """Return the configuration class based on FLASK_ENV or provided env.

    Args:
        env (str | None, optional): Environment name. Defaults to None.

    Returns:
        type[BaseConfig]: Configuration class for the specified environment.
    """
    env = env or os.getenv("FLASK_ENV", "development")
    mapping = {
        "development": DevConfig,
        "production": ProdConfig,
        "testing": TestConfig,
        "test": TestConfig,
    }
    return mapping.get(env.lower(), DevConfig)


__all__ = [
    "BaseConfig",
    "DevConfig",
    "ProdConfig",
    "TestConfig",
    "get_config_class",
]
