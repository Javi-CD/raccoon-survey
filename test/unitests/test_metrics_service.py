# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import datetime as dt

import pytest

from src.core.services.metrics_service import _start_of_day, _start_of_week

pytestmark = pytest.mark.unit


def test_start_of_day_normalizes_time_to_midnight():
    """Test that start_of_day normalizes the time to midnight."""
    sample = dt.datetime(2024, 3, 15, 14, 30, 45)
    sod = _start_of_day(sample)
    assert sod == dt.datetime(2024, 3, 15)


def test_start_of_week_returns_monday_of_same_week_from_thursday():
    """Test that start_of_week returns the Monday of the same week from a Thursday."""
    thursday = dt.datetime(2024, 3, 14)  # 2024-03-14 is Thursday
    sow = _start_of_week(thursday)
    assert sow.weekday() == 0  # Monday
    assert sow == dt.datetime(2024, 3, 11)


def test_start_of_week_returns_same_day_when_input_is_monday():
    """Test that start_of_week returns the same day when the input is a Monday."""
    monday = dt.datetime(2024, 3, 11, 18, 45)
    sow = _start_of_week(monday)
    assert sow == dt.datetime(2024, 3, 11)
