# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from src.core.database import db


class AuditLog(db.Model):
    """Audit log model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(100), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), nullable=False)
    changed_by_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="SET NULL")
    )
    ip_address = db.Column(db.String(45))
    previous_data = db.Column(db.JSON)
    new_data = db.Column(db.JSON)
    metadata_ = db.Column("metadata", db.JSON)
    triggered_by = db.Column(db.String(20), server_default="manual", nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    changed_by_user = db.relationship("User")

    __table_args__ = (
        db.Index("idx_audit_entity", "entity_type", "entity_id"),
        db.Index("idx_audit_action", "action"),
        db.Index("idx_audit_changed_by", "changed_by_user_id"),
        db.Index("idx_audit_created_at", "created_at"),
        db.Index("idx_audit_triggered_by", "triggered_by"),
        db.CheckConstraint(
            "action IN ('create','update','delete','soft_delete','restore','login','logout','assign_role','generate_tokens')",
            name="ck_audit_logs_action",
        ),
        db.CheckConstraint(
            "triggered_by IN ('manual','system')",
            name="ck_audit_logs_triggered",
        ),
    )


__all__ = ["AuditLog"]
