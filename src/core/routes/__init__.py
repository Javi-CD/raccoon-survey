from __future__ import annotations

from flask import Flask

from src.ui.routes.pages import bp as ui_bp

from .anonymous import bp as anonymous_bp
from .auth import auth_bp
from .docs import bp as docs_bp
from .maintenance import bp as maintenance_bp
from .metrics import bp as metrics_bp
from .questions import bp as questions_bp
from .reports import bp as reports_bp
from .surveys import bp as surveys_bp
from .teams import bp as teams_bp
from .tokens import bp as tokens_bp


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
    app.register_blueprint(tokens_bp, url_prefix="/api/v1/tokens")
    app.register_blueprint(maintenance_bp, url_prefix="/api/v1/maintenance")
    app.register_blueprint(anonymous_bp, url_prefix="/api/v1/anonymous")
    app.register_blueprint(reports_bp, url_prefix="/api/v1/reports")
    app.register_blueprint(metrics_bp, url_prefix="/api/v1/metrics")
    app.register_blueprint(docs_bp, url_prefix="/api/v1")
    app.register_blueprint(ui_bp)


__all__ = ["register_routes"]
