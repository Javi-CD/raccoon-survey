# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

"""add audit/categories/question_categories

Revision ID: 5dfb7cd4abc5
Revises: 31cd4e25f1e6
Create Date: 2025-10-07 11:16:19.023049

"""

from collections.abc import Sequence  # noqa: I001

import sqlalchemy as sa
from alembic import op

from src.core.models import (
    AuditLog,
    Category,
    Question,
    QuestionCategory,
    User,
)

# Resolve table names from model __tablename__
CATEGORY_TBL = Category.__tablename__
AUDIT_LOG_TBL = AuditLog.__tablename__
QUESTION_CATEGORY_TBL = QuestionCategory.__tablename__
QUESTION_TBL = Question.__tablename__
USER_TBL = User.__tablename__

# revision identifiers, used by Alembic.
revision: str = "5dfb7cd4abc5"
down_revision: str | Sequence[str] | None = "31cd4e25f1e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        CATEGORY_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("state", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("idx_categories_name", CATEGORY_TBL, ["name"], unique=False)
    op.create_index("idx_categories_state", CATEGORY_TBL, ["state"], unique=False)

    op.create_table(
        AUDIT_LOG_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("entity_type", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(length=50), nullable=False),
        sa.Column("changed_by_user_id", sa.Integer(), nullable=True),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("previous_data", sa.JSON(), nullable=True),
        sa.Column("new_data", sa.JSON(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column(
            "triggered_by",
            sa.String(length=20),
            server_default="manual",
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.CheckConstraint(
            "action IN ('create','update','delete','soft_delete','restore','login','logout','assign_role','generate_tokens')",
            name="ck_audit_logs_action",
        ),
        sa.CheckConstraint(
            "triggered_by IN ('manual','system')", name="ck_audit_logs_triggered"
        ),
        sa.ForeignKeyConstraint(
            ["changed_by_user_id"], [f"{USER_TBL}.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_audit_action", AUDIT_LOG_TBL, ["action"], unique=False)
    op.create_index(
        "idx_audit_changed_by", AUDIT_LOG_TBL, ["changed_by_user_id"], unique=False
    )
    op.create_index("idx_audit_created_at", AUDIT_LOG_TBL, ["created_at"], unique=False)
    op.create_index(
        "idx_audit_entity", AUDIT_LOG_TBL, ["entity_type", "entity_id"], unique=False
    )
    op.create_index(
        "idx_audit_triggered_by", AUDIT_LOG_TBL, ["triggered_by"], unique=False
    )

    op.create_table(
        QUESTION_CATEGORY_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("assigned_by_user_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["assigned_by_user_id"], [f"{USER_TBL}.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["category_id"], [f"{CATEGORY_TBL}.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["question_id"], [f"{QUESTION_TBL}.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "question_id", "category_id", name="uq_question_category_pair"
        ),
    )
    op.create_index(
        "idx_question_categories_assigned_by",
        QUESTION_CATEGORY_TBL,
        ["assigned_by_user_id"],
        unique=False,
    )
    op.create_index(
        "idx_question_categories_category_id",
        QUESTION_CATEGORY_TBL,
        ["category_id"],
        unique=False,
    )
    op.create_index(
        "idx_question_categories_question_id",
        QUESTION_CATEGORY_TBL,
        ["question_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "idx_question_categories_question_id", table_name=QUESTION_CATEGORY_TBL
    )
    op.drop_index(
        "idx_question_categories_category_id", table_name=QUESTION_CATEGORY_TBL
    )
    op.drop_index(
        "idx_question_categories_assigned_by", table_name=QUESTION_CATEGORY_TBL
    )
    op.drop_table(QUESTION_CATEGORY_TBL)

    op.drop_index("idx_audit_triggered_by", table_name=AUDIT_LOG_TBL)
    op.drop_index("idx_audit_entity", table_name=AUDIT_LOG_TBL)
    op.drop_index("idx_audit_created_at", table_name=AUDIT_LOG_TBL)
    op.drop_index("idx_audit_changed_by", table_name=AUDIT_LOG_TBL)
    op.drop_index("idx_audit_action", table_name=AUDIT_LOG_TBL)
    op.drop_table(AUDIT_LOG_TBL)

    op.drop_index("idx_categories_state", table_name=CATEGORY_TBL)
    op.drop_index("idx_categories_name", table_name=CATEGORY_TBL)
    op.drop_table(CATEGORY_TBL)
