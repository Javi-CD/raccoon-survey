# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

import csv
import io
import secrets
from collections.abc import Iterable
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from src.core.database import db
from src.core.models import Survey, SurveyToken


def _generate_token_str() -> str:
    """Generate a URL-safe random token string.

    Length varies; ensure it's within VARCHAR(255) limit.

    Returns:
        str: URL-safe random token string
    """

    token = secrets.token_urlsafe(48)  # ~64 chars
    # Ensure max length constraint (255)
    return token[:255]


def _ensure_survey_exists(survey_id: int) -> Survey | None:
    """Check if a survey exists.

    Args:
        survey_id (int): Survey ID

    Returns:
        Survey | None: Survey instance if found, else None
    """
    return db.session.get(Survey, survey_id)


def generate_tokens_for_survey(
    survey_id: int,
    count: int = 1,
    *,
    expires_at: datetime.now(UTC),
    team_id: int | None = None,
    employee_identifiers: Iterable[str] | None = None,
) -> list[SurveyToken]:
    """Generate one-time tokens for a survey.

    - Ensures uniqueness via DB unique constraint with retry on collision.
    - Defaults team_id to survey.team_id if not provided.
    - Optionally attach employee_identifiers (length must match count if provided).

    Args:
        survey_id (int): Survey ID
        expires_at (datetime.now): Expiration datetime
        count (int, optional): Number of tokens to generate. Defaults to 1.
        team_id (int | None, optional): Team ID. Defaults to None.
        employee_identifiers (Iterable[str] | None, optional): Employee identifiers. Defaults to None.

    Raises:
        ValueError: If count is not > 0
        LookupError: If survey_id does not exist
        ValueError: If employee_identifiers length does not match count
        RuntimeError: If failed to generate unique tokens after max retries

    Returns:
        list[SurveyToken]: List of generated SurveyToken instances
    """
    if count <= 0:
        raise ValueError("count must be > 0")

    survey = _ensure_survey_exists(survey_id)
    if survey is None:
        raise LookupError("survey_not_found")

    resolved_team_id = team_id or survey.team_id

    tokens: list[SurveyToken] = []
    identifiers_list: list[str | None] = []

    if employee_identifiers is not None:
        identifiers_list = list(employee_identifiers)
        if len(identifiers_list) != count:
            raise ValueError("employee_identifiers length must match count")
    else:
        identifiers_list = [None] * count

    for i in range(count):
        # Retry on unique token collisions
        retries = 0
        max_retries = 5
        created: SurveyToken | None = None

        while retries < max_retries and created is None:
            token_str = _generate_token_str()
            st = SurveyToken(
                survey_id=survey_id,
                team_id=resolved_team_id,
                token=token_str,
                employee_identifier=identifiers_list[i],
                expires_at=expires_at,
                is_used=False,
            )
            db.session.add(st)
            try:
                db.session.commit()  # persist each token independently
                created = st
            except IntegrityError:
                db.session.rollback()
                retries += 1
                continue

        if created is None:
            raise RuntimeError("failed_to_generate_unique_token")

        tokens.append(created)

    db.session.commit()

    return tokens


def list_tokens(
    survey_id: int,
    *,
    is_used: bool | None = None,
    include_expired: bool = True,
) -> list[dict]:
    """List survey tokens.

    Args:
        survey_id (int): Survey ID
        is_used (bool | None, optional): Filter by used status. Defaults to None.
        include_expired (bool, optional): Include expired tokens. Defaults to True.

    Returns:
        list[dict]: List of token dictionaries
    """
    q = SurveyToken.query.filter_by(survey_id=survey_id)
    if is_used is not None:
        q = q.filter_by(is_used=is_used)
    if not include_expired:
        now = datetime.now(UTC)
        q = q.filter(SurveyToken.expires_at >= now)

    q = q.order_by(SurveyToken.created_at.desc())
    result = [
        {
            "id": t.id,
            "token": t.token,
            "employee_identifier": t.employee_identifier,
            "is_used": t.is_used,
            "used_at": t.used_at.isoformat() if t.used_at else None,
            "expires_at": t.expires_at.isoformat() if t.expires_at else None,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "survey_id": t.survey_id,
            "team_id": t.team_id,
        }
        for t in q.all()
    ]

    return result


def mark_token_used(token_str: str) -> bool:
    """Mark token as used.

    Args:
        token_str (str): Token string

    Returns:
        bool: True if marked as used, False if not found or already used
    """
    t = SurveyToken.query.filter_by(token=token_str).first()
    if t is None:
        return False
    if t.is_used:
        return True

    now = datetime.now(UTC)
    t.is_used = True
    t.used_at = now
    db.session.commit()

    return True


def is_token_valid_for_submission(token_str: str, survey_id: int | None = None) -> bool:
    """Validate token for anonymous submission. Checks not expired and not used.
    Optionally assures it belongs to a given survey_id.

    Args:
        token_str (str): Token string
        survey_id (int | None, optional): Survey ID. Defaults to None.

    Returns:
        bool: True if valid for submission, False otherwise
    """
    now = datetime.now(UTC)
    q = SurveyToken.query.filter_by(token=token_str)
    if survey_id is not None:
        q = q.filter_by(survey_id=survey_id)

    t = q.first()
    if t is None:
        return False
    if t.is_used:
        return False

    return not (t.expires_at and t.expires_at < now)


def export_tokens_csv(
    survey_id: int,
    *,
    is_used: bool | None = None,
    include_expired: bool = True,
) -> str:
    """Export survey tokens to CSV.

    Args:
        survey_id (int): Survey ID
        is_used (bool | None, optional): Filter by used status. Defaults to None.
        include_expired (bool, optional): Include expired tokens. Defaults to True.

    Returns:
        str: CSV string
    """
    rows = list_tokens(survey_id, is_used=is_used, include_expired=include_expired)
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "id",
            "token",
            "employee_identifier",
            "is_used",
            "used_at",
            "expires_at",
            "created_at",
            "survey_id",
            "team_id",
        ],
    )
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

    return output.getvalue()


def cleanup_expired_tokens(
    *,
    survey_id: int | None = None,
    team_id: int | None = None,
    dry_run: bool = False,
    older_than: datetime | None = None,
) -> dict:
    """Clean up expired tokens.

    Args:
        survey_id (int | None): Optional filter by survey.
        team_id (int | None): Optional filter by team.
        dry_run (bool): If True, do not delete; only return the count.
        older_than (datetime | None): Threshold time; defaults to now (UTC).

    Returns:
        dict: {"matched": int, "deleted": int}
    """
    threshold = older_than or datetime.now(UTC)
    q = SurveyToken.query.filter(SurveyToken.expires_at < threshold)

    if survey_id is not None:
        q = q.filter(SurveyToken.survey_id == survey_id)
    if team_id is not None:
        q = q.filter(SurveyToken.team_id == team_id)

    matched = q.count()

    if dry_run:
        return {"matched": matched, "deleted": 0}

    deleted = q.delete(synchronize_session=False)
    db.session.commit()

    return {"matched": matched, "deleted": int(deleted)}
