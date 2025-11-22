# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import pytest
from werkzeug.security import generate_password_hash

from src.core.services.auth_service import build_claims, check_password

pytestmark = pytest.mark.unit


class _Role:
    """Class to represent a user role."""

    def __init__(self, name="admin", state=True):
        """
        Initialize a _Role instance.

        Args:
            name (str, optional): The name of the role. Defaults to "admin".
            state (bool, optional): The state of the role. Defaults to True.
        """
        self.name = name
        self.state = state


class _FakeUser:
    """Class to represent a fake user for testing purposes."""

    def __init__(self, id=1, name="demo", role=None, team_id=None, password_hash=None):
        """
        Initialize a _FakeUser instance.

        Args:
            id (int, optional): The ID of the user. Defaults to 1.
            name (str, optional): The name of the user. Defaults to "demo".
            role (_Role, optional): The role of the user. Defaults to None.
            team_id (int, optional): The ID of the team the user belongs to. Defaults to None.
            password_hash (str, optional): The hashed password of the user. Defaults to None.
        """
        self.id = id
        self.name = name
        self.role = role or _Role()
        self.team_id = team_id
        self.password_hash = password_hash


def test_build_claims_contains_expected_fields():
    """Test that build_claims returns the expected claims for a user."""
    user = _FakeUser(id=42, name="alice", role=_Role(name="editor"), team_id=7)
    claims = build_claims(user)

    assert claims["name"] == "alice"
    assert claims["role"] == "editor"
    assert claims["team_id"] == 7


def test_check_password_validates_correctly():
    """Test that check_password validates passwords correctly."""
    raw = "S3curePassword!"
    user = _FakeUser(password_hash=generate_password_hash(raw))

    assert check_password(user, raw) is True
    assert check_password(user, "wrong") is False
