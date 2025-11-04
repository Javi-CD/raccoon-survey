# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from flask import Blueprint, jsonify

from src.core.middlewares.rbac import role_required
from src.core.services.metrics_service import get_dashboard_metrics

bp = Blueprint("metrics", __name__)


@bp.get("/dashboard")
@role_required("admin", "rrhh")
def dashboard_metrics() -> tuple[dict, int]:
    """Return aggregated metrics for the admin dashboard.

    Returns:
        tuple[dict, int]: Dictionary with keys: cards, charts.
    """
    try:
        data = get_dashboard_metrics()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
