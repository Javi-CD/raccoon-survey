from __future__ import annotations

from flask import Blueprint, jsonify, request

from src.core.database import db
from src.core.middlewares.rbac import role_required
from src.core.models import Team

bp = Blueprint("teams", __name__)

def serialize_team(team: Team) -> dict:
    """Serialize a team.

    Args:
        team (Team): Team instance.

    Returns:
        dict: Serialized team.
    """
    return {
        "id": team.id,
        "name": team.name,
        "description": team.description,
        "state": team.state,
        "created_at": team.created_at.isoformat() if team.created_at else None,
    }


@bp.get("/")
@role_required("admin", "rrhh")
def list_teams() -> tuple[dict, int]:
    """List teams.

    Returns:
        tuple[dict, int]: Serialized teams and HTTP status code.
    """
    teams = Team.query.order_by(Team.created_at.desc()).all()

    return jsonify([serialize_team(t) for t in teams]), 200


@bp.post("/")
@role_required("admin", "rrhh")
def create_team() -> tuple[dict, int]:
    """Create a team.

    Returns:
        tuple[dict, int]: Serialized team and HTTP status code.
    """
    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    description = payload.get("description")

    if not name:
        return jsonify({"message": "name is required"}), 400

    team = Team(name=name, description=description)
    db.session.add(team)
    db.session.commit()

    return jsonify(serialize_team(team)), 201


@bp.get("/<int:team_id>")
@role_required("admin", "rrhh")
def get_team(team_id: int) -> tuple[dict, int]:
    """Get a team.

    Args:
        team_id (int): Team ID.

    Returns:
        tuple[dict, int]: Serialized team and HTTP status code.
    """
    team = Team.query.get(team_id)
    if not team:
        return jsonify({"message": "team not found"}), 404

    return jsonify(serialize_team(team)), 200


@bp.put("/<int:team_id>")
@role_required("admin", "rrhh")
def update_team(team_id: int) -> tuple[dict, int]:
    """Update a team.

    Args:
        team_id (int): Team ID.

    Returns:
        tuple[dict, int]: Serialized team and HTTP status code.
    """
    team = Team.query.get(team_id)
    if not team:
        return jsonify({"message": "team not found"}), 404

    payload = request.get_json(silent=True) or {}
    name = payload.get("name")
    description = payload.get("description")
    state = payload.get("state")

    if name is not None:
        team.name = name
    if description is not None:
        team.description = description
    if state is not None:
        team.state = bool(state)

    db.session.commit()

    return jsonify(serialize_team(team))


@bp.patch("/<int:team_id>/state")
@role_required("admin", "rrhh")
def change_team_state(team_id: int) -> tuple[dict, int]:
    """Change a team state.

    Args:
        team_id (int): Team ID.

    Returns:
        tuple[dict, int]: Serialized team and HTTP status code.
    """
    team = Team.query.get(team_id)
    if not team:
        return jsonify({"message": "team not found"}), 404

    payload = request.get_json(silent=True) or {}
    state = payload.get("state")
    if state is None:
        return jsonify({"message": "state is required"}), 400

    team.state = bool(state)
    db.session.commit()

    return jsonify(serialize_team(team)), 200
