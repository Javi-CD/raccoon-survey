# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from collections.abc import Callable
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required


def role_required(*allowed_roles: str) -> Callable:
    """Enforce JWT auth and role-based access for a view.

    Example:

    .. code-block:: python

        @role_required("admin", "rrhh")
        def view():
            pass

    Args:
        allowed_roles (str): Roles allowed to access the decorated function.

    Returns:
        Callable: The decorated function.
    """

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt() or {}
            role = claims.get("role")

            if role is None:
                return jsonify({"message": "missing role claim"}), 403

            if allowed_roles and role not in allowed_roles:
                return jsonify({"message": "forbidden: insufficient role"}), 403

            return fn(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["role_required"]
