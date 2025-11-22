# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import datetime as dt

import pytest

from src.core.services.reports_service import _parse_date_range

pytestmark = pytest.mark.unit


def test_parse_date_range_returns_tuple_when_valid_order():
    """Test that parse_date_range returns a tuple when the start date is before the end date."""
    start = dt.date(2024, 1, 10)
    end = dt.date(2024, 1, 20)
    result = _parse_date_range(start, end)
    assert result == (start, end)


def test_parse_date_range_returns_tuple_when_end_after_start():
    """Test that parse_date_range returns a tuple when the end date is after the start date."""
    start = dt.date(2024, 1, 10)
    end = dt.date(2024, 1, 20)
    result = _parse_date_range(start, end)
    assert result == (start, end)


def test_parse_date_range_raises_when_start_after_end():
    """Test that parse_date_range raises a ValueError when the start date is after the end date."""
    start = dt.date(2024, 2, 1)
    end = dt.date(2024, 1, 31)
    with pytest.raises(ValueError):
        _parse_date_range(start, end)
