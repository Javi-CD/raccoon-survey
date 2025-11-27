# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import pytest

from src.core.services.jwt_blocklist import is_token_revoked, revoke_token

pytestmark = pytest.mark.unit


def test_is_token_revoked_false_when_not_revoked():
    """Test that is_token_revoked returns False when the token is not revoked."""
    assert is_token_revoked("abc123") is False


def test_revoke_token_marks_token_as_revoked():
    """Test that revoke_token marks a token as revoked."""
    jti = "token-001"
    revoke_token(jti)
    assert is_token_revoked(jti) is True


def test_revoke_token_ignores_none_jti():
    """Test that revoke_token ignores None as the JTI."""
    revoke_token(None)
    # Ensure no error and typical token remains not revoked
    assert is_token_revoked("random") is False
