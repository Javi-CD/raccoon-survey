# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from flask import Blueprint, jsonify, request

from src.core.middlewares.rbac import role_required
from src.core.models import User
from src.core.services import users_service

bp = Blueprint("users", __name__)


def serialize_user(u: User) -> dict:
    """Serialize a user instance.

    Args:
        u (User): User instance.

    Returns:
        dict: Serialized user.
    """
    return {
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "role_id": u.role_id,
        "team_id": u.team_id,
        "role": {"id": u.role.id, "name": u.role.name} if u.role else None,
        "team": {"id": u.team.id, "name": u.team.name} if u.team else None,
        "state": u.state,
        "created_at": u.created_at.isoformat() if u.created_at else None,
    }


@bp.get("/")
@role_required("admin", "rrhh")
def list_users() -> tuple[list[dict], int]:
    """List users).

    Returns:
        tuple[list[dict], int]: A tuple containing a list of user dictionaries and an HTTP status code.
    """
    rows = users_service.list_users(active_only=True)

    return jsonify([serialize_user(u) for u in rows]), 200


@bp.post("/")
@role_required("admin", "rrhh")
def create_user() -> tuple[dict, int]:
    """Create a user.

    Returns:
        tuple[dict, int]: A tuple containing the serialized user dictionary and an HTTP status code.
    """
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip().lower()
    password = payload.get("password")
    role_id = payload.get("role_id")
    team_id = payload.get("team_id")

    if not name:
        return jsonify({"message": "name is required"}), 400
    if not email:
        return jsonify({"message": "email is required"}), 400
    if not password:
        return jsonify({"message": "password is required"}), 400

    user = users_service.create_user(
        {
            "name": name,
            "email": email,
            "password": password,
            "role_id": role_id,
            "team_id": team_id,
        }
    )

    return jsonify(serialize_user(user)), 201


@bp.get("/<int:user_id>")
@role_required("admin", "rrhh")
def get_user(user_id: int) -> tuple[dict, int]:
    """Get a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        tuple[dict, int]: A tuple containing the serialized user dictionary and an HTTP status code.
    """
    user = users_service.get_user(user_id)
    if not user:
        return jsonify({"message": "user not found"}), 404

    return jsonify(serialize_user(user)), 200


@bp.put("/<int:user_id>")
@role_required("admin", "rrhh")
def update_user(user_id: int) -> tuple[dict, int]:
    """Update a user.

    Args:
        user_id (int): The ID of the user to update.

    Returns:
        tuple[dict, int]: A tuple containing the serialized user dictionary and an HTTP status code.
    """
    existing = users_service.get_user(user_id)
    if not existing:
        return jsonify({"message": "user not found"}), 404

    payload = request.get_json(silent=True) or {}

    user = users_service.update_user(
        user_id,
        {
            "name": payload.get("name"),
            "email": payload.get("email"),
            "password": payload.get("password"),
            "role_id": payload.get("role_id"),
            "team_id": payload.get("team_id"),
            "state": payload.get("state"),
        },
    )

    return jsonify(serialize_user(user)), 200


@bp.patch("/<int:user_id>/state")
@role_required("admin", "rrhh")
def change_user_state(user_id: int) -> tuple[dict, int]:
    """Change a user state.

    Args:
        user_id (int): The ID of the user to update.

    Returns:
        tuple[dict, int]: A tuple containing the serialized user dictionary and an HTTP status code.
    """
    existing = users_service.get_user(user_id)
    if not existing:
        return jsonify({"message": "user not found"}), 404

    payload = request.get_json(silent=True) or {}
    state = payload.get("state")
    if state is None:
        return jsonify({"message": "state is required"}), 400

    user = users_service.set_user_state(user_id, bool(state))

    return jsonify(serialize_user(user)), 200


__all__ = ["bp"]
