from __future__ import annotations

from src.core.database import db


class Team(db.Model):
    """Team model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    state = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    users = db.relationship("User", back_populates="team")
    surveys = db.relationship("Survey", back_populates="team")
    survey_tokens = db.relationship("SurveyToken", back_populates="team")


__all__ = ["Team"]
