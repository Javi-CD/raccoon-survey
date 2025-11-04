# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db


class Question(db.Model):
    """Question model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(
        db.Integer, db.ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False
    )
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)

    options = db.Column(db.JSON)
    is_required = db.Column(db.Boolean, default=False)
    order_position = db.Column(db.Integer, default=0)
    state = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    survey = db.relationship("Survey", back_populates="questions")
    responses = db.relationship("Response", back_populates="question")

    __table_args__ = (
        db.Index("idx_questions_survey_id", "survey_id"),
        db.Index("idx_questions_type", "type"),
        db.Index("idx_questions_order", "order_position"),
        db.Index("idx_questions_state", "state"),
    )


__all__ = ["Question"]
