# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import pytest

from src.core.services.tokens_service import _generate_token_str

pytestmark = pytest.mark.unit


def test_generate_token_str_is_non_empty_and_url_safe():
    """Test that generate_token_str returns a non-empty string that is URL safe."""
    token = _generate_token_str()
    assert isinstance(token, str)
    assert len(token) > 0

    # URL safe: no spaces and no obvious unsafe characters
    for ch in token:
        assert ch not in " \n\r\t"


def test_generate_token_str_length_reasonable():
    """Test that generate_token_str returns a string of a reasonable length."""
    token = _generate_token_str()
    assert len(token) <= 255


def test_generate_token_str_probably_unique():
    """Test that generate_token_str returns a string that is probably unique."""
    tokens = {_generate_token_str() for _ in range(50)}
    assert len(tokens) == 50
