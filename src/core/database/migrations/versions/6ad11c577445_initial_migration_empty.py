# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

"""initial_migration_empty

Revision ID: 6ad11c577445
Revises:
Create Date: 2025-10-02 16:09:20.408061

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "6ad11c577445"
down_revision: str | Sequence[str] | None | None = None
branch_labels: str | Sequence[str] | None | None = None
depends_on: str | Sequence[str] | None | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
