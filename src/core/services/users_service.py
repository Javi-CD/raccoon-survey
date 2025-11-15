# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from werkzeug.security import generate_password_hash

from src.core.database import db
from src.core.models import User


def list_users(active_only: bool = True) -> list[User]:
    """List users, optionally only active.

    Args:
        active_only (bool, optional): Whether to filter active users only. Defaults to True.

    Returns:
        list[User]: A list of User objects.
    """
    q = User.query

    if active_only:
        q = q.filter(User.state.is_(True))

    return q.order_by(User.created_at.desc()).all()


def get_user(user_id: int) -> User | None:
    """Get a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User | None: The User object if found, None if not found.
    """
    return User.query.get(user_id)


def create_user(data: dict) -> User:
    """Create a user.

    Args:
        data (dict): A dictionary containing the user data.

    Returns:
        User: The created User object.
    """
    user = User(
        name=str(data.get("name") or "").strip(),
        email=str(data.get("email") or "").strip().lower(),
        password_hash=generate_password_hash(str(data.get("password") or "")),
        team_id=data.get("team_id"),
        role_id=data.get("role_id"),
    )
    db.session.add(user)
    db.session.commit()

    return user


def update_user(user_id: int, data: dict) -> User | None:
    """Update a user fields.

    Args:
        user_id (int): The ID of the user to update.
        data (dict): A dictionary containing the fields to update.

    Returns:
        User | None: The updated User object if the operation was successful, None if the user was not found.
    """
    user = User.query.get(user_id)
    if not user:
        return None

    for field in ["name", "email", "team_id", "role_id", "state"]:
        if field in data and data[field] is not None:
            value = data[field]

            if field == "email" and isinstance(value, str):
                value = value.strip().lower()

            setattr(user, field, value)

    if data.get("password"):
        user.password_hash = generate_password_hash(str(data["password"]))

    db.session.commit()
    return user


def set_user_state(user_id: int, state: bool) -> User | None:
    """Soft-delete or restore a user by state.

    Args:
        user_id (int): The ID of the user to update.
        state (bool): The desired state of the user (True to restore, False to delete).

    Returns:
        User | None: The updated User object if the operation was successful, None if the user was not found.
    """
    user = User.query.get(user_id)
    if not user:
        return None

    user.state = bool(state)
    db.session.commit()

    return user


__all__ = [
    "create_user",
    "get_user",
    "list_users",
    "set_user_state",
    "update_user",
]
