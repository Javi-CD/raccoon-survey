# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import func

from src.core.database import db
from src.core.models import Response, Survey, SurveyToken, User


def _start_of_day(dt: datetime) -> datetime:
    """Return the start of the day for the given datetime.

    Args:
        dt (datetime): Datetime to get the start of the day for.

    Returns:
        datetime: Start of the day for the given datetime.
    """
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)


def _start_of_week(dt: datetime) -> datetime:
    """Return the start of the week for the given datetime.

    Args:
        dt (datetime): Datetime to get the start of the week for.

    Returns:
        datetime: Start of the week for the given datetime.
    """
    return _start_of_day(dt - timedelta(days=dt.weekday()))


def _get_cards_metrics(today: datetime) -> dict[str, int]:
    """Compute cards metrics for dashboard.

    Args:
        today (datetime): Date to compute metrics for.

    Returns:
        dict[str, int]: Dictionary with keys: total_surveys, active_users, responses_today, reports_generated
    """
    total_surveys_active = (
        db.session.query(func.count(Survey.id)).filter(Survey.state.is_(True)).scalar()
    ) or 0
    active_users = (
        db.session.query(func.count(User.id)).filter(User.state.is_(True)).scalar()
    ) or 0
    responses_today = (
        db.session.query(func.count(Response.id))
        .filter(Response.state.is_(True))
        .filter(Response.created_at >= today)
        .scalar()
    ) or 0
    reports_generated = (
        db.session.query(func.count(func.distinct(SurveyToken.survey_id)))
        .join(Response, Response.survey_token_id == SurveyToken.id)
        .filter(Response.state.is_(True))
        .scalar()
    ) or 0

    return {
        "total_surveys": int(total_surveys_active),
        "active_users": int(active_users),
        "responses_today": int(responses_today),
        "reports_generated": int(reports_generated),
    }


def _get_responses_by_week(week_start: datetime) -> tuple[list[str], list[int]]:
    """Compute responses by day for current week (Mon..Sun).

    Args:
        week_start (datetime): Start of the week to compute metrics for.

    Returns:
        tuple[list[str], list[int]]: Tuple with day labels and responses count for each day.
    """
    counts_by_day: dict[int, int] = defaultdict[int, int](int)
    day_labels = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

    for i in range(7):
        day_start = week_start + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        count = (
            db.session.query(func.count(Response.id))
            .filter(Response.state.is_(True))
            .filter(Response.created_at >= day_start)
            .filter(Response.created_at < day_end)
            .scalar()
        ) or 0
        counts_by_day[i] = count

    responses_by_week_data = [counts_by_day[i] for i in range(7)]

    return day_labels, responses_by_week_data


def _get_surveys_distribution(now: datetime) -> tuple[list[str], list[int]]:
    """Compute distribution of surveys: Active, Inactive, Expired.

    Args:
        now (datetime): Date to compute metrics for.

    Returns:
        tuple[list[str], list[int]]: Tuple with survey state labels and count for each state.
    """
    expired_active = (
        db.session.query(func.count(Survey.id))
        .filter(Survey.state.is_(True))
        .filter(Survey.expires_at.isnot(None))
        .filter(Survey.expires_at < now)
        .scalar()
    ) or 0
    active_vigentes = (
        db.session.query(func.count(Survey.id))
        .filter(Survey.state.is_(True))
        .filter((Survey.expires_at.is_(None)) | (Survey.expires_at >= now))
        .scalar()
    ) or 0
    inactive = (
        db.session.query(func.count(Survey.id)).filter(Survey.state.is_(False)).scalar()
    ) or 0

    return ["Activas", "Inactivas", "Expiradas"], [
        int(active_vigentes),
        int(inactive),
        int(expired_active),
    ]


def get_dashboard_metrics() -> dict[str, Any]:
    """Return aggregated metrics for the admin dashboard.

    Returns:
        dict[str, Any]: Dictionary with keys: cards, charts.
    """
    now = datetime.now()
    today = _start_of_day(now)
    week_start = _start_of_week(now)

    cards = _get_cards_metrics(today)
    week_labels, week_data = _get_responses_by_week(week_start)
    dist_labels, dist_data = _get_surveys_distribution(now)

    return {
        "cards": cards,
        "charts": {
            "responses_by_week": {
                "labels": week_labels,
                "data": week_data,
            },
            "surveys_distribution": {
                "labels": dist_labels,
                "data": dist_data,
            },
        },
    }
