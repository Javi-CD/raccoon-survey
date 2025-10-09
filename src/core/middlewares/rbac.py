from __future__ import annotations

from collections.abc import Callable
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required


def role_required(*allowed_roles: str) -> Callable:
    """Decorator that enforces JWT auth and role-based access.

    Usage:
        @role_required("admin", "rrhh")
        def view():
            ...

    Args:
        allowed_roles (str): A list of roles that are allowed to access the decorated function.

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
