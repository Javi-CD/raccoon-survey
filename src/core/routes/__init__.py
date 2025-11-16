# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from flask import Flask

from src.ui.routes.pages import bp as ui_bp

from .anonymous import bp as anonymous_bp
from .auth import auth_bp
from .categories import bp as categories_bp
from .docs import bp as docs_bp
from .maintenance import bp as maintenance_bp
from .metrics import bp as metrics_bp
from .questions import bp as questions_bp
from .reports import bp as reports_bp
from .roles import bp as roles_bp
from .surveys import bp as surveys_bp
from .teams import bp as teams_bp
from .tokens import bp as tokens_bp
from .users import bp as users_bp


def register_routes(app: Flask) -> None:
    """Register application blueprints.

    This keeps route registration centralized and tidy.

    Args:
        app (Flask): Flask instance
    """
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(teams_bp, url_prefix="/api/v1/teams")
    app.register_blueprint(users_bp, url_prefix="/api/v1/users")
    app.register_blueprint(surveys_bp, url_prefix="/api/v1/surveys")
    app.register_blueprint(questions_bp, url_prefix="/api/v1/questions")
    app.register_blueprint(tokens_bp, url_prefix="/api/v1/tokens")
    app.register_blueprint(categories_bp, url_prefix="/api/v1/categories")
    app.register_blueprint(maintenance_bp, url_prefix="/api/v1/maintenance")
    app.register_blueprint(anonymous_bp, url_prefix="/api/v1/anonymous")
    app.register_blueprint(reports_bp, url_prefix="/api/v1/reports")
    app.register_blueprint(metrics_bp, url_prefix="/api/v1/metrics")
    app.register_blueprint(roles_bp, url_prefix="/api/v1/roles")
    app.register_blueprint(docs_bp, url_prefix="/api/v1")
    app.register_blueprint(ui_bp)


__all__ = ["register_routes"]
