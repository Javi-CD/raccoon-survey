# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

"""create core tables

Revision ID: 31cd4e25f1e6
Revises: 6ad11c577445
Create Date: 2025-10-06 14:59:31.694987

"""

from collections.abc import Sequence  # noqa: I001

import sqlalchemy as sa
from alembic import op

from src.core.models import (
    Question,
    Response,
    Role,
    Survey,
    SurveyToken,
    Team,
    User,
)

# Table names sourced from model __tablename__ definitions
ROLE_TBL = Role.__tablename__
TEAM_TBL = Team.__tablename__
USER_TBL = User.__tablename__
SURVEY_TBL = Survey.__tablename__
QUESTION_TBL = Question.__tablename__
SURVEY_TOKEN_TBL = SurveyToken.__tablename__
RESPONSE_TBL = Response.__tablename__

# revision identifiers, used by Alembic.
revision: str = "31cd4e25f1e6"
down_revision: str | Sequence[str] | None = "6ad11c577445"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        ROLE_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=50), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("state", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index("idx_roles_name", ROLE_TBL, ["name"], unique=False)
    op.create_index("idx_roles_state", ROLE_TBL, ["state"], unique=False)

    op.create_table(
        TEAM_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("state", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        USER_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("state", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["role_id"], [f"{ROLE_TBL}.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["team_id"], [f"{TEAM_TBL}.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("idx_users_email", USER_TBL, ["email"], unique=False)
    op.create_index("idx_users_role_id", USER_TBL, ["role_id"], unique=False)
    op.create_index("idx_users_state", USER_TBL, ["state"], unique=False)
    op.create_index("idx_users_team_id", USER_TBL, ["team_id"], unique=False)

    op.create_table(
        SURVEY_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_anonymous", sa.Boolean(), nullable=True),
        sa.Column("state", sa.Boolean(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"], [f"{USER_TBL}.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(["team_id"], [f"{TEAM_TBL}.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_surveys_created_at", SURVEY_TBL, ["created_at"], unique=False)
    op.create_index(
        "idx_surveys_created_by", SURVEY_TBL, ["created_by_user_id"], unique=False
    )
    op.create_index("idx_surveys_expires_at", SURVEY_TBL, ["expires_at"], unique=False)
    op.create_index("idx_surveys_state", SURVEY_TBL, ["state"], unique=False)
    op.create_index("idx_surveys_team_id", SURVEY_TBL, ["team_id"], unique=False)

    op.create_table(
        QUESTION_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("survey_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("is_required", sa.Boolean(), nullable=True),
        sa.Column("order_position", sa.Integer(), nullable=True),
        sa.Column("state", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["survey_id"], [f"{SURVEY_TBL}.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_questions_order", QUESTION_TBL, ["order_position"], unique=False
    )
    op.create_index("idx_questions_state", QUESTION_TBL, ["state"], unique=False)
    op.create_index(
        "idx_questions_survey_id", QUESTION_TBL, ["survey_id"], unique=False
    )
    op.create_index("idx_questions_type", QUESTION_TBL, ["type"], unique=False)

    op.create_table(
        SURVEY_TOKEN_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("survey_id", sa.Integer(), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("employee_identifier", sa.String(length=100), nullable=True),
        sa.Column("is_used", sa.Boolean(), nullable=True),
        sa.Column("used_at", sa.DateTime(), nullable=True),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["survey_id"], [f"{SURVEY_TBL}.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["team_id"], [f"{TEAM_TBL}.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(
        "idx_survey_tokens_expires_at", SURVEY_TOKEN_TBL, ["expires_at"], unique=False
    )
    op.create_index(
        "idx_survey_tokens_is_used", SURVEY_TOKEN_TBL, ["is_used"], unique=False
    )
    op.create_index(
        "idx_survey_tokens_survey_id", SURVEY_TOKEN_TBL, ["survey_id"], unique=False
    )
    op.create_index(
        "idx_survey_tokens_team_id", SURVEY_TOKEN_TBL, ["team_id"], unique=False
    )
    op.create_index(
        "idx_survey_tokens_token", SURVEY_TOKEN_TBL, ["token"], unique=False
    )

    op.create_table(
        RESPONSE_TBL,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("survey_token_id", sa.Integer(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=False),
        sa.Column("state", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("(CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["question_id"], [f"{QUESTION_TBL}.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["survey_token_id"], [f"{SURVEY_TOKEN_TBL}.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_responses_created_at", RESPONSE_TBL, ["created_at"], unique=False
    )
    op.create_index(
        "idx_responses_question_id", RESPONSE_TBL, ["question_id"], unique=False
    )
    op.create_index("idx_responses_state", RESPONSE_TBL, ["state"], unique=False)
    op.create_index(
        "idx_responses_survey_token_id", RESPONSE_TBL, ["survey_token_id"], unique=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index("idx_responses_survey_token_id", table_name=RESPONSE_TBL)
    op.drop_index("idx_responses_state", table_name=RESPONSE_TBL)
    op.drop_index("idx_responses_question_id", table_name=RESPONSE_TBL)
    op.drop_index("idx_responses_created_at", table_name=RESPONSE_TBL)
    op.drop_table(RESPONSE_TBL)

    op.drop_index("idx_survey_tokens_token", table_name=SURVEY_TOKEN_TBL)
    op.drop_index("idx_survey_tokens_team_id", table_name=SURVEY_TOKEN_TBL)
    op.drop_index("idx_survey_tokens_survey_id", table_name=SURVEY_TOKEN_TBL)
    op.drop_index("idx_survey_tokens_is_used", table_name=SURVEY_TOKEN_TBL)
    op.drop_index("idx_survey_tokens_expires_at", table_name=SURVEY_TOKEN_TBL)
    op.drop_table(SURVEY_TOKEN_TBL)

    op.drop_index("idx_questions_type", table_name=QUESTION_TBL)
    op.drop_index("idx_questions_survey_id", table_name=QUESTION_TBL)
    op.drop_index("idx_questions_state", table_name=QUESTION_TBL)
    op.drop_index("idx_questions_order", table_name=QUESTION_TBL)
    op.drop_table(QUESTION_TBL)

    op.drop_index("idx_surveys_team_id", table_name=SURVEY_TBL)
    op.drop_index("idx_surveys_state", table_name=SURVEY_TBL)
    op.drop_index("idx_surveys_expires_at", table_name=SURVEY_TBL)
    op.drop_index("idx_surveys_created_by", table_name=SURVEY_TBL)
    op.drop_index("idx_surveys_created_at", table_name=SURVEY_TBL)
    op.drop_table(SURVEY_TBL)

    op.drop_index("idx_users_team_id", table_name=USER_TBL)
    op.drop_index("idx_users_state", table_name=USER_TBL)
    op.drop_index("idx_users_role_id", table_name=USER_TBL)
    op.drop_index("idx_users_email", table_name=USER_TBL)
    op.drop_table(USER_TBL)

    op.drop_table(TEAM_TBL)

    op.drop_index("idx_roles_state", table_name=ROLE_TBL)
    op.drop_index("idx_roles_name", table_name=ROLE_TBL)
    op.drop_table(ROLE_TBL)
