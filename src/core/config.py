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


from typing import ClassVar


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
    JWT_SECRET_KEY: ClassVar[str] = os.getenv("JWT_SECRET_KEY", "change-me-in-prod")

    # CORS
    CORS_ORIGINS: ClassVar[tuple[str, ...]] = tuple(
        os.getenv("CORS_ORIGINS", "*").split(",")
    )


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
