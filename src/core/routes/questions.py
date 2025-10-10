from __future__ import annotations

from flask import Blueprint, jsonify, request

from src.core.middlewares.rbac import role_required
from src.core.models import Question
from src.core.services import questions_service, surveys_service

bp = Blueprint("questions", __name__)


def serialize_question(q: Question) -> dict:
    """Serialize a question.

    Args:
        q (Question): Question instance.

    Returns:
        dict: Serialized question.
    """
    return {
        "id": q.id,
        "survey_id": q.survey_id,
        "text": q.text,
        "type": q.type,
        "options": q.options,
        "is_required": q.is_required,
        "order_position": q.order_position,
        "state": q.state,
        "created_at": q.created_at.isoformat() if q.created_at else None,
    }


@bp.get("/")
@role_required("admin", "rrhh")
def list_questions() -> tuple[dict, int]:
    """List questions.

    Returns:
        tuple[dict, int]: Serialized questions and HTTP status code.
    """
    survey_id = request.args.get("survey_id", type=int)
    questions = questions_service.list_questions(survey_id)

    return jsonify([serialize_question(q) for q in questions]), 200


@bp.post("/")
@role_required("admin", "rrhh")
def create_question() -> tuple[dict, int]:
    """Create a new question.

    Returns:
        tuple[dict, int]: Serialized question with created fields and HTTP status code.
    """
    payload = request.get_json(silent=True) or {}
    required_fields = ["survey_id", "text", "type"]
    missing = [f for f in required_fields if not payload.get(f)]
    if missing:
        return (
            jsonify({"message": f"missing fields: {', '.join(missing)}"}),
            400,
        )

    # Validate that the referenced survey exists to avoid FK violations
    survey = surveys_service.get_survey(payload["survey_id"])
    if not survey:
        return jsonify({"message": "survey not found"}), 404

    question = questions_service.create_question(payload)

    return jsonify(serialize_question(question)), 201


@bp.get("/<int:question_id>")
@role_required("admin", "rrhh")
def get_question(question_id: int) -> tuple[dict, int]:
    """Get question by ID.

    Args:
        question_id (int): Question ID.

    Returns:
        tuple[dict, int]: Serialized question and HTTP status code.
    """
    question = questions_service.get_question(question_id)
    if not question:
        return jsonify({"message": "question not found"}), 404

    return jsonify(serialize_question(question))


@bp.put("/<int:question_id>")
@role_required("admin", "rrhh")
def update_question(question_id: int) -> tuple[dict, int]:
    """Update question.

    Args:
        question_id (int): Question ID.

    Returns:
        tuple[dict, int]: Serialized question with updated fields and HTTP status code.
    """
    question = questions_service.get_question(question_id)
    if not question:
        return jsonify({"message": "question not found"}), 404

    payload = request.get_json(silent=True) or {}

    # If the payload attempts to change the survey_id, validate it exists first
    if "survey_id" in payload and payload["survey_id"] is not None:
        survey = surveys_service.get_survey(payload["survey_id"])
        if not survey:
            return jsonify({"message": "survey not found"}), 404
    question = questions_service.update_question(question_id, payload)

    return jsonify(serialize_question(question))


@bp.patch("/<int:question_id>/state")
@role_required("admin", "rrhh")
def change_question_state(question_id: int) -> tuple[dict, int]:
    """Change question state.

    Args:
        question_id (int): Question ID.

    Returns:
        tuple[dict, int]: Serialized question with updated state and HTTP status code.
    """
    question = questions_service.get_question(question_id)
    if not question:
        return jsonify({"message": "question not found"}), 404

    payload = request.get_json(silent=True) or {}
    state = payload.get("state")

    if state is None:
        return jsonify({"message": "state is required"}), 400

    question = questions_service.set_question_state(question_id, bool(state))

    return jsonify(serialize_question(question))
