# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db


class QuestionCategory(db.Model):
    """Question category model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "question_categories"

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    assigned_by_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL")
    )
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    question = db.relationship("Question")
    category = db.relationship("Category", back_populates="question_categories")
    assigned_by_user = db.relationship("User")

    __table_args__ = (
        db.UniqueConstraint(
            "question_id", "category_id", name="uq_question_category_pair"
        ),
        db.Index("idx_question_categories_question_id", "question_id"),
        db.Index("idx_question_categories_category_id", "category_id"),
        db.Index("idx_question_categories_assigned_by", "assigned_by_user_id"),
    )


__all__ = ["QuestionCategory"]
