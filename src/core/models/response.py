from __future__ import annotations

from src.core.database import db


class Response(db.Model):
    """Response model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    survey_token_id = db.Column(
        db.Integer,
        db.ForeignKey("survey_tokens.id", ondelete="CASCADE"),
        nullable=False,
    )
    answer = db.Column(db.Text, nullable=False)
    state = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    question = db.relationship("Question", back_populates="responses")
    survey_token = db.relationship("SurveyToken", back_populates="responses")

    __table_args__ = (
        db.Index("idx_responses_question_id", "question_id"),
        db.Index("idx_responses_survey_token_id", "survey_token_id"),
        db.Index("idx_responses_created_at", "created_at"),
        db.Index("idx_responses_state", "state"),
    )


__all__ = ["Response"]
