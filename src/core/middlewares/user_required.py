# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from collections.abc import Callable
from functools import wraps

from flask import g, jsonify, request

try:
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
except ImportError:
    verify_jwt_in_request = None
    get_jwt_identity = None

from src.core.models import User


def user_required(
    source: str = "jwt",
    key: str = "user_id",
    field: str = "id",
    attach_to: str = "current_user",
    require_active_role: bool = False,
) -> Callable:
    """Decorator that ensures that the user exists in the database.

    Basic use:
        - From JWT (default):
            @user_required() # read identity from the JWT and validate it
        - From route or query parameter:
            @user_required(source="param", key="user_id")
        - From the JSON body:
            @user_required(source="json", key="user_id")

    Args:
        source (str): Origin of the user identifier. Values: "jwt" | "param" | "json".
        key (str): Name of the key that contains the identifier when `source` is "param" or "json".
        field (str): `User` model field to search for. By default "id". Ex: "email".
        attach_to (str): Name of the attribute in `flask.g` where the found user will be attached.
        require_active_role (bool): If True, also validates that the user's role is active.

    Returns:
        Callable: Decorated function that, if the user exists, continues; Otherwise it responds with an error.
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            lookup_value = None

            if source == "jwt":
                if verify_jwt_in_request is None or get_jwt_identity is None:
                    return jsonify({"message": "JWT support not available"}), 500
                try:
                    # Required JWT (acees_token)
                    verify_jwt_in_request()
                except Exception:
                    return jsonify({"message": "missing or invalid JWT"}), 401

                lookup_value = get_jwt_identity()
                if lookup_value is None:
                    return jsonify({"message": "missing identity in JWT"}), 400

            elif source == "param":
                view_args = request.view_args or {}
                lookup_value = (
                    kwargs.get(key) or view_args.get(key) or request.args.get(key)
                )

                if lookup_value is None:
                    return jsonify({"message": f"{key} is required"}), 400

            elif source == "json":
                data = request.get_json(silent=True) or {}
                lookup_value = data.get(key)

                if lookup_value is None:
                    return jsonify({"message": f"{key} is required"}), 400

            else:
                return jsonify({"message": "invalid source for user lookup"}), 500

            # Normalize and search for the user
            user: User | None = None

            if field == "id":
                try:
                    user_id = int(str(lookup_value))
                except (TypeError, ValueError):
                    return jsonify({"message": f"invalid {key} format"}), 400

                user = User.query.get(user_id)

            elif field == "email":
                email = str(lookup_value).strip().lower()
                user = User.query.filter_by(email=email).first()
            else:
                user = User.query.filter_by(**{field: lookup_value}).first()

            if not user:
                return jsonify({"message": "user not found"}), 404

            if require_active_role and (
                not user.role or getattr(user.role, "state", True) is False
            ):
                return jsonify({"message": "unauthorized"}), 403

            setattr(g, attach_to, user)

            return fn(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["user_required"]
