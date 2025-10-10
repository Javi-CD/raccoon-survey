from __future__ import annotations

from datetime import timedelta

from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash

from src.core.models import User

from . import jwt_blocklist


def build_claims(user: User) -> dict:
    """Builds JWT claims from a user object.

    Args:
        user (User): User object

    Returns:
        dict: JWT claims
    """
    return {
        "role": getattr(getattr(user, "role", None), "name", None),
        "team_id": getattr(user, "team_id", None),
        "name": getattr(user, "name", None),
    }


def verify_user_active_role(user: User) -> bool:
    """Verifies if a user has an active role.

    Args:
        user (User): User object

    Returns:
        bool: True if user has an active role, False otherwise
    """
    role = getattr(user, "role", None)

    return bool(role) and bool(getattr(role, "state", True))


def check_password(user: User, password: str) -> bool:
    """Checks if a password matches the user's password hash.

    Args:
        user (User): User object
        password (str): Password to check

    Returns:
        bool: True if password matches, False otherwise
    """
    return check_password_hash(user.password_hash, password)


def create_tokens(
    user: User, access_expires_seconds: int, refresh_expires_seconds: int
) -> dict:
    """Creates access and refresh tokens for a user.

    Args:
        user (User): User object
        access_expires_seconds (int): Access token expiration time in seconds
        refresh_expires_seconds (int): Refresh token expiration time in seconds

    Returns:
        dict: A dictionary containing access and refresh tokens
    """
    claims = build_claims(user)
    access_expires = timedelta(seconds=int(access_expires_seconds))
    refresh_expires = timedelta(seconds=int(refresh_expires_seconds))

    access_token = create_access_token(
        identity=str(user.id), additional_claims=claims, expires_delta=access_expires
    )
    refresh_token = create_refresh_token(
        identity=str(user.id), additional_claims=claims, expires_delta=refresh_expires
    )

    return {"access_token": access_token, "refresh_token": refresh_token}


def refresh_access_token(
    identity: str, claims: dict, access_expires_seconds: int
) -> dict:
    """Refreshes an access token for a user.

    Args:
        identity (str): User identity
        claims (dict): JWT claims
        access_expires_seconds (int): Access token expiration time in seconds

    Returns:
        dict: A dictionary containing a new access token
    """
    access_expires = timedelta(seconds=int(access_expires_seconds))
    access_token = create_access_token(
        identity=identity, additional_claims=claims, expires_delta=access_expires
    )

    return {"access_token": access_token}


def revoke_token(jti: str | None) -> None:
    """Revokes a JWT token.

    Args:
        jti (str | None): JWT token ID
    """
    if jti:
        jwt_blocklist.revoke_token(jti)


def profile_from_jwt(identity: str | None, jwt_payload: dict) -> dict:
    """Builds a user profile from JWT payload.

    Args:
        identity (str | None): User identity
        jwt_payload (dict): JWT payload

    Returns:
        dict: User profile
    """
    return {
        "id": identity,
        "role": jwt_payload.get("role"),
        "team_id": jwt_payload.get("team_id"),
        "name": jwt_payload.get("name"),
    }


__all__ = [
    "build_claims",
    "check_password",
    "create_tokens",
    "profile_from_jwt",
    "refresh_access_token",
    "revoke_token",
    "verify_user_active_role",
]
