# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import pytest

from test.utils.helpers import _uniq


@pytest.mark.integration
def test_list_roles_empty(client, auth_header_admin: dict):
    """Test listing roles when no roles exist.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
    """
    resp = client.get("/api/v1/roles/", headers=auth_header_admin)
    assert resp.status_code == 200
    assert resp.get_json() == []


@pytest.mark.integration
def test_create_role_success(client, auth_header_admin: dict):
    """Test role creation with valid data.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
    """
    name = _uniq("rrhh")
    resp = client.post(
        "/api/v1/roles/",
        json={"name": name, "description": "Human Resources"},
        headers=auth_header_admin,
    )
    assert resp.status_code == 201

    created = resp.get_json()
    assert created["name"] == name
    assert created["description"] == "Human Resources"
    assert created["state"] is True


@pytest.mark.integration
def test_get_role_success(client, auth_header_admin: dict):
    """Test role retrieval by ID.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
    """
    # Create a role
    name = _uniq("rrhh")
    created = client.post(
        "/api/v1/roles/",
        json={"name": name, "description": "Human Resources"},
        headers=auth_header_admin,
    ).get_json()
    role_id = int(created["id"])

    # Get role by ID
    resp = client.get(f"/api/v1/roles/{role_id}", headers=auth_header_admin)
    assert resp.status_code == 200

    got = resp.get_json()
    assert got["id"] == role_id
    assert got["name"] == name


@pytest.mark.integration
def test_update_role_success(client, auth_header_admin: dict):
    """Test role update with valid data.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
    """
    # Create a role
    name = _uniq("rrhh")
    created = client.post(
        "/api/v1/roles/",
        json={"name": name, "description": "Human Resources"},
        headers=auth_header_admin,
    ).get_json()
    role_id = int(created["id"])

    # Update role
    resp = client.put(
        f"/api/v1/roles/{role_id}",
        json={"name": "RRHH", "description": "RRHH Updated"},
        headers=auth_header_admin,
    )
    assert resp.status_code == 200

    updated = resp.get_json()
    assert updated["name"] == "RRHH"
    assert updated["description"] == "RRHH Updated"


@pytest.mark.integration
def test_soft_delete_role_success(client, auth_header_admin: dict):
    """Test role soft-deletion by ID.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
    """
    # Create a role
    name = _uniq("rrhh")
    created = client.post(
        "/api/v1/roles/",
        json={"name": name, "description": "Human Resources"},
        headers=auth_header_admin,
    ).get_json()
    role_id = int(created["id"])

    # Soft-delete role
    resp = client.delete(f"/api/v1/roles/{role_id}", headers=auth_header_admin)
    assert resp.status_code == 200

    deleted = resp.get_json()
    assert deleted["state"] is False

    # Verify: listing active roles should not include deleted
    resp2 = client.get("/api/v1/roles/", headers=auth_header_admin)
    assert resp2.status_code == 200
    assert isinstance(resp2.get_json(), list)
    assert all(r.get("state") is True for r in resp2.get_json())


@pytest.mark.integration
def test_create_role_requires_name(client, auth_header_admin: dict):
    """Test role creation fails when name is missing.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The admin authorization header.
    """
    resp = client.post(
        "/api/v1/roles/",
        json={"name": ""},
        headers=auth_header_admin,
    )
    assert resp.status_code == 400
    data = resp.get_json()
    assert data and data.get("message") == "name is required"
