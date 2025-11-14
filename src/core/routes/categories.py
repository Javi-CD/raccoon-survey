# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from flask import Blueprint, jsonify, request

from src.core.middlewares.rbac import role_required
from src.core.models import Category
from src.core.services import categories_service

bp = Blueprint("categories", __name__)


def serialize_category(c: Category) -> dict:
    """Serialize category.

    Args:
        c (Category): Category to serialize.

    Returns:
        dict: Serialized category.
    """
    return {
        "id": c.id,
        "name": c.name,
        "description": c.description,
        "state": c.state,
        "created_at": c.created_at.isoformat() if c.created_at else None,
    }


@bp.get("/")
@role_required("admin", "rrhh")
def list_categories() -> tuple[list[dict], int]:
    """List categories.

    Returns:
        tuple[list[dict], int]: List of serialized categories and status code 200.
    """
    rows = categories_service.list_categories(active_only=True)

    return jsonify([serialize_category(c) for c in rows]), 200


@bp.post("/")
@role_required("admin", "rrhh")
def create_category() -> tuple[dict, int]:
    """Create category

    Returns:
        tuple[dict, int]: Serialized category and HTTP status code.
    """
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    description = payload.get("description")

    if not name:
        return jsonify({"message": "name is required"}), 400

    exists = Category.query.filter(Category.name == name).first()
    if exists:
        return jsonify({"message": "category with same name already exists"}), 409

    cat = categories_service.create_category({"name": name, "description": description})

    return jsonify(serialize_category(cat)), 201


@bp.get("/<int:category_id>")
@role_required("admin", "rrhh")
def get_category(category_id: int) -> tuple[dict, int]:
    """Get category by ID

    Args:
        category_id (int): Category ID

    Returns:
        tuple[dict, int]: Serialized category and HTTP status code.
    """
    cat = categories_service.get_category(category_id)
    if not cat:
        return jsonify({"message": "category not found"}), 404

    return jsonify(serialize_category(cat)), 200


@bp.put("/<int:category_id>")
@role_required("admin", "rrhh")
def update_category(category_id: int) -> tuple[dict, int]:
    """Update category

    Args:
        category_id (int): Category ID

    Returns:
        tuple[dict, int]: Serialized category with updated fields and HTTP status code.
    """
    cat = categories_service.get_category(category_id)
    if not cat:
        return jsonify({"message": "category not found"}), 404

    payload = request.get_json(silent=True) or {}
    update_data: dict = {}

    for field in ["name", "description", "state"]:
        if field in payload and payload[field] is not None:
            update_data[field] = payload[field]

    if "name" in update_data:
        name = (update_data["name"] or "").strip()
        if not name:
            return jsonify({"message": "name cannot be empty"}), 400

        is_duplicate_category = Category.query.filter(
            Category.name == name, Category.id != category_id
        ).first()
        if is_duplicate_category:
            return jsonify({"message": "category with same name already exists"}), 409

        update_data["name"] = name

    cat = categories_service.update_category(category_id, update_data)

    return jsonify(serialize_category(cat)), 200


@bp.patch("/<int:category_id>/state")
@role_required("admin", "rrhh")
def change_category_state(category_id: int) -> tuple[dict, int]:
    """Change category state

    Args:
        category_id (int): Category ID

    Returns:
        tuple[dict, int]: Serialized category with updated state and HTTP status code.
    """
    cat = categories_service.get_category(category_id)
    if not cat:
        return jsonify({"message": "category not found"}), 404

    payload = request.get_json(silent=True) or {}
    state = payload.get("state")
    if state is None:
        return jsonify({"message": "state is required"}), 400

    cat = categories_service.set_category_state(category_id, bool(state))

    return jsonify(serialize_category(cat)), 200


__all__ = ["bp"]
