# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

from test.utils.helpers import _uniq


def test_list_categories_empty(client, auth_header_admin: dict):
    """Test listing categories when no categories exist.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    res = client.get("/api/v1/categories/", headers=auth_header_admin)
    assert res.status_code == 200
    assert res.get_json() == []


def test_create_category_success(client, auth_header_admin: dict):
    """Test creating a category successfully.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name = _uniq()
    payload = {"name": name, "description": "General surveys"}
    res = client.post("/api/v1/categories/", json=payload, headers=auth_header_admin)
    assert res.status_code == 201

    data = res.get_json()
    assert data["id"] > 0
    assert data["name"] == name
    assert data["description"] == "General surveys"
    assert data["state"] is True


def test_get_category_success(client, auth_header_admin: dict):
    """Test getting a category by ID successfully.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name = _uniq()
    res_create = client.post(
        "/api/v1/categories/",
        json={"name": name, "description": "HR"},
        headers=auth_header_admin,
    )
    assert res_create.status_code == 201
    created = res_create.get_json()

    res_get = client.get(
        f"/api/v1/categories/{created['id']}", headers=auth_header_admin
    )
    assert res_get.status_code == 200

    data = res_get.get_json()
    assert data["id"] == created["id"]
    assert data["name"] == name
    assert data["description"] == "HR"
    assert data["state"] is True


def test_update_category_success(client, auth_header_admin: dict):
    """Test updating a category successfully.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name1 = _uniq()
    res_create = client.post(
        "/api/v1/categories/",
        json={"name": name1, "description": "Old desc"},
        headers=auth_header_admin,
    )
    assert res_create.status_code == 201
    created = res_create.get_json()

    new_name = _uniq()
    res_update = client.put(
        f"/api/v1/categories/{created['id']}",
        json={"name": new_name, "description": "New desc"},
        headers=auth_header_admin,
    )
    assert res_update.status_code == 200

    data = res_update.get_json()
    assert data["name"] == new_name
    assert data["description"] == "New desc"


def test_change_category_state_success(client, auth_header_admin: dict):
    """Test changing the state of a category successfully.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name = _uniq()
    res_create = client.post(
        "/api/v1/categories/",
        json={"name": name, "description": "Ops"},
        headers=auth_header_admin,
    )
    assert res_create.status_code == 201
    created = res_create.get_json()

    res_patch = client.patch(
        f"/api/v1/categories/{created['id']}/state",
        json={"state": False},
        headers=auth_header_admin,
    )
    assert res_patch.status_code == 200
    patched = res_patch.get_json()
    assert patched["state"] is False

    # Verify via GET
    res_get = client.get(
        f"/api/v1/categories/{created['id']}", headers=auth_header_admin
    )
    assert res_get.status_code == 200
    assert res_get.get_json()["state"] is False


def test_create_category_requires_name(client, auth_header_admin: dict):
    """Test creating a category requires a name.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    res = client.post("/api/v1/categories/", json={}, headers=auth_header_admin)
    assert res.status_code == 400
    assert res.get_json()["message"] == "name is required"


def test_update_category_empty_name_rejected(client, auth_header_admin: dict):
    """Test updating a category with an empty name is rejected.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name = _uniq()
    res_create = client.post(
        "/api/v1/categories/",
        json={"name": name, "description": "Finance"},
        headers=auth_header_admin,
    )
    assert res_create.status_code == 201
    created = res_create.get_json()

    res_update = client.put(
        f"/api/v1/categories/{created['id']}",
        json={"name": "  "},
        headers=auth_header_admin,
    )
    assert res_update.status_code == 400
    assert res_update.get_json()["message"] == "name cannot be empty"


def test_update_category_duplicate_name_conflict(client, auth_header_admin: dict):
    """Test updating a category with a duplicate name is rejected.

    Args:
        client (FlaskClient): The test client for the Flask application.
        auth_header_admin (dict): The authentication header for admin access.
    """
    name_a = _uniq("catA")
    name_b = _uniq("catB")
    a = client.post(
        "/api/v1/categories/",
        json={"name": name_a},
        headers=auth_header_admin,
    )
    b = client.post(
        "/api/v1/categories/",
        json={"name": name_b},
        headers=auth_header_admin,
    )
    assert a.status_code == 201 and b.status_code == 201
    cat_b = b.get_json()

    res_update = client.put(
        f"/api/v1/categories/{cat_b['id']}",
        json={"name": name_a},
        headers=auth_header_admin,
    )
    assert res_update.status_code == 409
    assert res_update.get_json()["message"] == "category with same name already exists"
