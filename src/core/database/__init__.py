from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

__all__ = ["db"]
