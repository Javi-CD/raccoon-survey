# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from __future__ import annotations

from flask import Blueprint, jsonify, request

from src.core.services import responses_service

bp = Blueprint("anonymous", __name__)


@bp.post("/responses")
def submit_anonymous() -> tuple[dict, int]:
    """Submit anonymous responses using a one-time survey token.

    Body JSON:
    - token: str (required)
    - survey_id: int (optional, for extra validation)
    - responses: list[{question_id: int, answer: str}] (required)

    Returns:
        tuple[dict, int]: JSON response with saved_count, token_id, and survey_id, status code 201 on success
    """
    payload = request.get_json(silent=True) or {}
    token = payload.get("token")
    responses = payload.get("responses")
    survey_id = payload.get("survey_id")

    if not token:
        return jsonify({"message": "token is required"}), 400

    if responses is None or not isinstance(responses, list) or len(responses) == 0:
        return jsonify({"message": "responses must be a non-empty list"}), 400

    try:
        result = responses_service.submit_anonymous_responses(
            token_str=token, responses=responses, survey_id=survey_id
        )
    except LookupError as e:
        # token/survey not found
        return jsonify({"message": str(e)}), 404
    except ValueError as e:
        # invalid payload, token expired/already used, missing required questions, etc.
        return jsonify({"message": str(e)}), 400
    except RuntimeError as e:
        # database errors
        return jsonify({"message": str(e)}), 500

    return jsonify(result), 201


@bp.get("/resolve")
def resolve_anonymous() -> tuple[dict, int]:
    """Upload anonymous survey and its questions by token.

    Query parameters:
    - token: str (required)
    - survey_id: int (optional)

    Returns:
        tuple[dict, int]: JSON response with survey_id, token_id, and questions, status code 200 on success
    """
    token = request.args.get("token", type=str)
    survey_id = request.args.get("survey_id", type=int)

    if not token:
        return jsonify({"message": "token is required"}), 400

    try:
        data = responses_service.get_anonymous_survey(
            token_str=token, survey_id=survey_id
        )
    except LookupError as e:
        return jsonify({"message": str(e)}), 404
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"message": str(e)}), 500

    return jsonify(data), 200
