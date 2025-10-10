from __future__ import annotations

from flask import Flask

from .auth import auth_bp
from .questions import bp as questions_bp
from .surveys import bp as surveys_bp
from .teams import bp as teams_bp


def register_routes(app: Flask) -> None:
    """Register application blueprints.

    This keeps route registration centralized and tidy.

    Args:
        app (Flask): Flask instance
    """
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(teams_bp, url_prefix="/api/v1/teams")
    app.register_blueprint(surveys_bp, url_prefix="/api/v1/surveys")
    app.register_blueprint(questions_bp, url_prefix="/api/v1/questions")


__all__ = ["register_routes"]
