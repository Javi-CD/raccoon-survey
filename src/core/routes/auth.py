# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from flask import Blueprint, current_app, g, jsonify, request
from flask_jwt_extended import (
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from src.core.middlewares.rbac import role_required
from src.core.middlewares.user_required import user_required
from src.core.services import auth_service

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/login")
@user_required(source="json", key="email", field="email")
def login():
    """Handles user login and generates JWT tokens.

    Returns:
        JSON: A JSON response containing access and refresh tokens.
    """
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    user = getattr(g, "current_user", None)
    if not user:
        return jsonify({"message": "user not found"}), 404

    if not auth_service.verify_user_active_role(user):
        return jsonify({"message": "unauthorized"}), 403

    if not auth_service.check_password(user, password):
        return jsonify({"message": "invalid credentials"}), 401

    access_expires_seconds = int(
        current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 900)
    )
    refresh_expires_seconds = int(
        current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES", 2592000)
    )

    tokens = auth_service.create_tokens(
        user, access_expires_seconds, refresh_expires_seconds
    )

    return jsonify(tokens), 200


@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    """Handles token refresh and generates a new access token.

    Returns:
        JSON: A JSON response containing a new access token.
    """
    identity = get_jwt_identity()
    jwt_payload = get_jwt()
    claims = {
        "role": jwt_payload.get("role"),
        "team_id": jwt_payload.get("team_id"),
        "name": jwt_payload.get("name"),
    }
    access_expires_seconds = int(
        current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 900)
    )
    result = auth_service.refresh_access_token(identity, claims, access_expires_seconds)

    return jsonify(result), 200


@auth_bp.post("/logout")
@jwt_required()
def logout():
    """Handles user logout and revokes the refresh token.

    Returns:
        JSON: A JSON response confirming successful logout.
    """
    jti = get_jwt().get("jti")
    auth_service.revoke_token(jti)

    return jsonify({"message": "logout successful"}), 200


@auth_bp.get("/me")
@role_required("admin", "rrhh")
def me():
    """Handles user profile retrieval.

    Returns:
        JSON: A JSON response containing user profile information.
    """
    jwt_payload = get_jwt()
    identity = get_jwt_identity()
    profile = auth_service.profile_from_jwt(identity, jwt_payload)

    return jsonify(profile), 200
