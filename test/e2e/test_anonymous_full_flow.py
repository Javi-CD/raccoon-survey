# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import pytest

from test.utils.helpers import _uniq, expires_at_future

pytestmark = pytest.mark.e2e


def _create_team(client, auth_header_admin: dict) -> dict:
    """Create a team.

    Args:
        client (TestClient): The test client fixture.
        auth_header_admin (dict): The admin authentication header.

    Returns:
        dict: The created team.
    """
    name = _uniq("Team")
    res = client.post(
        "/api/v1/teams/",
        json={"name": name, "description": "E2E team"},
        headers=auth_header_admin,
    )
    assert res.status_code == 201

    return res.get_json()


def _create_survey(client, auth_header_admin: dict, team_id: int) -> dict:
    """Create a survey.

    Args:
        client (TestClient): The test client fixture.
        auth_header_admin (dict): The admin authentication header.
        team_id (int): The team ID.

    Returns:
        dict: The created survey.
    """
    title = _uniq("Survey")
    res = client.post(
        "/api/v1/surveys/",
        json={
            "title": title,
            "description": "E2E anonymous flow",
            "team_id": team_id,
            "is_anonymous": True,
            "state": True,
        },
        headers=auth_header_admin,
    )
    assert res.status_code == 201

    return res.get_json()


def _create_question(
    client,
    auth_header_admin: dict,
    survey_id: int,
    *,
    text: str,
    qtype: str,
    is_required: bool = True,
    options: dict | None = None,
    order_position: int = 1,
) -> dict:
    """Create a question.

    Args:
        client (TestClient): The test client fixture.
        auth_header_admin (dict): The admin authentication header.
        survey_id (int): The survey ID.
        text (str): The question text.
        qtype (str): The question type.
        is_required (bool, optional): Whether the question is required. Defaults to True.
        options (dict | None, optional): The question options. Defaults to None.
        order_position (int, optional): The question order position. Defaults to 1.

    Returns:
        dict: The created question.
    """
    payload = {
        "survey_id": survey_id,
        "text": text,
        "type": qtype,
        "is_required": is_required,
        "order_position": order_position,
    }
    if options is not None:
        payload["options"] = options

    res = client.post(
        "/api/v1/questions/",
        json=payload,
        headers=auth_header_admin,
    )
    assert res.status_code == 201

    return res.get_json()


def _generate_token(client, auth_header_admin: dict, survey_id: int) -> dict:
    """Generate a token.

    Args:
        client (TestClient): The test client fixture.
        auth_header_admin (dict): The admin authentication header.
        survey_id (int): The survey ID.

    Returns:
        dict: The generated token.
    """
    expires_at = expires_at_future(days=1)
    res = client.post(
        f"/api/v1/tokens/{survey_id}/generate",
        json={"count": 1, "expires_at": expires_at},
        headers=auth_header_admin,
    )
    assert res.status_code == 201
    rows = res.get_json()
    assert isinstance(rows, list) and len(rows) == 1
    return rows[0]


def test_e2e_anonymous_submit_and_summary(client, auth_header_admin: dict):
    """Test the anonymous full flow.

    This test covers the following steps:
    1. Create a team.
    2. Create a survey.
    3. Create two questions.
    4. Generate a token.
    5. Resolve the token.
    6. Submit responses anonymously.
    7. Check the summary.

    Args:
        client (TestClient): The test client fixture.
        auth_header_admin (dict): The admin authentication header.
    """

    # Create team, survey, questions and token
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

    token_row = _generate_token(client, auth_header_admin, survey["id"])

    # Resolve the token
    res_resolve = client.get(
        f"/api/v1/anonymous/resolve?token={token_row['token']}&survey_id={survey['id']}"
    )
    assert res_resolve.status_code == 200

    resolved = res_resolve.get_json()
    assert resolved["survey"]["id"] == survey["id"]
    assert len(resolved.get("questions", [])) == 2

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [
            {"question_id": q1["id"], "answer": "Satisfecho"},
            {"question_id": q2["id"], "answer": "4"},
        ],
    }

    # Submit responses anonymously
    res_submit = client.post("/api/v1/anonymous/responses", json=payload)
    assert res_submit.status_code == 201

    submit_result = res_submit.get_json()
    assert submit_result["survey_id"] == survey["id"]
    assert submit_result.get("saved_count") == 2

    # Check the summary
    res_summary = client.get(
        f"/api/v1/reports/surveys/{survey['id']}/summary", headers=auth_header_admin
    )
    assert res_summary.status_code == 200

    summary = res_summary.get_json()
    assert summary["survey_id"] == survey["id"]
    assert isinstance(summary.get("questions"), list) and len(summary["questions"]) == 2

    res_summary = client.get(
        f"/api/v1/reports/surveys/{survey['id']}/summary", headers=auth_header_admin
    )
    assert res_summary.status_code == 200

    data = res_summary.get_json()
    assert data["survey_id"] == survey["id"]
    assert isinstance(data.get("questions"), list) and len(data["questions"]) == 2

    q1_summary = next((x for x in data["questions"] if x["id"] == q1["id"]), None)
    q2_summary = next((x for x in data["questions"] if x["id"] == q2["id"]), None)
    assert q1_summary and q1_summary["total"] == 1
    assert any(
        a["value"] == "Satisfecho" and a["count"] == 1 for a in q1_summary["answers"]
    )

    assert q2_summary and q2_summary["total"] == 1
    assert any(a["value"] == "4" and a["count"] == 1 for a in q2_summary["answers"])
