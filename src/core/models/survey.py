# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db


class Survey(db.Model):
    """Survey model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "surveys"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete="CASCADE"))
    created_by_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL")
    )
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=True)
    state = db.Column(db.Boolean, default=True)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    team = db.relationship("Team", back_populates="surveys")
    created_by_user = db.relationship("User", back_populates="created_surveys")
    questions = db.relationship("Question", back_populates="survey")
    tokens = db.relationship("SurveyToken", back_populates="survey")

    __table_args__ = (
        db.Index("idx_surveys_team_id", "team_id"),
        db.Index("idx_surveys_created_by", "created_by_user_id"),
        db.Index("idx_surveys_created_at", "created_at"),
        db.Index("idx_surveys_expires_at", "expires_at"),
        db.Index("idx_surveys_state", "state"),
    )


__all__ = ["Survey"]
