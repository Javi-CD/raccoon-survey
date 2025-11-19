# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from flask import Blueprint, jsonify, request

from src.core.middlewares.rbac import role_required
from src.core.models import Role
from src.core.services import roles_service

bp = Blueprint("roles", __name__)


def serialize_role(r: Role) -> dict:
    return {
        "id": r.id,
        "name": r.name,
        "description": r.description,
        "state": r.state,
    }


@bp.get("/")
@role_required("admin", "rrhh")
def list_roles() -> tuple[list[dict], int]:
    """List all roles.

    Returns:
        tuple[list[dict], int]: A tuple containing a list of role dictionaries and an HTTP status code.
    """
    rows = roles_service.list_roles(active_only=True)
    return jsonify([serialize_role(r) for r in rows]), 200


@bp.post("/")
@role_required("admin", "rrhh")
def create_role() -> tuple[dict, int]:
    """Create a role.

    Returns:
        tuple[dict, int]: Serialized role and HTTP status code.
    """
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    description = payload.get("description")

    if not name:
        return jsonify({"message": "name is required"}), 400

    role = roles_service.create_role({"name": name, "description": description})

    return jsonify(serialize_role(role)), 201


@bp.get("/<int:role_id>")
@role_required("admin", "rrhh")
def get_role(role_id: int) -> tuple[dict, int]:
    """Get a role by ID.

    Args:
        role_id (int): Role ID.

    Returns:
        tuple[dict, int]: Serialized role and HTTP status code.
    """
    role = roles_service.get_role(role_id)
    if not role:
        return jsonify({"message": "role not found"}), 404

    return jsonify(serialize_role(role)), 200


@bp.put("/<int:role_id>")
@role_required("admin", "rrhh")
def update_role(role_id: int) -> tuple[dict, int]:
    """Update a role.

    Args:
        role_id (int): Role ID.

    Returns:
        tuple[dict, int]: Serialized role and HTTP status code.
    """
    existing = roles_service.get_role(role_id)
    if not existing:
        return jsonify({"message": "role not found"}), 404

    payload = request.get_json(silent=True) or {}
    role = roles_service.update_role(
        role_id,
        {
            "name": payload.get("name"),
            "description": payload.get("description"),
            "state": payload.get("state"),
        },
    )

    return jsonify(serialize_role(role)), 200


@bp.delete("/<int:role_id>")
@role_required("admin", "rrhh")
def change_role_state(role_id: int) -> tuple[dict, int]:
    """Change role state.

    Args:
        role_id (int): Role ID.

    Returns:
        tuple[dict, int]: Serialized role and HTTP status code.
    """
    existing = roles_service.get_role(role_id)
    if not existing:
        return jsonify({"message": "role not found"}), 404

    role = roles_service.set_role_state(role_id, False)

    return jsonify(serialize_role(role)), 200


__all__ = ["bp"]
