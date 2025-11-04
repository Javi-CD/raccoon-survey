# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

# NOTE: This is a simple in-memory blocklist.
# TODO: Use a database to store the revoked tokens.
REVOKED_TOKENS: set[str] = set()


def revoke_token(jti: str | None) -> None:
    """Adds a JWT token to the blocklist.

    Args:
        jti (str | None): The JWT token identifier to be revoked.
    """
    if jti:
        REVOKED_TOKENS.add(jti)


def is_token_revoked(jti: str | None) -> bool:
    """Checks if a JWT token is revoked.

    Args:
        jti (str | None): The JWT token identifier to check.

    Returns:
        bool: True if the token is revoked, False otherwise.
    """
    return bool(jti) and jti in REVOKED_TOKENS


__all__ = ["is_token_revoked", "revoke_token"]
