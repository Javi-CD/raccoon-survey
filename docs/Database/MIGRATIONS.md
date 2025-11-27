# Database Migrations (Alembic)

This document explains how migrations are implemented in the project and how to use them in development, CI, and production.

## Table of Contents
- [Overview](#overview)
- [How It Is Implemented in the Application](#how-it-is-implemented-in-the-application)
- [Prerequisites](#prerequisites)
- [Alembic Basic Commands](#alembic-basic-commands)
- [Typical Workflow (Dev)](#typical-workflow-dev)
- [Integration with Flask and Configuration](#integration-with-flask-and-configuration)
- [Migrations Directory](#migrations-directory)
- [Data Seeding (Optional)](#data-seeding-optional)
- [CI/CD and Deployment](#cicd-and-deployment)
- [Notes and Considerations](#notes-and-considerations)
- [Common Problems](#common-problems)
- [Quick Examples (PowerShell)](#quick-examples-powershell)

---

## Overview

- Tool: `Alembic` on top of `SQLAlchemy`.
- ORM: models in `src/core/models` (e.g., `User`, `Survey`, `Question`, etc.).
- Configuration: `alembic.ini` and Flask environment via `create_app()`.
- Script location: `src/core/database/migrations/`.
- Target metadata for autogenerate: `db.metadata` from `src/core/database/__init__.py`.

---

## How It Is Implemented in the Application

- `src/core/database/__init__.py` exposes `db: SQLAlchemy` used by all models.

- `src/core/__init__.py` defines `create_app()`, which:
  - Loads configuration from `src/core/config.py` (includes `DATABASE_URL`).
  - Initializes `SQLAlchemy` (`db.init_app(app)`).

- `alembic.ini` points to `script_location = src/core/database/migrations` and uses `sqlalchemy.url`.

- `src/core/database/migrations/env.py`:
  - Imports `create_app()` to read Flask `SQLALCHEMY_DATABASE_URI`.
  - Sets `config.set_main_option("sqlalchemy.url", db_url)`.
  - Defines `target_metadata = db.metadata` for `--autogenerate`.

- Existing revisions (examples):
  - `31cd4e25f1e6_create_core_tables.py`: creates base tables (`roles`, `teams`, `users`, `surveys`, `questions`, `survey_tokens`, `responses`).
  - `5dfb7cd4abc5_add_audit_categories_question_categories.py`: adds `audit_logs`, `categories`, `question_categories` and indexes.

---

## Prerequisites

Key variables table:

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | Connection URL used by Alembic | `postgresql+psycopg2://user:pass@localhost:5432/raccoon_survey` |
| `FLASK_ENV` | Runtime environment | `development` |
| `DATABASE_ECHO` | Log SQL to console | `1` |

### How to define `DATABASE_URL`
  
 - PowerShell (Windows):
    
    ```powershell
    $env:DATABASE_URL = "postgresql+psycopg2://user:pass@localhost:5432/raccoon_survey"
    ```
- Bash (Linux/macOS):
    
```bash
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/raccoon_survey"
```

---

## Alembic Basic Commands

- Current state
- History
- Create migration (autogenerate)
- Upgrade
- Downgrade
- Stamp

<br/>

| Command | Purpose | Example |
|---|---|---|
| `alembic current` | Show currently applied revision | `alembic current` |
| `alembic history --verbose` | Show revision history | `alembic history --verbose` |
| `alembic revision --autogenerate -m "<message>"` | Create migration from model changes | `alembic revision --autogenerate -m "add new field"` |
| `alembic upgrade head` | Apply migrations up to latest | `alembic upgrade head` |
| `alembic upgrade <revision_id>` | Apply up to a specific revision | `alembic upgrade 31cd4e25f1e6` |
| `alembic downgrade -1` | Revert one migration | `alembic downgrade -1` |
| `alembic downgrade base` | Return to initial state | `alembic downgrade base` |
| `alembic stamp head` | Set state without running migrations | `alembic stamp head` |

<details>
 <summary><b>Quick examples by shell</b></summary>
  
  - PowerShell:
    
    ```powershell
    alembic revision --autogenerate -m "add audit metadata"
    alembic upgrade head
    ```
  - Bash:
    
    ```bash
    alembic revision --autogenerate -m "add audit metadata"
    alembic upgrade head
    ```
</details>

<br/>

1. Modify/add models in `src/core/models` (columns, indexes, relationships).

2. Generate a migration:
   - `alembic revision --autogenerate -m "add new field to Question"`

3. Review the file in `src/core/database/migrations/versions/` and adjust manually if needed.

4. Apply migrations:
   - `alembic upgrade head`

5. Verify the app and/or run tests.

---

## Integration with Flask and Configuration


Key files table:

| File | Role |
|---|---|
| `src/core/config.py` | Exposes `DATABASE_URL` and SQLAlchemy options |
| `src/core/__init__.py` | Defines `create_app()` and initializes `db` |
| `src/core/database/migrations/env.py` | Sets `sqlalchemy.url` and `target_metadata` |
| `alembic.ini` | Script location and Alembic parameters |

## Migrations Directory
Structure and purpose:

| Path | Description |
|---|---|
| `src/core/database/migrations/env.py` | Bridge Alembic ↔ Flask/SQLAlchemy (`db.metadata`) |
| `src/core/database/migrations/script.py.mako` | Template for new revisions |
| `src/core/database/migrations/versions/` | Folder with versioned migrations |
| `src/core/database/migrations/README` | Internal notes |

---

## Data Seeding (Optional)

Main functions:

| Function | Purpose |
|---|---|
| `get_or_create_role` | Create/get initial role |
| `get_or_create_team` | Create/get team |
| `get_or_create_user` | Temporary admin user and relationships |
| `get_or_create_category` | Categories for questions |
| `get_or_create_survey` | Example surveys |
| `get_or_create_question` | Questions linked to surveys |

---

## Common Problems

<details>
  <summary>`sqlalchemy.url` not found</summary>
  
  - Cause: `DATABASE_URL` is not defined.
  - Solution: Export `DATABASE_URL` and rerun:
    
    ```powershell
    $env:DATABASE_URL = "postgresql+psycopg2://user:pass@localhost:5432/raccoon_survey"
    alembic current
    ```
</details>

<br/>

<details>
  <summary>Autogenerate does not detect changes</summary>
  
  - Cause: the model is not imported by `src/core/models/__init__.py`.
  - Solution: make sure it is imported and run:
    
    ```bash
    alembic revision --autogenerate -m "sync models"
    ```
</details>

<br/>

<details>
  <summary>Import error in `env.py`</summary>
  
  - Cause: Alembic executed outside the repo root.
  - Solution: run from the repo root or adjust paths in `alembic.ini` (`%(here)s`).
</details>

<br/>

---

<div align="center">

© Copy. 2025 Raccoon Survey.

</div>
