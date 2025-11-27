# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from test.utils.helpers import (
    _create_survey,
    _create_team,
    expires_at_future,
    expires_at_past,
)


def test_generate_tokens_success_basic(client, auth_header_admin: dict):
    """Test generating tokens for a survey successfully.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])

    expires_at = expires_at_future(days=1)
    res = client.post(
        f"/api/v1/tokens/{survey['id']}/generate",
        json={"count": 3, "expires_at": expires_at},
        headers=auth_header_admin,
    )
    assert res.status_code == 201

    rows = res.get_json()
    assert isinstance(rows, list) and len(rows) == 3
    for r in rows:
        assert r["survey_id"] == survey["id"]
        assert r["team_id"] == team["id"]
        assert isinstance(r["token"], str) and len(r["token"]) > 0
        assert r["is_used"] is False
        assert r["expires_at"] is not None

    # Listing should return the same tokens
    res_list = client.get(
        f"/api/v1/tokens/{survey['id']}/list", headers=auth_header_admin
    )
    assert res_list.status_code == 200

    listed = res_list.get_json()
    assert len(listed) == 3


def test_generate_tokens_with_identifiers_success(client, auth_header_admin: dict):
    """Test generating tokens with employee identifiers successfully.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])

    expires_at = expires_at_future(days=2)
    identifiers = ["emp-001", "emp-002", "emp-003"]
    res = client.post(
        f"/api/v1/tokens/{survey['id']}/generate",
        json={
            "count": 3,
            "expires_at": expires_at,
            "employee_identifiers": identifiers,
        },
        headers=auth_header_admin,
    )
    assert res.status_code == 201
    rows = res.get_json()
    assert [r["employee_identifier"] for r in rows] == identifiers


def test_generate_tokens_missing_expires_at(client, auth_header_admin: dict):
    """Test generating tokens missing expires_at parameter.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])

    res = client.post(
        f"/api/v1/tokens/{survey['id']}/generate",
        json={"count": 1},
        headers=auth_header_admin,
    )
    assert res.status_code == 400
    assert res.get_json()["message"] == "expires_at is required (ISO format)"


def test_generate_tokens_invalid_expires_at(client, auth_header_admin: dict):
    """Test generating tokens with invalid expires_at parameter.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])

    res = client.post(
        f"/api/v1/tokens/{survey['id']}/generate",
        json={"count": 1, "expires_at": "2025-13-40T25:61:00"},
        headers=auth_header_admin,
    )
    assert res.status_code in (400, 404)
    assert res.get_json()["message"] in (
        "invalid expires_at format",
        "survey not found",
    )


def test_generate_tokens_survey_not_found(client, auth_header_admin: dict):
    """Test generating tokens for a non-existent survey.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    expires_at = expires_at_future(days=1)
    res = client.post(
        "/api/v1/tokens/999999/generate",
        json={"count": 2, "expires_at": expires_at},
        headers=auth_header_admin,
    )
    assert res.status_code == 404
    assert res.get_json()["message"] == "survey not found"


def test_list_tokens_with_filters(client, auth_header_admin: dict):
    """Test listing tokens with filters.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])

    # Create one expired and two valid tokens
    past_expires = expires_at_past(days=1)
    future_expires = expires_at_future(days=1)

    r1 = client.post(
        f"/api/v1/tokens/{survey['id']}/generate",
        json={"count": 1, "expires_at": past_expires},
        headers=auth_header_admin,
    )
    r2 = client.post(
        f"/api/v1/tokens/{survey['id']}/generate",
        json={"count": 2, "expires_at": future_expires},
        headers=auth_header_admin,
    )
    assert r1.status_code == 201 and r2.status_code == 201

    res_list_all = client.get(
        f"/api/v1/tokens/{survey['id']}/list", headers=auth_header_admin
    )
    assert res_list_all.status_code == 200
    all_rows = res_list_all.get_json()
    assert len(all_rows) == 3

    res_list_valid = client.get(
        f"/api/v1/tokens/{survey['id']}/list?include_expired=false",
        headers=auth_header_admin,
    )
    assert res_list_valid.status_code == 200
    valid_rows = res_list_valid.get_json()
    assert len(valid_rows) == 2


def test_export_tokens_csv(client, auth_header_admin: dict):
    """Test exporting tokens to a CSV file.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team = _create_team(client, auth_header_admin)
    survey = _create_survey(client, auth_header_admin, team["id"])

    expires_at = expires_at_future(days=1)
    res_gen = client.post(
        f"/api/v1/tokens/{survey['id']}/generate",
        json={"count": 2, "expires_at": expires_at},
        headers=auth_header_admin,
    )
    assert res_gen.status_code == 201
    rows = res_gen.get_json()

    res_csv = client.get(
        f"/api/v1/tokens/{survey['id']}/export", headers=auth_header_admin
    )
    assert res_csv.status_code == 200
    content_type = res_csv.headers.get("Content-Type")
    assert content_type.startswith("text/csv")

    csv_text = res_csv.get_data(as_text=True)
    assert (
        "id,token,employee_identifier,is_used,used_at,expires_at,created_at,survey_id,team_id"
        in csv_text
    )
    # Ensure tokens present in CSV
    for r in rows:
        assert r["token"] in csv_text
