from __future__ import annotations

import datetime
import os
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import check_password_hash

from . import models as _models
from .routes.auth import auth_bp

try:
    from flask_jwt_extended import (
        JWTManager,
        create_access_token,
        create_refresh_token,
        get_jwt,
        get_jwt_identity,
        jwt_required,
    )
except ImportError:
    JWTManager = None

from .config import get_config_class
from .database import db
from .models import User
from .services import jwt_blocklist


def create_app(config: dict[str, Any] | None = None) -> Flask:
    """Application Factory

    Creates and configures the Flask app instance and initializes extensions.

    Args:
        config (dict[str, Any] | None, optional): Application configuration overrides.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__)

    config_class = get_config_class(os.getenv("FLASK_ENV"))
    app.config.from_object(config_class)

    # Apply provided config overrides
    if config:
        app.config.update(config)

    # Initialize CORS
    CORS(
        app,
        resources={r"/*": {"origins": config_class.CORS_ORIGINS}},
        supports_credentials=True,
    )

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize JWT if available
    if JWTManager is not None:
        jwt = JWTManager(app)

        @jwt.token_in_blocklist_loader
        def check_if_token_revoked(_jwt_header, jwt_payload):
            jti = jwt_payload.get("jti")
            return jwt_blocklist.is_token_revoked(jti)

    # Healthcheck endpoint
    @app.get("/api/v1/health")
    def health() -> tuple[dict, int]:
        return {
            "message": "Success",
            "status": "200",
            "timestamp": datetime.datetime.now().isoformat(),
        }, 200


    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    @app.errorhandler(404)
    def not_found(_: Exception) -> tuple[dict, int]:  # type: ignore[override]
        return jsonify(
            {"status": "404", "message": f"resource {request.path} not found"}
        ), 404

    @app.errorhandler(500)
    def server_error(_: Exception) -> tuple[dict, int]:  # type: ignore[override]
        return jsonify({"status": "500", "message": "server_error"}), 500

    return app
