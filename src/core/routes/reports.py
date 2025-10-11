from __future__ import annotations

from datetime import datetime

from flask import Blueprint, jsonify, request

from src.core.middlewares.rbac import role_required
from src.core.services import reports_service

bp = Blueprint("reports", __name__)


def _parse_iso_dt(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise ValueError("invalid_datetime_format")  # noqa: B904


@bp.get("/surveys/<int:survey_id>/summary")
@role_required("admin", "rrhh")
def survey_summary(survey_id: int) -> tuple[dict, int]:
    """Aggregate responses for a survey, optionally filtered by team and date range.

    Args:
        survey_id (int): ID of the survey.

    Returns:
        tuple[dict, int]: Formatted summary and status code.
    """
    team_id_raw = request.args.get("team_id")
    date_from_str = request.args.get("date_from")
    date_to_str = request.args.get("date_to")

    team_id = int(team_id_raw) if team_id_raw is not None else None
    date_from = _parse_iso_dt(date_from_str)
    date_to = _parse_iso_dt(date_to_str)

    try:
        data = reports_service.get_survey_summary(
            survey_id, team_id=team_id, date_from=date_from, date_to=date_to
        )
        return jsonify(data), 200
    except LookupError as e:
        return jsonify({"message": str(e)}), 404
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@bp.get("/teams/<int:team_id>/summary")
@role_required("admin", "rrhh")
def team_summary(team_id: int) -> tuple[dict, int]:
    """Aggregate responses for a team, optionally filtered by survey and date range.

    Args:
        team_id (int): ID of the team.

    Returns:
        tuple[dict, int]: Formatted summary and status code.
    """
    survey_id_raw = request.args.get("survey_id")
    date_from_str = request.args.get("date_from")
    date_to_str = request.args.get("date_to")

    survey_id = int(survey_id_raw) if survey_id_raw is not None else None
    date_from = _parse_iso_dt(date_from_str)
    date_to = _parse_iso_dt(date_to_str)

    try:
        data = reports_service.get_team_summary(
            team_id, survey_id=survey_id, date_from=date_from, date_to=date_to
        )
        return jsonify(data), 200
    except LookupError as e:
        return jsonify({"message": str(e)}), 404
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@bp.get("/export")
@role_required("admin", "rrhh")
def export_reports() -> tuple[str, int, dict]:
    """Export survey or team summary as CSV.

    Returns:
        tuple[str, int, dict]: CSV content, status code, and headers.
    """
    survey_id_raw = request.args.get("survey_id")
    team_id_raw = request.args.get("team_id")
    date_from_str = request.args.get("date_from")
    date_to_str = request.args.get("date_to")

    survey_id = int(survey_id_raw) if survey_id_raw is not None else None
    team_id = int(team_id_raw) if team_id_raw is not None else None
    date_from = _parse_iso_dt(date_from_str)
    date_to = _parse_iso_dt(date_to_str)

    try:
        if survey_id is not None:
            summary = reports_service.get_survey_summary(
                survey_id, team_id=team_id, date_from=date_from, date_to=date_to
            )
        elif team_id is not None:
            summary = reports_service.get_team_summary(
                team_id, survey_id=survey_id, date_from=date_from, date_to=date_to
            )
        else:
            return jsonify({"message": "either survey_id or team_id is required"}), 400

        csv_content = reports_service.export_summary_csv(summary=summary)
        filename = (
            f"survey_{survey_id}_summary.csv"
            if survey_id is not None
            else f"team_{team_id}_summary.csv"
        )

        return (
            csv_content,
            200,
            {
                "Content-Type": "text/csv; charset=utf-8",
                "Content-Disposition": f"attachment; filename={filename}",
            },
        )

    except LookupError as e:
        return jsonify({"message": str(e)}), 404
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500
