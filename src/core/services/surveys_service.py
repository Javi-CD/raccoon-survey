# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from datetime import UTC, datetime

from src.core.database import db
from src.core.models import Survey


def list_surveys(team_id: int | None = None) -> list[Survey]:
    """List surveys.

    Args:
        team_id (int | None, optional): Team ID. Defaults to None.

    Returns:
        list[Survey]: List of surveys.
    """
    query = Survey.query
    if team_id is not None:
        query = query.filter(Survey.team_id == team_id)  # pyright: ignore[reportGeneralTypeIssues]

    return query.order_by(Survey.created_at.desc()).all()


def create_survey(data: dict) -> Survey:
    """Create survey.

    Args:
        data (dict): Data to create survey.

    Returns:
        Survey: Created survey.
    """
    survey = Survey(
        team_id=data.get("team_id"),  # pyright: ignore[reportCallIssue]
        created_by_user_id=data.get("created_by_user_id"),  # pyright: ignore[reportCallIssue]
        title=data.get("title"),  # pyright: ignore[reportCallIssue]
        description=data.get("description"),  # pyright: ignore[reportCallIssue]
        is_anonymous=bool(data.get("is_anonymous", True)),  # pyright: ignore[reportCallIssue]
        expires_at=data.get("expires_at"),  # pyright: ignore[reportCallIssue]
    )
    db.session.add(survey)
    db.session.commit()

    return survey


def get_survey(survey_id: int) -> Survey | None:
    """Get survey by ID.

    Args:
        survey_id (int): Survey ID.

    Returns:
        Survey | None: Survey or None if not found.
    """
    return Survey.query.get(survey_id)


def update_survey(survey_id: int, data: dict) -> Survey | None:
    """Update survey.

    Args:
        survey_id (int): Survey ID.
        data (dict): Data to update survey.

    Returns:
        Survey | None: Updated survey or None if not found.
    """
    survey = Survey.query.get(survey_id)
    if not survey:
        return None

    for field in [
        "title",
        "description",
        "is_anonymous",
        "team_id",
        "created_by_user_id",
        "expires_at",
        "state",
    ]:
        if field in data:
            setattr(survey, field, data[field])

    db.session.commit()

    return survey


def set_survey_state(survey_id: int, state: bool) -> Survey | None:
    """Set survey state.

    Args:
        survey_id (int): Survey ID.
        state (bool): State to set.

    Returns:
        Survey | None: Updated survey or None if not found.
    """
    survey = Survey.query.get(survey_id)
    if not survey:
        return None

    survey.state = bool(state)
    db.session.commit()

    return survey


def deactivate_expired_surveys(now: datetime | None = None) -> dict:
    """Set state=False for surveys whose expires_at is in the past.

    Args:
        now (datetime | None): Reference datetime (UTC). Defaults to current UTC.

    Returns:
        dict: {"matched": int, "updated": int}
    """
    ref = now or datetime.now(UTC)
    q = (
        Survey.query.filter(Survey.state.is_(True))
        .filter(Survey.expires_at.isnot(None))
        .filter(Survey.expires_at < ref)
    )
    matched = q.count()
    updated = q.update({Survey.state: False}, synchronize_session=False)
    db.session.commit()

    return {"matched": int(matched), "updated": int(updated)}


__all__ = [
    "create_survey",
    "deactivate_expired_surveys",
    "get_survey",
    "list_surveys",
    "set_survey_state",
    "update_survey",
]
