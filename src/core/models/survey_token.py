# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db


class SurveyToken(db.Model):
    """Survey token model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "survey_tokens"

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(
        db.Integer, db.ForeignKey("surveys.id", ondelete="CASCADE"), nullable=False
    )
    team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id", ondelete="CASCADE"), nullable=False
    )
    token = db.Column(db.String(255), nullable=False, unique=True)
    employee_identifier = db.Column(db.String(100))
    is_used = db.Column(db.Boolean, default=False)
    used_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    survey = db.relationship("Survey", back_populates="tokens")
    team = db.relationship("Team", back_populates="survey_tokens")
    responses = db.relationship("Response", back_populates="survey_token")

    __table_args__ = (
        db.Index("idx_survey_tokens_token", "token"),
        db.Index("idx_survey_tokens_survey_id", "survey_id"),
        db.Index("idx_survey_tokens_team_id", "team_id"),
        db.Index("idx_survey_tokens_expires_at", "expires_at"),
        db.Index("idx_survey_tokens_is_used", "is_used"),
    )


__all__ = ["SurveyToken"]
