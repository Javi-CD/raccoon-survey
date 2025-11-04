# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from datetime import datetime

from flask import Blueprint, jsonify, request

from src.core.middlewares.rbac import role_required
from src.core.models import Survey
from src.core.services import surveys_service

bp = Blueprint("surveys", __name__)


def serialize_survey(s: Survey) -> dict:
    """Serialize a survey.

    Args:
        s (Survey): Survey instance.

    Returns:
        dict: Serialized survey.
    """
    return {
        "id": s.id,
        "team_id": s.team_id,
        "created_by_user_id": s.created_by_user_id,
        "title": s.title,
        "description": s.description,
        "is_anonymous": s.is_anonymous,
        "state": s.state,
        "expires_at": s.expires_at.isoformat() if s.expires_at else None,
        "created_at": s.created_at.isoformat() if s.created_at else None,
    }


@bp.get("/")
@role_required("admin", "rrhh")
def list_surveys() -> tuple[dict, int]:
    """List surveys.

    Returns:
        tuple[dict, int]: Serialized surveys and HTTP status code.
    """
    team_id = request.args.get("team_id", type=int)
    surveys = surveys_service.list_surveys(team_id)

    return jsonify([serialize_survey(s) for s in surveys]), 200


@bp.post("/")
@role_required("admin", "rrhh")
def create_survey() -> tuple[dict, int]:
    """Create a new survey.

    Returns:
        tuple[dict, int]: Serialized survey and HTTP status code.
    """
    payload = request.get_json(silent=True) or {}
    title = payload.get("title")
    team_id = payload.get("team_id")
    if not title or not team_id:
        return jsonify({"message": "title and team_id are required"}), 400

    description = payload.get("description")
    is_anonymous = bool(payload.get("is_anonymous", True))
    expires_at = payload.get("expires_at")
    created_by_user_id = payload.get("created_by_user_id")

    expires_dt = None
    if expires_at:
        try:
            expires_dt = datetime.fromisoformat(expires_at)
        except ValueError:
            return jsonify({"message": "invalid expires_at format"}), 400

    survey = surveys_service.create_survey(
        {
            "team_id": team_id,
            "created_by_user_id": created_by_user_id,
            "title": title,
            "description": description,
            "is_anonymous": is_anonymous,
            "expires_at": expires_dt,
        }
    )

    return jsonify(serialize_survey(survey)), 201


@bp.get("/<int:survey_id>")
@role_required("admin", "rrhh")
def get_survey(survey_id: int) -> tuple[dict, int]:
    """Get a survey.

    Args:
        survey_id (int): Survey ID.

    Returns:
        tuple[dict, int]: Serialized survey and HTTP status code.
    """
    survey = surveys_service.get_survey(survey_id)
    if not survey:
        return jsonify({"message": "survey not found"}), 404

    return jsonify(serialize_survey(survey)), 200


@bp.put("/<int:survey_id>")
@role_required("admin", "rrhh")
def update_survey(survey_id: int) -> tuple[dict, int]:
    """Update survey.

    Args:
        survey_id (int): Survey ID.

    Returns:
        tuple[dict, int]: Serialized survey with updated fields and HTTP status code.
    """
    survey = surveys_service.get_survey(survey_id)
    if not survey:
        return jsonify({"message": "survey not found"}), 404

    payload = request.get_json(silent=True) or {}
    update_data: dict = {}
    for field in [
        "title",
        "description",
        "is_anonymous",
        "team_id",
        "created_by_user_id",
    ]:
        if field in payload and payload[field] is not None:
            update_data[field] = payload[field]

    if "expires_at" in payload:
        expires_at = payload.get("expires_at")
        if expires_at:
            try:
                update_data["expires_at"] = datetime.fromisoformat(expires_at)
            except ValueError:
                return jsonify({"message": "invalid expires_at format"}), 400
        else:
            update_data["expires_at"] = None

    if "state" in payload and payload["state"] is not None:
        update_data["state"] = bool(payload["state"])

    survey = surveys_service.update_survey(survey_id, update_data)

    return jsonify(serialize_survey(survey))


@bp.patch("/<int:survey_id>/state")
@role_required("admin", "rrhh")
def change_survey_state(survey_id: int) -> tuple[dict, int]:
    """Change survey state.

    Args:
        survey_id (int): Survey ID.

    Returns:
        tuple[dict, int]: Serialized survey with updated state and HTTP status code.
    """
    survey = surveys_service.get_survey(survey_id)
    if not survey:
        return jsonify({"message": "survey not found"}), 404

    payload = request.get_json(silent=True) or {}
    state = payload.get("state")
    if state is None:
        return jsonify({"message": "state is required"}), 400

    survey = surveys_service.set_survey_state(survey_id, bool(state))

    return jsonify(serialize_survey(survey)), 200
