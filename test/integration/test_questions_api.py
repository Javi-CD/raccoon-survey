# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import pytest

from test.utils.helpers import _create_survey, _create_team, _uniq


@pytest.mark.integration
def test_list_questions_empty(client, auth_header_admin: dict):
    """Test listing questions returns an empty list when no questions exist.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    resp = client.get("/api/v1/questions/", headers=auth_header_admin)
    assert resp.status_code == 200
    assert resp.get_json() == []


@pytest.mark.integration
def test_create_question_success(client, auth_header_admin: dict):
    """Test creating a question returns the created question details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    survey_id = int(survey["id"])
    payload = {
        "survey_id": survey_id,
        "text": _uniq("Question"),
        "type": "text",
        "is_required": True,
        "order_position": 1,
    }
    resp = client.post(
        "/api/v1/questions/",
        json=payload,
        headers=auth_header_admin,
    )
    assert resp.status_code == 201

    created = resp.get_json()
    assert created["survey_id"] == survey_id
    assert created["text"] == payload["text"]
    assert created["type"] == "text"
    assert created["is_required"] is True


@pytest.mark.integration
def test_get_question_success(client, auth_header_admin: dict):
    """Test getting a question returns the question details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    survey_id = int(survey["id"])
    payload = {
        "survey_id": survey_id,
        "text": _uniq("Question"),
        "type": "text",
    }
    created = client.post(
        "/api/v1/questions/",
        json=payload,
        headers=auth_header_admin,
    ).get_json()
    qid = int(created["id"])

    resp = client.get(f"/api/v1/questions/{qid}", headers=auth_header_admin)
    assert resp.status_code == 200

    got = resp.get_json()
    assert got["id"] == qid
    assert got["survey_id"] == survey_id


@pytest.mark.integration
def test_update_question_success(client, auth_header_admin: dict):
    """Test updating a question returns the updated question details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    survey_id = int(survey["id"])
    created = client.post(
        "/api/v1/questions/",
        json={"survey_id": survey_id, "text": _uniq("Q"), "type": "text"},
        headers=auth_header_admin,
    ).get_json()
    qid = int(created["id"])

    resp = client.put(
        f"/api/v1/questions/{qid}",
        json={
            "text": _uniq("Updated"),
            "type": "multiple_choice",
            "options": ["A", "B"],
        },
        headers=auth_header_admin,
    )
    assert resp.status_code == 200
    updated = resp.get_json()

    assert updated["type"] == "multiple_choice"
    assert isinstance(updated.get("options"), list)


@pytest.mark.integration
def test_change_question_state_success(client, auth_header_admin: dict):
    """Test changing a question state returns the updated question details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])
    survey_id = int(survey["id"])
    created = client.post(
        "/api/v1/questions/",
        json={"survey_id": survey_id, "text": _uniq("Q"), "type": "text"},
        headers=auth_header_admin,
    ).get_json()
    qid = int(created["id"])

    resp = client.patch(
        f"/api/v1/questions/{qid}/state",
        json={"state": False},
        headers=auth_header_admin,
    )
    assert resp.status_code == 200

    changed = resp.get_json()
    assert changed["state"] is False


@pytest.mark.integration
def test_create_question_missing_fields(client, auth_header_admin: dict):
    """Test creating a question with missing fields returns a 400 status code.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    resp = client.post(
        "/api/v1/questions/",
        json={"text": "", "type": ""},
        headers=auth_header_admin,
    )
    assert resp.status_code == 400

    msg = resp.get_json().get("message")
    assert msg and msg.startswith("missing fields:")


@pytest.mark.integration
def test_create_question_survey_not_found(client, auth_header_admin: dict):
    """Test creating a question with a non-existent survey_id returns a 404 status code.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    resp = client.post(
        "/api/v1/questions/",
        json={"survey_id": 999999, "text": _uniq("Q"), "type": "text"},
        headers=auth_header_admin,
    )
    assert resp.status_code == 404
    assert resp.get_json().get("message") == "survey not found"
