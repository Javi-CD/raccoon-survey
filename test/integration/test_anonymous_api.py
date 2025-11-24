# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from test.utils.helpers import _uniq, expires_at_future, expires_at_past


def _create_team(client, auth_header_admin: dict) -> dict:
    """Create a team using the API.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.

    Returns:
        dict: The JSON response containing the created team details.
    """
    name = _uniq("team")
    res = client.post(
        "/api/v1/teams/",
        json={"name": name, "description": "Integration team"},
        headers=auth_header_admin,
    )
    assert res.status_code == 201

    return res.get_json()


def _create_survey(client, auth_header_admin: dict, team_id: int) -> dict:
    """Create a survey using the API.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
        team_id (int): The ID of the team to associate the survey with.

    Returns:
        dict: The JSON response containing the created survey details.
    """
    title = _uniq("survey")
    res = client.post(
        "/api/v1/surveys/",
        json={
            "title": title,
            "description": "Anonymous employee survey",
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


def _generate_token(
    client, auth_header_admin: dict, survey_id: int, *, expires_at: str
) -> dict:
    """Generate a token using the API.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
        survey_id (int): The ID of the survey to generate the token for.
        expires_at (str): The expiration time for the token in ISO format.

    Returns:
        dict: The JSON response containing the generated token details.
    """
    res = client.post(
        f"/api/v1/tokens/{survey_id}/generate",
        json={"count": 1, "expires_at": expires_at},
        headers=auth_header_admin,
    )
    assert res.status_code == 201
    rows = res.get_json()
    assert isinstance(rows, list) and len(rows) == 1

    return rows[0]


def test_anonymous_resolve_success(client, auth_header_admin: dict):
    """Test successful resolution of an anonymous response.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    # Create two questions: one required text, one optional scale
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

    # Token valid for 1 day
    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expires_at_future(days=1),
    )

    # Resolve anonymous
    res = client.get(
        f"/api/v1/anonymous/resolve?token={token_row['token']}&survey_id={survey['id']}"
    )
    assert res.status_code == 200

    data = res.get_json()
    assert data and data["survey"]["id"] == survey["id"]
    assert data["token"]["id"] == token_row["id"]
    assert isinstance(data.get("questions"), list) and len(data["questions"]) == 2

    got_ids = sorted(q["id"] for q in data["questions"])
    assert got_ids == sorted([q1["id"], q2["id"]])


def test_anonymous_resolve_missing_token(client):
    """Test resolution of an anonymous response with missing token.

    Args:
        client (FlaskClient): The test client for the Flask application.
    """
    res = client.get("/api/v1/anonymous/resolve")
    assert res.status_code == 400
    assert res.get_json().get("message") == "token is required"


def test_anonymous_resolve_invalid_token(client):
    """Test resolution of an anonymous response with invalid token.

    Args:
        client (FlaskClient): The test client for the Flask application.
    """
    res = client.get("/api/v1/anonymous/resolve?token=fake-token")
    assert res.status_code == 404
    assert res.get_json().get("message") == "token_not_found"


def test_anonymous_resolve_token_expired(client, auth_header_admin: dict):
    """Test resolution of an anonymous response with expired token.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Q"),
        qtype="text",
        is_required=True,
        order_position=1,
    )

    expired_at = expires_at_past(minutes=1)
    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expired_at,
    )

    res = client.get(
        f"/api/v1/anonymous/resolve?token={token_row['token']}&survey_id={survey['id']}"
    )
    assert res.status_code == 400
    assert res.get_json().get("message") == "token_expired"


def test_anonymous_submit_success_and_idempotency(client, auth_header_admin: dict):
    """Test successful submission of an anonymous response and idempotency.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
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
        qtype="text",
        is_required=False,
        order_position=2,
    )

    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expires_at_future(days=1),
    )

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [
            {"question_id": q1["id"], "answer": "Muy bien"},
            {"question_id": q2["id"], "answer": ""},  # optional empty should be skipped
        ],
    }
    res_submit = client.post("/api/v1/anonymous/responses", json=payload)
    assert res_submit.status_code == 201
    summary = res_submit.get_json()
    assert summary["saved_count"] == 1
    assert summary["survey_id"] == survey["id"]
    assert summary["token_id"] == token_row["id"]

    # Second submission with same token should fail (already used)
    res_again = client.post("/api/v1/anonymous/responses", json=payload)
    assert res_again.status_code == 400
    assert res_again.get_json().get("message") in (
        "token_already_used",
        "already_submitted",
    )

    # Resolve after used should also fail with 400
    res_resolve = client.get(
        f"/api/v1/anonymous/resolve?token={token_row['token']}&survey_id={survey['id']}"
    )
    assert res_resolve.status_code == 400
    assert res_resolve.get_json().get("message") in (
        "token_already_used",
        "token_expired",
    )


def test_anonymous_submit_token_expired(client, auth_header_admin: dict):
    """Test submission of an anonymous response with expired token.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    q1 = _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Req"),
        qtype="text",
        is_required=True,
        order_position=1,
    )

    expired_at = expires_at_past(minutes=1)
    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expired_at,
    )

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [{"question_id": q1["id"], "answer": "Hola"}],
    }
    res = client.post("/api/v1/anonymous/responses", json=payload)
    assert res.status_code == 400
    assert res.get_json().get("message") == "token_expired"


