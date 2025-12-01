Testing Guide
=============

Summary
-------
How to run the test suite and how the tests folder is organized.

Requirements
------------
- Python 3.11
- Dependencies from ``pyproject.toml``

Installation
------------
.. code-block:: bash

   # Install dependencies
   uv sync

   # Alternative
   python -m venv .venv && source .venv/bin/activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt

Full Run
--------
.. code-block:: bash

   pytest -q

Subsets
-------
- Integration:

  .. code-block:: bash

     pytest -q test/integration

- E2E:

  .. code-block:: bash

     pytest -q test/e2e

- Unit tests:

  .. code-block:: bash

     pytest -q test/unitests

Structure
---------
- ``test/integration``: API endpoint tests.
- ``test/e2e``: full flows (e.g., anonymity, token export).
- ``test/unitests``: internal services and utilities.
- ``test/utils/helpers.py``: shared helpers (teams, surveys, questions, tokens, expirations).

Key helpers 
----------------------
- Create team: ``_create_team(client, auth_header_admin) -> dict``
- Create survey: ``_create_survey(client, auth_header_admin, team_id) -> dict``
- Crear pregunta: ``_create_question(client, auth_header_admin, survey_id, ...) -> dict``
- Generar token: ``_generate_token(client, auth_header_admin, survey_id, expires_at=...) -> dict``
- Utilidades de expiración: ``expires_at_future()``, ``expires_at_past()``

Environment Config
--------------------
- Base file: ``.env.example`` 

.. code-block:: text

   # *******************
   # * Database Config *
   # *******************
   DATABASE_URL=postgresql://user:password@localhost:5432/raccoon_survey_db
   DATABASE_ECHO=0

   # ****************
   # * Flask Config *
   # ****************
   FLASK_DEBUG=1
   FLASK_ENV=development

   # *****************
   # * Server Config *
   # *****************
   HOST=0.0.0.0
   PORT=3000
   DEBUG=True
   CORS_ORIGINS=http://localhost:3000

   # ***************
   # * JWT Config *
   # **************
   JWT_SECRET_KEY=
   JWT_ACCESS_TOKEN_EXPIRES=900
   JWT_REFRESH_TOKEN_EXPIRES=2592000

   # ***************
   # * Log Config *
   # ***************
   LOG_LEVEL=development

   # * ***************************
   # * Default Admin Credentials *
   # * ***************************
   DEFAULT_USER_ADMIN_NAME=
   DEFAULT_USER_ADMIN_EMAIL=
   DEFAULT_USER_ADMIN_PASSWORD=

   # * **************************
   # * Cleanup scheduler Config *
   # * **************************
   CLEANUP_RUN_ON_START=1
   CLEANUP_CRON_HOUR=3
   CLEANUP_CRON_MINUTE=0

- Set values ​​required for the local execution environment.

.. code-block:: bash

   # Copy example file
   cp .env.example .env

.. note::
   The tests isolate the database per test using fixtures defined in ``test/integration/conftest.py`` and ``test/conftest.py``.

.. tip::
   Use the shared helpers to avoid duplication and maintain consistency between test cases.

