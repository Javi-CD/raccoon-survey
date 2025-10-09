from __future__ import annotations

from datetime import timedelta

from flask import Blueprint, current_app, g, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash

from src.core.middlewares.rbac import role_required
from src.core.middlewares.user_required import user_required
from src.core.services import jwt_blocklist

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

    if not user.role or getattr(user.role, "state", True) is False:
        return jsonify({"message": "unauthorized"}), 403

    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "invalid credentials"}), 401

    claims = {
        "role": user.role.name,
        "team_id": user.team_id,
        "name": user.name,
    }

    access_expires = timedelta(
        seconds=int(current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 900))
    )
    refresh_expires = timedelta(
        seconds=int(current_app.config.get("JWT_REFRESH_TOKEN_EXPIRES", 2592000))
    )

    access_token = create_access_token(
        identity=str(user.id), additional_claims=claims, expires_delta=access_expires
    )
    refresh_token = create_refresh_token(
        identity=str(user.id), additional_claims=claims, expires_delta=refresh_expires
    )

    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


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
    access_expires = timedelta(
        seconds=int(current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES", 900))
    )
    access_token = create_access_token(
        identity=identity, additional_claims=claims, expires_delta=access_expires
    )

    return jsonify({"access_token": access_token}), 200


@auth_bp.post("/logout")
@jwt_required()
def logout():
    """Handles user logout and revokes the refresh token.

    Returns:
        JSON: A JSON response confirming successful logout.
    """
    jti = get_jwt().get("jti")
    jwt_blocklist.revoke_token(jti)

    return jsonify({"message": "logout successful"}), 200


@auth_bp.get("/me")
@role_required("admin", "rrhh")
def me():
    """Handles user profile retrieval.

    Returns:
        JSON: A JSON response containing user profile information.
    """
    jwt_payload = get_jwt()
    return (
        jsonify(
            {
                "id": get_jwt_identity(),
                "role": jwt_payload.get("role"),
                "team_id": jwt_payload.get("team_id"),
                "name": jwt_payload.get("name"),
            }
        ),
        200,
    )
