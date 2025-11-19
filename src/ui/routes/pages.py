# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from flask import (
    Blueprint,
    abort,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)

from src.ui.middlewares.handle_global_errors import register_global_error_handlers

bp = Blueprint(
    "ui",
    __name__,
    template_folder="../templates",
    static_folder="../static",
    static_url_path="/ui/static",
)

# Register global error handlers in the blueprint
register_global_error_handlers(bp)

# Private routes that require an active session
PRIVATE_UI_PATHS = {"/dashboard", "/surveys", "/reports", "/config"}


@bp.before_app_request
def _guard_private_ui_pages() -> None:
    """Guard private UI pages by checking session or access token.

    Returns:
        None: Redirects to login page if session or access token is missing.
    """
    try:
        path = request.path or ""
        if path in PRIVATE_UI_PATHS:
            has_session = (request.cookies.get("rs_has_session") or "") == "1"
            access = request.cookies.get("rs_access_token") or ""
            refresh = request.cookies.get("rs_refresh_token") or ""

            is_authenticated = has_session or (access and refresh)

            if not is_authenticated:
                return abort(401)

    except Exception:
        # Fallback
        return redirect(url_for("ui.login_page"))


@bp.get("/")
def home() -> str:
    """Render the home page.

    Returns:
        str: Rendered HTML template for the home page.
    """
    return render_template("index.html")


@bp.get("/login")
def login_page() -> str:
    """Render the login page.

    Returns:
        str: Rendered HTML template for the login page.
    """
    return render_template("pages/auth/login.html")


@bp.get("/dashboard")
def dashboard_page() -> str:
    """Render the dashboard page.

    Returns:
        str: Rendered HTML template for the dashboard page.
    """
    return render_template("pages/private/dashboard.html")


@bp.get("/surveys")
def surveys_page() -> str:
    """Render the surveys page.

    Returns:
        str: Rendered HTML template for the surveys page.
    """
    return render_template("pages/private/surveys.html")


@bp.get("/reports")
def reports_page() -> str:
    """Render the reports page.

    Returns:
        str: Rendered HTML template for the reports page.
    """
    return render_template("pages/private/reports.html")


@bp.get("/config")
def config_page() -> str:
    """Render the configuration page.

    Returns:
        str: Rendered HTML template for the configuration page.
    """
    return render_template("pages/private/config.html")


@bp.get("/solve")
def resolver_page() -> str:
    """Render the resolver page.

    Returns:
        str: Rendered HTML template for the resolver page.
    """
    return render_template("pages/public/solveSurveys.html")


@bp.get("/docs")
def api_docs_page() -> str:
    return render_template("pages/public/docs.html")


# ---------------------------------
# Bug Testing Routes
# ---------------------------------
@bp.get("/error/<int:code>")
def preview_error(code: int):
    """Preview error pages in development environment.

    Args:
        code (int): HTTP status code to preview.

    Returns:
        str: Rendered HTML template for the error page.
    """
    try:
        # Only enable if the app is in debug or non-production mode
        is_debug = current_app.debug or (current_app.env or "").lower() != "production"
        if not is_debug:
            return redirect(url_for("ui.home"))

    except Exception:  # noqa: S110
        # If the environment cannot be determined, allow in local mode
        pass

    if code in (400, 401, 404, 500):
        abort(code)

    abort(404)
