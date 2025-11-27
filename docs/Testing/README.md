# Testing Guide

This guide summarizes how to run the test suite and how the project's `test/` folder is organized.

---

## Requirements

- Python 3.11
- Dependencies defined in `requirements.txt`

Installation:

```bash
uv sync

# Using Pip
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Run the full suite

```bash
pytest -q
```

---

## Run with coverage

Requirements:
- Install the plugin:
  ```bash
  uv add pytest-cov
  
  # Using pip
  pip install pytest-cov
  ```

- Coverage configuration: `.coveragerc` at the project root (``source=src`` and branch coverage).

Commands:
```bash
pytest --cov=src --cov-report=term-missing:skip-covered --cov-report=html --cov-report=xml
```

Results:
- `coverage.xml`: XML report for external integrations.
- `htmlcov/`: navigable HTML report showing covered and missing lines.

---

## Run subsets

- Integration only:
  ```bash
  pytest -q test/integration
  ```
- E2E only:
  ```bash
  pytest -q test/e2e
  ```
- Unit tests only:
  ```bash
  pytest -q test/unitests
  ```

---

## Test organization

- `test/integration/`: API endpoint tests (CRUD, validations, states).
- `test/e2e/`: full flows (tokens, anonymity, team summaries).
- `test/unitests/`: internal service and utility tests.
- `test/utils/helpers.py`: shared helpers to create teams, surveys, questions, generate tokens, and expiration utilities.

---

## Environment variables

- Base file: `.env.example`
- Adjust values required for your execution environment.

---

## Tips

- Tests use fixtures to initialize the application and isolate the database per test.
- Use shared helpers to avoid duplicating logic (for example `_create_team`, `_create_survey`, `_create_question`, `_generate_token`).
- To generate tokens, provide `expires_at` in ISO format (use `expires_at_future()` or `expires_at_past()`).

---
