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

bp = Blueprint("tokens", __name__)


@bp.post("/<int:survey_id>/generate")
@role_required("admin", "rrhh")
def generate_tokens(survey_id: int) -> tuple[list[dict], int]:
    """Generate survey tokens.

    Args:
        survey_id (int): Survey ID

    Returns:
        tuple[list[dict], int]: List of generated tokens, status code
    """
    payload = request.get_json(silent=True) or {}
    count = int(payload.get("count", 1))

    expires_at_str = payload.get("expires_at")
    if not expires_at_str:
        return jsonify({"message": "expires_at is required (ISO format)"}), 400

    try:
        expires_at = dt.datetime.fromisoformat(expires_at_str)
    except ValueError:
        return jsonify({"message": "invalid expires_at format"}), 400

    team_id = payload.get("team_id")

    employee_identifiers = payload.get("employee_identifiers")
    if employee_identifiers is not None and not isinstance(employee_identifiers, list):
        return jsonify({"message": "employee_identifiers must be a list"}), 400

    try:
        tokens = tokens_service.generate_tokens_for_survey(
            survey_id,
            count,
            expires_at=expires_at,
            team_id=team_id,
            employee_identifiers=employee_identifiers,
        )
    except LookupError:
        return jsonify({"message": "survey not found"}), 404
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500

    result = [
        {
            "id": t.id,
            "token": t.token,
            "employee_identifier": t.employee_identifier,
            "expires_at": t.expires_at.isoformat() if t.expires_at else None,
            "created_at": t.created_at.isoformat() if t.created_at else None,
            "survey_id": t.survey_id,
            "team_id": t.team_id,
            "is_used": t.is_used,
            "used_at": t.used_at.isoformat() if t.used_at else None,
        }
        for t in tokens
    ]

    return jsonify(result), 201


@bp.get("/<int:survey_id>/list")
@role_required("admin", "rrhh")
def list_tokens(survey_id: int) -> tuple[list[dict], int]:
    """List survey tokens.

    Args:
        survey_id (int): Survey ID

    Returns:
        tuple[list[dict], int]: List of tokens, status code
    """
    is_used = request.args.get("is_used")
    include_expired = request.args.get("include_expired")
    if is_used is not None:
        is_used = is_used.lower() in ("true", "1", "yes")

    include_expired = (
        True
        if include_expired is None
        else include_expired.lower() in ("true", "1", "yes")
    )

    rows = tokens_service.list_tokens(
        survey_id, is_used=is_used, include_expired=include_expired
    )

    return jsonify(rows), 200


@bp.get("/<int:survey_id>/export")
@role_required("admin", "rrhh")
def export_tokens(survey_id: int) -> tuple[str, int, dict]:
    """Export survey tokens to CSV.

    Args:
        survey_id (int): Survey ID

    Returns:
        tuple[str, int, dict]: CSV content, status code, headers
    """
    is_used = request.args.get("is_used")
    include_expired = request.args.get("include_expired")
    if is_used is not None:
        is_used = is_used.lower() in ("true", "1", "yes")

    include_expired = (
        True
        if include_expired is None
        else include_expired.lower() in ("true", "1", "yes")
    )

    csv_content = tokens_service.export_tokens_csv(
        survey_id, is_used=is_used, include_expired=include_expired
    )

    return (
        csv_content,
        200,
        {
            "Content-Type": "text/csv; charset=utf-8",
            "Content-Disposition": f"attachment; filename=survey_{survey_id}_tokens.csv",
        },
    )
