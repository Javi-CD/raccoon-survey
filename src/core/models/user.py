# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db


class User(db.Model):
    """User model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id", ondelete="SET NULL"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id", ondelete="SET NULL"))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    team = db.relationship("Team", back_populates="users")
    role = db.relationship("Role", back_populates="users")
    created_surveys = db.relationship("Survey", back_populates="created_by_user")

    __table_args__ = (
        db.Index("idx_users_team_id", "team_id"),
        db.Index("idx_users_role_id", "role_id"),
        db.Index("idx_users_state", "state"),
        db.Index("idx_users_email", "email"),
    )


__all__ = ["User"]
