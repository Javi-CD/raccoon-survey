# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

import csv
import io
from collections import defaultdict
from datetime import datetime
from typing import Any

from src.core.database import db
from src.core.models import Question, Response, Survey, SurveyToken, Team


def _parse_date_range(
    date_from: datetime | None, date_to: datetime | None
) -> tuple[datetime | None, datetime | None]:
    """Validate date range.

    Args:
        date_from (datetime | None): Start of the date range.
        date_to (datetime | None): End of the date range.

    Raises:
        ValueError: If date_from is after date_to.

    Returns:
        tuple[datetime | None, datetime | None]: Validated date range.
    """
    if date_from and date_to and date_from > date_to:
        raise ValueError("invalid_date_range")

    return date_from, date_to


def _base_query_for_survey(
    survey_id: int,
    *,
    team_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    """Base query for survey responses.

    Args:
        survey_id (int): ID of the survey.
        team_id (int | None, optional): ID of the team. Defaults to None.
        date_from (datetime | None, optional): Start of the date range. Defaults to None.
        date_to (datetime | None, optional): End of the date range. Defaults to None.

    Returns:
        Query: Base query for survey responses.
    """
    q = (
        db.session.query(Response, Question, SurveyToken)
        .join(Response.question)
        .join(Response.survey_token)
        .filter(SurveyToken.survey_id == survey_id)
        .filter(Response.state.is_(True))
        .filter(Question.state.is_(True))
    )
    if team_id is not None:
        q = q.filter(SurveyToken.team_id == team_id)
    if date_from is not None:
        q = q.filter(Response.created_at >= date_from)
    if date_to is not None:
        q = q.filter(Response.created_at <= date_to)

    return q


def _base_query_for_team(
    team_id: int,
    *,
    survey_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    """Base query for team responses.

    Args:
        team_id (int): ID of the team.
        survey_id (int | None, optional): ID of the survey. Defaults to None.
        date_from (datetime | None, optional): Start of the date range. Defaults to None.
        date_to (datetime | None, optional): End of the date range. Defaults to None.

    Returns:
        Query: Base query for team responses.
    """
    q = (
        db.session.query(Response, Question, SurveyToken)
        .join(Response.question)
        .join(Response.survey_token)
        .filter(SurveyToken.team_id == team_id)
        .filter(Response.state.is_(True))
        .filter(Question.state.is_(True))
    )
    if survey_id is not None:
        q = q.filter(SurveyToken.survey_id == survey_id)
    if date_from is not None:
        q = q.filter(Response.created_at >= date_from)
    if date_to is not None:
        q = q.filter(Response.created_at <= date_to)

    return q


def _aggregate_rows(
    rows: list[tuple[Response, Question, SurveyToken]],
) -> dict[int, dict[str, Any]]:
    """Aggregate responses per question, counting answers.

    Args:
        rows (list[tuple[Response, Question, SurveyToken]]): List of response rows.

    Returns:
        dict[int, dict[str, Any]]: Aggregated data per question.
    """
    agg: dict[int, dict[str, Any]] = {}
    for resp, question, _token in rows:
        entry = agg.setdefault(
            question.id,
            {
                "question": question,
                "total": 0,
                "answers": defaultdict(int),
            },
        )
        entry["total"] += 1
        entry["answers"][resp.answer] += 1

    return agg


def _format_summary(
    *,
    survey_id: int | None,
    team_id: int | None,
    date_from: datetime | None,
    date_to: datetime | None,
    agg: dict[int, dict[str, Any]],
) -> dict:
    """Format aggregated data into a summary.

    Args:
        survey_id (int | None): ID of the survey.
        team_id (int | None): ID of the team.
        date_from (datetime | None): Start of the date range.
        date_to (datetime | None): End of the date range.
        agg (dict[int, dict[str, Any]]): Aggregated data per question.

    Returns:
        dict: Formatted summary.
    """
    questions_summary = []
    for _qid, data in sorted(agg.items(), key=lambda x: x[0]):
        q: Question = data["question"]
        answers_list = [
            {"value": val, "count": cnt} for val, cnt in sorted(data["answers"].items())
        ]

        questions_summary.append(
            {
                "id": q.id,
                "text": q.text,
                "type": q.type,
                "total": data["total"],
                "answers": answers_list,
            }
        )

    return {
        "survey_id": survey_id,
        "team_id": team_id,
        "date_from": date_from.isoformat() if date_from else None,
        "date_to": date_to.isoformat() if date_to else None,
        "questions": questions_summary,
    }


def get_survey_summary(
    survey_id: int,
    *,
    team_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict:
    """Aggregate responses for a survey, optionally filtered by team and date range.

    Args:
        survey_id (int): ID of the survey.
        team_id (int | None, optional): ID of the team. Defaults to None.
        date_from (datetime | None, optional): Start of the date range. Defaults to None.
        date_to (datetime | None, optional): End of the date range. Defaults to None.

    Returns:
        dict: Formatted summary.
    """
    if Survey.query.get(survey_id) is None:
        raise LookupError("survey_not_found")
    if team_id is not None and Team.query.get(team_id) is None:
        raise LookupError("team_not_found")

    date_from, date_to = _parse_date_range(date_from, date_to)
    q = _base_query_for_survey(
        survey_id, team_id=team_id, date_from=date_from, date_to=date_to
    )
    rows = q.all()
    agg = _aggregate_rows(rows)

    return _format_summary(
        survey_id=survey_id,
        team_id=team_id,
        date_from=date_from,
        date_to=date_to,
        agg=agg,
    )


def get_team_summary(
    team_id: int,
    *,
    survey_id: int | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
) -> dict:
    """Aggregate responses for a team, optionally filtered by survey and date range.

    Args:
        team_id (int): ID of the team.
        survey_id (int | None, optional): ID of the survey. Defaults to None.
        date_from (datetime | None, optional): Start of the date range. Defaults to None.
        date_to (datetime | None, optional): End of the date range. Defaults to None.

    Returns:
        dict: Formatted summary.
    """
    if Team.query.get(team_id) is None:
        raise LookupError("team_not_found")
    if survey_id is not None and Survey.query.get(survey_id) is None:
        raise LookupError("survey_not_found")

    date_from, date_to = _parse_date_range(date_from, date_to)
    q = _base_query_for_team(
        team_id, survey_id=survey_id, date_from=date_from, date_to=date_to
    )
    rows = q.all()
    agg = _aggregate_rows(rows)

    return _format_summary(
        survey_id=survey_id,
        team_id=team_id,
        date_from=date_from,
        date_to=date_to,
        agg=agg,
    )


def export_summary_csv(
    *,
    summary: dict,
) -> str:
    """Export a summary dict to CSV with rows per answer value.

    Args:
        summary (dict): Formatted summary.

    Returns:
        str: CSV content.
    """
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "survey_id",
            "team_id",
            "question_id",
            "question_text",
            "question_type",
            "answer_value",
            "count",
            "total",
            "date_from",
            "date_to",
        ],
    )

    writer.writeheader()
    for q in summary.get("questions", []):
        for a in q.get("answers", []):
            writer.writerow(
                {
                    "survey_id": summary.get("survey_id"),
                    "team_id": summary.get("team_id"),
                    "question_id": q.get("id"),
                    "question_text": q.get("text"),
                    "question_type": q.get("type"),
                    "answer_value": a.get("value"),
                    "count": a.get("count"),
                    "total": q.get("total"),
                    "date_from": summary.get("date_from"),
                    "date_to": summary.get("date_to"),
                }
            )

    return output.getvalue()


__all__ = [
    "export_summary_csv",
    "get_survey_summary",
    "get_team_summary",
]