def test_anonymous_submit_missing_required_questions(client, auth_header_admin: dict):
    """Test submission of an anonymous response with missing required questions.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    rq = _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Req"),
        qtype="text",
        is_required=True,
        order_position=1,
    )

    # Create an optional question to send a non-empty responses list
    oq = _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Opt"),
        qtype="text",
        is_required=False,
        order_position=2,
    )

    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expires_at_future(days=1),
    )

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [{"question_id": oq["id"], "answer": "x"}],
    }
    res = client.post("/api/v1/anonymous/responses", json=payload)
    assert res.status_code == 400

    msg = res.get_json().get("message", "")
    assert isinstance(msg, str) and msg.startswith("missing_required_questions:")


def test_anonymous_submit_missing_question_id(client, auth_header_admin: dict):
    """Test submission of an anonymous response with missing question ID.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Req"),
        qtype="text",
        is_required=True,
        order_position=1,
    )
    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expires_at_future(days=1),
    )

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [{"answer": "Sin ID"}],
    }
    res = client.post("/api/v1/anonymous/responses", json=payload)
    assert res.status_code == 400
    assert res.get_json().get("message") == "missing_question_id"


def test_anonymous_submit_missing_answer(client, auth_header_admin: dict):
    """Test submission of an anonymous response with missing answer.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    q1 = _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Req"),
        qtype="text",
        is_required=True,
        order_position=1,
    )
    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expires_at_future(days=1),
    )

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [{"question_id": q1["id"]}],
    }
    res = client.post("/api/v1/anonymous/responses", json=payload)
    assert res.status_code == 400
    assert res.get_json().get("message") == "missing_answer"


def test_anonymous_submit_question_not_in_survey(client, auth_header_admin: dict):
    """Test submission of an anonymous response with question not in survey.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Req"),
        qtype="text",
        is_required=True,
        order_position=1,
    )
    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expires_at_future(days=1),
    )

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [{"question_id": 999999, "answer": "no"}],
    }
    res = client.post("/api/v1/anonymous/responses", json=payload)
    assert res.status_code == 400
    assert res.get_json().get("message") == "question_not_in_survey"


def test_anonymous_submit_empty_required_answer(client, auth_header_admin: dict):
    """Test submission of an anonymous response with empty required answer.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    q1 = _create_question(
        client,
        auth_header_admin,
        survey["id"],
        text=_uniq("Req"),
        qtype="text",
        is_required=True,
        order_position=1,
    )
    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expires_at_future(days=1),
    )

    payload = {
        "token": token_row["token"],
        "survey_id": survey["id"],
        "responses": [{"question_id": q1["id"], "answer": "  "}],
    }
    res = client.post("/api/v1/anonymous/responses", json=payload)
    assert res.status_code == 400
    msg = res.get_json().get("message", "")
    assert isinstance(msg, str) and msg.startswith("empty_required_answer:")


def test_anonymous_submit_invalid_membership(client, auth_header_admin: dict):
    """Test submission of an anonymous response with invalid membership.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
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

    token_row = _generate_token(
        client,
        auth_header_admin,
        survey["id"],
        expires_at=expires_at_future(days=1),
    )

    payload = {
        "token": token_row["token"],
        "survey_id": 999999,  # incorrect membership
        "responses": [{"question_id": q1["id"], "answer": "Ok"}],
    }
    res = client.post("/api/v1/anonymous/responses", json=payload)
    assert res.status_code == 400
    assert res.get_json().get("message") == "token_not_for_survey"


def test_anonymous_submit_token_not_found(client, auth_header_admin: dict):
    """Test submission of an anonymous response with a non-existent token.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    payload = {
        "token": "invalid-token",
        "responses": [{"question_id": 1, "answer": "A"}],
    }
    res = client.post("/api/v1/anonymous/responses", json=payload)
    assert res.status_code == 404
    assert res.get_json().get("message") == "token_not_found"
