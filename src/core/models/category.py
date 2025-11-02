from __future__ import annotations

from src.core.database import db


class Category(db.Model):
    """Category model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    state = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    question_categories = db.relationship("QuestionCategory", back_populates="category")

    __table_args__ = (
        db.Index("idx_categories_name", "name"),
        db.Index("idx_categories_state", "state"),
    )


__all__ = ["Category"]
