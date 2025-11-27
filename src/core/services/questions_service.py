# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db
from src.core.models import Question


def list_questions(survey_id: int | None = None) -> list[Question]:
    """List questions.

    Args:
        survey_id (int | None, optional): Survey ID. Defaults to None.

    Returns:
        list[Question]: List of questions.
    """
    query = Question.query
    if survey_id is not None:
        query = query.filter(Question.survey_id == survey_id)

    return query.order_by(Question.order_position.asc()).all()


def create_question(data: dict) -> Question:
    """Create question.

    Args:
        data (dict): Data to create question.

    Returns:
        Question: Created question.
    """
    question = Question(
        survey_id=data.get("survey_id"),
        text=data.get("text"),
        type=data.get("type"),
        options=data.get("options"),
        is_required=bool(data.get("is_required", False)),
        order_position=data.get("order_position", 0),
    )
    db.session.add(question)
    db.session.commit()

    return question


def get_question(question_id: int) -> Question | None:
    """Get question by ID.

    Args:
        question_id (int): Question ID.

    Returns:
        Question | None: Question or None if not found.
    """
    return db.session.get(Question, question_id)


def update_question(question_id: int, data: dict) -> Question | None:
    """Update question.

    Args:
        question_id (int): Question ID.
        data (dict): Data to update question.

    Returns:
        Question | None: Updated question or None if not found.
    """
    question = db.session.get(Question, question_id)
    if not question:
        return None

    for field in [
        "survey_id",
        "text",
        "type",
        "options",
        "is_required",
        "order_position",
        "state",
    ]:
        if field in data:
            setattr(question, field, data[field])

    db.session.commit()

    return question


def set_question_state(question_id: int, state: bool) -> Question | None:
    """Set question state.

    Args:
        question_id (int): Question ID.
        state (bool): State to set.

    Returns:
        Question | None: Updated question or None if not found.
    """
    question = db.session.get(Question, question_id)
    if not question:
        return None

    question.state = bool(state)
    db.session.commit()

    return question


__all__ = [
    "create_question",
    "get_question",
    "list_questions",
    "set_question_state",
    "update_question",
]
