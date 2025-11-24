import datetime as dt

from test.e2e.test_anonymous_full_flow import (
    _create_question,
    _create_survey,
    _create_team,
    _uniq,
)


def test_e2e_team_summary_with_date_filter(client, auth_header_admin: dict):
    """Test the team summary endpoint with date filter.

    This test ensures that the team summary endpoint returns the correct data
    when filtered by a date range.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): A dictionary containing the admin authorization header.
    """

    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])

    q1 = _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Q1"),
        qtype="text",
        is_required=True,
        order_position=1,
    )
    q2 = _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Q2"),
        qtype="scale",
        is_required=False,
        options={"min": 1, "max": 5},
        order_position=2,
    )

    # Generate a token associated explicitly to the team (required for team summary)
    res_gen = client.post(
        f"/api/v1/tokens/{survey['id']}/generate",
        json={
            "count": 1,
            "expires_at": "2099-12-31T23:59:59",
            "team_id": team["id"],
        },
        headers=auth_header_admin,
    )
    assert res_gen.status_code == 201
    token_row = res_gen.get_json()[0]

    # Resolve the token to get the question IDs
    res_resolve = client.get(
        f"/api/v1/anonymous/resolve?token={token_row['token']}&survey_id={survey['id']}"
    )
    assert res_resolve.status_code == 200

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [
            {"question_id": q1["id"], "answer": "Muy bien"},
            {"question_id": q2["id"], "answer": "5"},
        ],
    }
    res_submit = client.post("/api/v1/anonymous/responses", json=payload)
    assert res_submit.status_code == 201

    # Range of dates around UTC "now" to avoid time zone discrepancies
    now = dt.datetime.utcnow()
    date_from = (now - dt.timedelta(days=1)).isoformat()
    date_to = (now + dt.timedelta(days=1)).isoformat()

    # Query the team summary with date filter
    res_summary = client.get(
        f"/api/v1/reports/teams/{team['id']}/summary?survey_id={survey['id']}&date_from={date_from}&date_to={date_to}",
        headers=auth_header_admin,
    )
    assert res_summary.status_code == 200

    summary = res_summary.get_json()
    assert summary["team_id"] == team["id"]
    assert isinstance(summary.get("questions"), list) and len(summary["questions"]) == 2

    questions_by_id = {q["id"]: q for q in summary["questions"]}
    q1_summary = questions_by_id.get(q1["id"])  # type: ignore[index]
    q2_summary = questions_by_id.get(q2["id"])  # type: ignore[index]
    assert q1_summary and q1_summary["total"] == 1
    assert any(
        a["value"] == "Muy bien" and a["count"] == 1 for a in q1_summary["answers"]
    )
    assert q2_summary and q2_summary["total"] == 1
    assert any(a["value"] == "5" and a["count"] == 1 for a in q2_summary["answers"])
