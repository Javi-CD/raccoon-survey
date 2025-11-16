# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db
from src.core.models import Role


def list_roles(active_only: bool = True) -> list[Role]:
    """List all roles.

    Args:
        active_only (bool, optional): Whether to filter active roles only. Defaults to True.

    Returns:
        list[Role]: A list of Role objects.
    """
    q = Role.query

    if active_only:
        q = q.filter(Role.state.is_(True))

    return q.order_by(Role.name.asc()).all()


def get_role(role_id: int) -> Role | None:
    """Get a role by ID.

    Args:
        role_id (int): Role ID.

    Returns:
        Role | None: Role if found, otherwise None.
    """
    return Role.query.get(role_id)


def create_role(data: dict) -> Role:
    """Create a role.

    Args:
        data (dict): Data to create role.

    Returns:
        Role: Created role.
    """
    role = Role(
        name=str(data.get("name") or "").strip(),
        description=data.get("description"),
    )
    db.session.add(role)
    db.session.commit()

    return role


def update_role(role_id: int, data: dict) -> Role | None:
    """Update a role.

    Args:
        role_id (int): Role ID.
        data (dict): Fields to update.

    Returns:
        Role | None: Updated role, or None if not found.
    """
    role = Role.query.get(role_id)
    if not role:
        return None

    for field in ["name", "description", "state"]:
        if field in data and data[field] is not None:
            value = data[field]

            if field == "name" and isinstance(value, str):
                value = value.strip()

            setattr(role, field, value)

    db.session.commit()

    return role


def set_role_state(role_id: int, state: bool) -> Role | None:
    """Soft-delete or restore a role by state.

    Args:
        role_id (int): Role ID.
        state (bool): Desired state (True to restore, False to delete).

    Returns:
        Role | None: Updated role, or None if not found.
    """
    role = Role.query.get(role_id)
    if not role:
        return None

    role.state = bool(state)
    db.session.commit()

    return role


__all__ = [
    "create_role",
    "get_role",
    "list_roles",
    "set_role_state",
    "update_role",
]
