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


@pytest.mark.integration
def test_list_users_empty(client, auth_header_admin: dict):
    """Test listing users returns an empty list when no users exist.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    resp = client.get("/api/v1/users/", headers=auth_header_admin)
    assert resp.status_code == 200
    assert resp.get_json() == []


@pytest.mark.integration
def test_create_user_success(client, auth_header_admin: dict):
    """Test creating a user returns a 201 status code and the created user.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name = _uniq("User")
    email = f"{uuid.uuid4().hex[:8]}@example.com"
    resp = client.post(
        "/api/v1/users/",
        json={"name": name, "email": email, "password": "secret"},
        headers=auth_header_admin,
    )
    assert resp.status_code == 201

    created = resp.get_json()
    assert created["name"] == name
    assert created["email"] == email
    assert created["state"] is True
    assert created.get("role_id") is None
    assert created.get("team_id") is None


@pytest.mark.integration
def test_get_user_success(client, auth_header_admin: dict):
    """Test getting a user returns the user details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name = _uniq("User")
    email = f"{uuid.uuid4().hex[:8]}@example.com"
    created = client.post(
        "/api/v1/users/",
        json={"name": name, "email": email, "password": "secret"},
        headers=auth_header_admin,
    ).get_json()
    user_id = int(created["id"])

    resp = client.get(f"/api/v1/users/{user_id}", headers=auth_header_admin)
    assert resp.status_code == 200
    got = resp.get_json()
    assert got["id"] == user_id
    assert got["email"] == email


@pytest.mark.integration
def test_update_user_success(client, auth_header_admin: dict):
    """Test updating a user returns the updated user details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name = _uniq("User")
    email = f"{uuid.uuid4().hex[:8]}@example.com"
    created = client.post(
        "/api/v1/users/",
        json={"name": name, "email": email, "password": "secret"},
        headers=auth_header_admin,
    ).get_json()
    user_id = int(created["id"])

    new_name = _uniq("Updated")
    new_email = f"{uuid.uuid4().hex[:8]}@example.com"
    resp = client.put(
        f"/api/v1/users/{user_id}",
        json={"name": new_name, "email": new_email},
        headers=auth_header_admin,
    )
    assert resp.status_code == 200
    updated = resp.get_json()
    assert updated["name"] == new_name
    assert updated["email"] == new_email


@pytest.mark.integration
def test_soft_delete_user_success(client, auth_header_admin: dict):
    """Test soft deleting a user returns the deleted user details.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name = _uniq("User")
    email = f"{uuid.uuid4().hex[:8]}@example.com"
    created = client.post(
        "/api/v1/users/",
        json={"name": name, "email": email, "password": "secret"},
        headers=auth_header_admin,
    ).get_json()
    user_id = int(created["id"])

    # Soft delete
    resp = client.patch(
        f"/api/v1/users/{user_id}/state",
        json={"state": False},
        headers=auth_header_admin,
    )
    assert resp.status_code == 200
    deleted = resp.get_json()
    assert deleted["state"] is False

    # Verify listing active users excludes deleted
    resp2 = client.get("/api/v1/users/", headers=auth_header_admin)
    assert resp2.status_code == 200
    assert all(u.get("state") is True for u in resp2.get_json())


@pytest.mark.integration
def test_create_user_requires_name_email_password(client, auth_header_admin: dict):
    """Test creating a user requires name, email, and password.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    # Missing name
    r1 = client.post(
        "/api/v1/users/",
        json={"name": "", "email": "a@b.com", "password": "x"},
        headers=auth_header_admin,
    )
    assert r1.status_code == 400
    assert r1.get_json().get("message") == "name is required"

    # Missing email
    r2 = client.post(
        "/api/v1/users/",
        json={"name": "A", "email": "", "password": "x"},
        headers=auth_header_admin,
    )
    assert r2.status_code == 400
    assert r2.get_json().get("message") == "email is required"

    # Missing password
    r3 = client.post(
        "/api/v1/users/",
        json={"name": "A", "email": "a@b.com"},
        headers=auth_header_admin,
    )
    assert r3.status_code == 400
    assert r3.get_json().get("message") == "password is required"
