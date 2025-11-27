# Copyright (C) 2025 Raccoon Survey org
# This file is part of Raccoon Survey.
# Raccoon Survey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License v3 as published by
# the Free Software Foundation.
# See the LICENSE file distributed with this program for details.

import os

from flask import Flask
import pytest

from src.core import create_app
from src.core.database import db


@pytest.fixture(scope="session")
def app() -> Flask:
    """Fixture to create a Flask application instance for testing.

    Returns:
        Flask: The Flask application instance configured for testing.
    """

    os.environ.setdefault(
        "SECRET_KEY",
        "vO2tcwOvaSSnH45zncBgTYqr9wEpZGH2z-OazEexDXFWj3BtQogfXnzJI1lrL03XoaWbVQZWqh7FUsc0OAL1FA",
    )
    os.environ.setdefault(
        "JWT_SECRET_KEY",
        "Y6VwXVypEnlva1KLG1wOmv5W2qN4-0d9kFkOxUsx2bJE9md4kqvbWM4EmOepfcy003BSsgmQiPKJU_4GFFqnpQ",
    )

    overrides = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "DATABASE_URL": "sqlite:///:memory:",
        # Required by BaseConfig
        "DEFAULT_USER_ADMIN_EMAIL": "admin@example.com",
        "DEFAULT_USER_ADMIN_PASSWORD": "adminpass",
        "DEFAULT_USER_ADMIN_NAME": "Admin Test",
    }

    application = create_app(overrides)
    with application.app_context():
        db.create_all()

    yield application

    # Clean up after tests
    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask):
    """Fixture to create a test client for the Flask application.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        FlaskClient: The test client for the Flask application.
    """
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_db(app: Flask):
    """Reset the database before each test to ensure isolation.

    Args:
        app (Flask): The Flask application instance.
    """
    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.create_all()


@pytest.fixture()
def auth_header_admin(app: Flask) -> dict:
    """Fixture to create a dictionary with an admin authorization header.

    Args:
        app (Flask): The Flask application instance.

    Returns:
        dict: A dictionary containing the admin authorization header.
    """
    from flask_jwt_extended import create_access_token

    with app.app_context():
        token = create_access_token(identity="1", additional_claims={"role": "admin"})

    return {"Authorization": f"Bearer {token}"}
