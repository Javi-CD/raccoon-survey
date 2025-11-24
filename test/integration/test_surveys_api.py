from datetime import datetime, timedelta
import uuid

import pytest


def _uniq(base: str) -> str:
    """Generate a unique string by appending a UUID.

    Args:
        base (str): The base string to which the UUID will be appended.

    Returns:
        str: The unique string.
    """
    return f"{base}-{uuid.uuid4().hex[:6]}"


def _create_team(client, auth_header_admin: dict) -> int:
    """Create a team and return its ID.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.

    Returns:
        int: The ID of the created team.
    """
    name = _uniq("Team")
    resp = client.post(
        "/api/v1/teams/",
        json={"name": name},
        headers=auth_header_admin,
    )
    assert resp.status_code == 201

    team_id = int(resp.get_json()["id"])

    return team_id


@pytest.mark.integration
def test_list_surveys_empty(client, auth_header_admin: dict):
    """Test listing surveys returns an empty list when no surveys exist.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    resp = client.get("/api/v1/surveys/", headers=auth_header_admin)
    assert resp.status_code == 200
    assert resp.get_json() == []


@pytest.mark.integration
def test_create_survey_success(client, auth_header_admin: dict):
    """Test creating a survey returns a 201 status code and the created survey.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team_id = _create_team(client, auth_header_admin)
    title = _uniq("Survey")
    resp = client.post(
        "/api/v1/surveys/",
        json={"title": title, "team_id": team_id, "description": "Desc"},
        headers=auth_header_admin,
    )
    assert resp.status_code == 201
    created = resp.get_json()
    assert created["title"] == title
    assert created["team_id"] == team_id
    assert created["is_anonymous"] is True


@pytest.mark.integration
def test_get_survey_success(client, auth_header_admin: dict):
    """Test getting a survey returns the survey details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team_id = _create_team(client, auth_header_admin)
    title = _uniq("Survey")
    created = client.post(
        "/api/v1/surveys/",
        json={"title": title, "team_id": team_id},
        headers=auth_header_admin,
    ).get_json()
    survey_id = int(created["id"])

    resp = client.get(f"/api/v1/surveys/{survey_id}", headers=auth_header_admin)
    assert resp.status_code == 200

    got = resp.get_json()
    assert got["id"] == survey_id
    assert got["title"] == title


@pytest.mark.integration
def test_update_survey_success(client, auth_header_admin: dict):
    """Test updating a survey returns the updated survey details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team_id = _create_team(client, auth_header_admin)
    title = _uniq("Survey")
    created = client.post(
        "/api/v1/surveys/",
        json={"title": title, "team_id": team_id},
        headers=auth_header_admin,
    ).get_json()
    survey_id = int(created["id"])

    new_title = _uniq("Updated")
    expires_at = (datetime.utcnow() + timedelta(days=7)).isoformat()
    resp = client.put(
        f"/api/v1/surveys/{survey_id}",
        json={
            "title": new_title,
            "description": "Updated Desc",
            "is_anonymous": False,
            "expires_at": expires_at,
        },
        headers=auth_header_admin,
    )
    assert resp.status_code == 200

    updated = resp.get_json()
    assert updated["title"] == new_title
    assert updated["description"] == "Updated Desc"
    assert updated["is_anonymous"] is False
    assert updated["expires_at"] is not None


@pytest.mark.integration
def test_change_survey_state_success(client, auth_header_admin: dict):
    """Test changing a survey state returns the updated survey state.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team_id = _create_team(client, auth_header_admin)
    title = _uniq("Survey")
    created = client.post(
        "/api/v1/surveys/",
        json={"title": title, "team_id": team_id},
        headers=auth_header_admin,
    ).get_json()
    survey_id = int(created["id"])

    resp = client.patch(
        f"/api/v1/surveys/{survey_id}/state",
        json={"state": False},
        headers=auth_header_admin,
    )
    assert resp.status_code == 200

    changed = resp.get_json()
    assert changed["state"] is False


@pytest.mark.integration
def test_create_survey_requires_title_and_team_id(client, auth_header_admin: dict):
    """Test creating a survey requires both title and team_id.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    # Missing both
    r1 = client.post(
        "/api/v1/surveys/",
        json={"title": "", "team_id": None},
        headers=auth_header_admin,
    )
    assert r1.status_code == 400
    assert r1.get_json().get("message") == "title and team_id are required"


@pytest.mark.integration
def test_update_survey_invalid_expires_at(client, auth_header_admin: dict):
    """Test updating a survey with an invalid expires_at format returns a 400 error.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    team_id = _create_team(client, auth_header_admin)
    title = _uniq("Survey")
    created = client.post(
        "/api/v1/surveys/",
        json={"title": title, "team_id": team_id},
        headers=auth_header_admin,
    ).get_json()
    survey_id = int(created["id"])

    resp = client.put(
        f"/api/v1/surveys/{survey_id}",
        json={"expires_at": "not-a-date"},
        headers=auth_header_admin,
    )
    assert resp.status_code == 400
    assert resp.get_json().get("message") == "invalid expires_at format"
