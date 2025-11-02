from __future__ import annotations

from src.core.database import db


class Role(db.Model):
    """Role model.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance.
    """

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text)
    state = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    users = db.relationship("User", back_populates="role")

    __table_args__ = (
        db.Index("idx_roles_name", "name"),
        db.Index("idx_roles_state", "state"),
    )


__all__ = ["Role"]
