# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

import datetime as dt

from flask import Blueprint, jsonify, request

from src.core.middlewares.rbac import role_required
from src.core.services import tokens_service

bp = Blueprint("maintenance", __name__)


@bp.post("/tokens/cleanup")
@role_required("admin", "rrhh")
def cleanup_tokens() -> tuple[dict, int]:
    """Clean up expired tokens.

    Returns:
        tuple[dict, int]: {"matched": int, "deleted": int}, status code 200
    """
    payload = request.get_json(silent=True) or {}
    survey_id = payload.get("survey_id")
    team_id = payload.get("team_id")
    dry_run = bool(payload.get("dry_run", False))
    older_than_str = payload.get("older_than")

    older_than = None
    if older_than_str:
        try:
            older_than = dt.datetime.fromisoformat(older_than_str)
        except ValueError:
            return jsonify({"message": "invalid older_than format"}), 400

    result = tokens_service.cleanup_expired_tokens(
        survey_id=survey_id, team_id=team_id, dry_run=dry_run, older_than=older_than
    )

    return jsonify(result), 200
