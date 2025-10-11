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
