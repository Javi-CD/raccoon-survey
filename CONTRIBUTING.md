# Contributing Guide — Raccoon Survey

Thank you for your interest in contributing. This guide summarizes how to prepare the environment, the recommended workflow, and the quality standards to keep the project healthy and secure.

---

## Table of Contents
- [Principles](#principles)
- [Requirements](#requirements)
- [Local setup](#local-setup)
  - [Backend](#backend)
  - [Frontend](#frontend)
  - [Run development server](#run-development-server)
- [Branch flow](#branch-flow)
- [Commit conventions](#commit-conventions)
- [Lint and formatting](#lint-and-formatting)
  - [Backend](#backend-lint-and-formatting)
  - [Frontend](#frontend-lint-and-formatting)
- [Tests](#tests)
- [Testing Guide](#testing-guide)
- [Documentation](#documentation)
- [Database migrations](#database-migrations)
- [Pull Request checklist](#pull-request-checklist)
- [Changelog and releases](#changelog-and-releases)
- [Code standards](#code-standards)
- [Issue and security reporting](#issue-and-security-reporting)
- [License](#license)

---

## Principles
- Respect and collaboration ([`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)).
- Security ([`SECURITY.md`](./SECURITY.md)).
- Small, well-tested changes.
- Documentation and change traceability.

---

## Requirements
- `Python 3.11+`, `uv`.
- `Node.js 18+` and `npm`.
- Git.

---

## Local setup

```bash

# Clone repository
git clone https://github.com/Javi-CD/raccoon-survey.git

# Copy .env.example to .env
cp .env.example .env

# Adjust variables in .env (JWT, CORS, DB, etc.)
```

### Backend

```bash

# Install dependencies
uv sync

# Using pip

python -m venv .venv && .\\.venv\\Scripts\\Activate.ps1 && pip install -r requirements.txt

```

### Frontend

```bash

# Install dependencies
npm install

```

### Run development server

```bash

uv run main.py

# Alternative
python main.py

```

Verify the development server is running correctly.

```bash

curl --location http://localhost:3000/api/v1/openapi.json
curl --location http://localhost:3000/api/v1/health

```

> If the ``PORT`` variable is not defined in ``.env``, the default is ``3000``.

---

## Branch flow
- `develop` branch: stable.
- Create a branch per change:
  ```plaintext

  type/branch-name

  examples:

  feature/auth-middlewares
  fix/truncate-database
  ```
- Use `merge --no-ff` in feature branches and test functionality before opening a pull request to `develop`.


---

## Commit conventions
- Use Conventional Commits:
  - `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
- Examples:
  - `feat(api): add refresh token to /auth/refresh`
  - `fix(ui): fix redirect on /dashboard without session`
- `husky` and `commitlint` hooks validate messages (see [`commitlint.config.js`](./commitlint.config.js) and [`husky`](./.husky/)).

---

## Lint and formatting
- Python: see [`docs/CI/PYTHON_LINTING.md`](./docs/CI/PYTHON_LINTING.md).
- JavaScript/CSS: configure and use:
  - ESLint: `npx eslint .` (see [`eslintrc.js`](./.eslintrc.js))
  - Prettier: `npx prettier --check .` (see [`prettierrc.js`](./.prettierrc.js))
  - Stylelint: `npx stylelint "src/ui/**/*.css"` (see [`stylelintrc.js`](./.stylelintrc.js))

---

## Tests
- Location: `test/` (`unitests/`, `integration/`, `e2e/`).
- Run: `pytest`.
- Add tests for new functionality and error cases.

---

## Testing Guide
- Full documentation: [`docs/Testing/README.md`](./docs/Testing/README.md).
- Includes how to run the full suite, coverage, subsets (unit/integration/e2e), environment variables, and tips.

---

## Documentation
- Security: [`docs/Security/README.md`](./docs/Security/README.md).
- API: [`docs/API/README.md`](./docs/API/README.md) and `src/core/openapi.json`.
- Database: [`docs/Database/schema_db.md`](./docs/Database/schema_db.md) and [`docs/Database/MIGRATIONS.md`](./docs/Database/MIGRATIONS.md).
- Sphinx: [`docs/source/index.rst`](./docs/source/index.rst), local build: `docs\make.bat html`.
- Swagger: `curl --location http://localhost:<PORT>/docs`
- Postman collection link: [Click Here!](https://www.postman.com/javier-prez/workspace/raccoon-surveys-api/collection/43954198-06d34335-49ff-4778-af25-1676be326cb6?action=share&creator=43954198&active-environment=43954198-cabc9e0c-dc39-401d-87b8-72ac404ce002)

---

## Database migrations
- Configuration: `alembic.ini`.
- Follow the guide: [`docs/Database/MIGRATIONS.md`](./docs/Database/MIGRATIONS.md).
- Include PR notes about schema changes.

---

## Pull Request checklist
- Lint and formatting pass (ESLint/Prettier/Stylelint/Python).
- Tests added and/or updated; `pytest` is green.
- Documentation updated (README/Docs/API/DB/Security if applicable).
- Limited scope changes with clear motivation.
- No secrets or credentials in the commit.
- CI green: `docs.yml`, `release.yml`, `changelog.yml`.

---

## Changelog and releases
- [`CHANGELOG.md`](./CHANGELOG.md) is maintained via CI; do not edit manually.
- Versioning and packages: see [`scripts/update_package_version.py`](./scripts/update_package_version.py), [`scripts/update_pyproject_version.py`](./scripts/update_pyproject_version.py), [`scripts/update_package_lock.js`](./scripts/update_package_lock.js).
- Release pipeline: [`release.yml`](./.github/workflows/release.yml).

---

## Code standards
- Python: static typing where possible, small functions, avoid cryptic names.
- Flask: routes in `src/core/routes/`, services in `src/core/services/`, utilities in `src/core/utils/`.
- UI: routes/guards in `src/ui/routes/`, avoid complex logic in templates.
- Security: use `role_required` and `user_required` decorators, and respect JWT/blocklist.

---

## Issue and security reporting
- Bugs: open an issue with reproducible steps and relevant logs.
- Vulnerabilities: follow [`SECURITY.md`](./SECURITY.md) (responsible disclosure). No exploits in production.

---

## License
- The project is under `GPLv3` (see [`LICENSE`](./LICENSE)).
- By contributing, you accept that your code is published under the same license.

---

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./src/ui/static/img/raccoon_survey_white.png" />
  <source media="(prefers-color-scheme: light)" srcset="./src/ui/static/img/raccoon_survey.png" />
  <img src="./src/ui/static/img/raccoon_survey.png" alt="Raccoon Survey Logo" width="100" height="100" />
</picture>   

© Copyright 2025, Raccoon Survey Team.

</div>
