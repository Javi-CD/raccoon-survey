# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import os
import pathlib
import random
import string
import sys

import pytest


@pytest.fixture(scope="session")
def random_string_factory():
    """Fixture to generate random strings.

    Returns:
        function: A function that generates random strings of a specified length.
    """

    def _make(length=12):
        chars = string.ascii_letters + string.digits
        return "".join(random.SystemRandom().choice(chars) for _ in range(length))

    return _make


@pytest.fixture(scope="session")
def env_cleanup():
    """Fixture to clean up environment variables after tests.

    Yields:
        None
    """
    original = dict[str, str](os.environ)
    yield

    # Restore environment variables after tests
    os.environ.clear()
    os.environ.update(original)


# Ensure project root and 'src' are importable
ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
