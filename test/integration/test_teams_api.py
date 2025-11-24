import pytest

pytestmark = pytest.mark.integration


def test_list_teams_empty(client, auth_header_admin):
    """Test listing teams when no teams exist.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
    """
    resp = client.get("/api/v1/teams/", headers=auth_header_admin)
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)
    assert data == []


def test_create_and_list_team(client, auth_header_admin):
    """Test team creation and listing.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
    """
    # Create team
    resp = client.post(
        "/api/v1/teams/",
        json={"name": "Equipo QA", "description": "Equipo de pruebas"},
        headers=auth_header_admin,
    )
    assert resp.status_code == 201

    created = resp.get_json()
    assert created["name"] == "Equipo QA"
    assert created["state"] is True

    # List teams
    resp2 = client.get("/api/v1/teams/", headers=auth_header_admin)
    assert resp2.status_code == 200

    data2 = resp2.get_json()
    assert len(data2) == 1
    assert data2[0]["name"] == "Equipo QA"
