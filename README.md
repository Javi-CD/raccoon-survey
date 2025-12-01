<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./src/ui/static/img/raccoon_survey_white.png" />
  <source media="(prefers-color-scheme: light)" srcset="./src/ui/static/img/raccoon_survey.png" />
  <img src="./src/ui/static/img/raccoon_survey.png" alt="Raccoon Survey Logo" width="100" height="100" />
</picture>  

# Raccoon Survey

[![License GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)
[![Coverage](https://codecov.io/github/Javi-CD/raccoon-survey/branch/develop/graph/badge.svg)](https://codecov.io/github/Javi-CD/raccoon-survey?branch=develop)
[![Docs Build](https://github.com/Javi-CD/raccoon-survey/actions/workflows/docs.yml/badge.svg?branch=develop)](https://github.com/Javi-CD/raccoon-survey/actions/workflows/docs.yml)
[![Tests](https://github.com/Javi-CD/raccoon-survey/actions/workflows/tests.yml/badge.svg?branch=develop)](https://github.com/Javi-CD/raccoon-survey/actions/workflows/tests.yml)

_Enterprise platform to manage, distribute, and analyze workplace climate through anonymous surveys._

</div>

---

## Table of Contents

<details>

<summary>View table of contents</summary>

<br/>

-  [Setup](#setup)
    - [Requirements](#requirements)
    - [Installation](#installation)
        - [API Dependencies](#api-dependencies)
        - [UI/UX Dependencies](#uiux-dependencies)
    - [Run](#run)
    - [Tests](#tests)
        - [Run all tests](#run-all-tests)
        - [Run specific test](#run-specific-test)
- [Documentation](#documentation)
    - [Documentation of internal modules](#documentation-of-internal-modules)
        - [API](#api)
        - [Database](#database)
        - [Testing](#testing)
        - [Security](#security)
        - [CI/CD](#cicd)
    - [Sphinx](#guide-to-generate-sphinx-documentation)
- [Structure](#structure)
- [Security and Privacy](#security-and-privacy)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [License](#license)

</details>

---

## Setup 

### Requirements
- `Python 3.11+`, `uv (recommended)` or `pip`.
- `Node.js 18+` and `npm`.

- Environment file: copy `/.env.example` to `/.env`.

---

### Installation

Configure variables in `.env`

```bash

copy .env.example .env

```

- #### API Dependencies

```bash

# Install dependencies - Create and activate virtual env automatically
uv sync

# Alternative
python -m venv .venv && .\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt

```

- #### UI/UX Dependencies

```bash
# Install dependencies
npm install
```

---

### Run

```bash

# Run local server
uv run main.py

# Alternative
python main.py

```

> The server will be available on the port defined in `.env` (default `3000`).

- **Base API URL:** `http://localhost:<PORT>/api/v1/`
- **Base UI URL:** `http://localhost:<PORT>/`

---

### Tests

To know the test coverage [Click Here!](https://app.codecov.io/github/Javi-CD/raccoon-survey?branch=develop)

## Run all tests

```bash

uv run pytest -q

# Alternative
python -m pytest -q

```

## Run specific test

```bash

# Run a specific test file
uv run pytest -q tests/test_file.py

# Run a specific test function
uv run pytest -q tests/test_file.py::test_function

```

For more information about the tests, see [`docs/Testing/README.md`](./docs/Testing/README.md).

---

## Documentation

Raccoon Surveys Guide: [Click Here!](https://javi-cd.github.io/raccoon-survey/).

### Documentation of internal modules:

- #### Security
    - Security guide: [`docs/Security/README.md`](./docs/Security/README.md).

- #### API
    - API documentation: [`docs/API/README.md`](./docs/API/README.md).
    - Swagger UI: [`GET /docs`](https://raccoon-survey-production.up.railway.app/docs).
    - Postman collection link: [Click Here!](https://www.postman.com/javier-prez/workspace/raccoon-surveys-api/collection/43954198-06d34335-49ff-4778-af25-1676be326cb6?action=share&creator=43954198&active-environment=43954198-cabc9e0c-dc39-401d-87b8-72ac404ce002)

- #### Database
    - Database schema: [`docs/Database/schema_db.md`](./docs/Database/schema_db.md).
    - Database migrations: [`docs/Database/MIGRATIONS.md`](./docs/Database/MIGRATIONS.md).

- #### CI/CD
    - Change log: [`docs/CI/CHANGELOG_CI.md`](./docs/CI/CHANGELOG_CI.md).
    - Commit validation: [`docs/CI/COMMIT_VALIDATION.md`](./docs/CI/COMMIT_VALIDATION.md).
    - Python linting: [`docs/CI/PYTHON_LINTING.md`](./docs/CI/PYTHON_LINTING.md).

<br />

### Guide to generate Sphinx documentation

<details>

<summary>Generate Sphinx documentation</summary>

<br />

Sphinx documentation: [`docs/source/`](./docs/source/).

- You can generate documentation locally using [`make.bat`](./docs/make.bat).
 
```bash

     make.bat html

 ```

> Output in `docs/_build/html/`

- The changes will be made locally by setting up a server:

```bash
   python -m http.server 8000 -d docs/_build/html
```

> Replace `http://localhost:8000` for the documentation.

</details>


---

## Structure

<details>

<summary>View structure</summary>

```plaintext
raccoon-survey/
|-- .coveragerc
|-- .env.example
|-- .gitignore
|-- .github/
|   |-- workflows/
|   |   |-- changelog.yml
|   |   |-- docs.yml
|   |   `-- release.yml
|   `-- scripts/
|       |-- update_package_lock.js
|       |-- update_package_version.py
|       `-- update_pyproject_version.py
|-- .husky/
|   |-- commit-msg
|   `-- pre-commit
|-- docs/
|   |-- API/
|   |   `-- README.md
|   |-- CI/
|   |   |-- CHANGELOG_CI.md
|   |   |-- COMMIT_VALIDATION.md
|   |   `-- PYTHON_LINTING.md
|   |-- Database/
|   |   |-- MIGRATIONS.md
|   |   `-- schema_db.md
|   |-- Security/
|   |   `-- README.md
|   `-- source/
|       |-- _static/
|       |-- api/
|       |-- conf.py
|       |-- core.rst
|       |-- database.rst
|       |-- extensions.rst
|       |-- index.rst
|       |-- middlewares.rst
|       |-- models.rst
|       |-- modules.rst
|       |-- routes.rst
|       `-- services.rst
|-- src/
|   |-- core/
|   |   |-- __init__.py
|   |   |-- config.py
|   |   |-- openapi.json
|   |   |-- database/
|   |   |-- extensions/
|   |   |-- middlewares/
|   |   |-- models/
|   |   |-- routes/
|   |   |-- services/
|   |   `-- utils/
|   `-- ui/
|       |-- public/
|       |-- routes/
|       |-- static/
|       `-- templates/
|-- test/
|   |-- e2e/
|   |-- integration/
|   `-- unitests/
|-- main.py
|-- package.json
|-- pyproject.toml
|-- pytest.ini
|-- requirements.txt
|-- uv.lock
|-- CODE_OF_CONDUCT.md
|-- LICENSE
|-- SECURITY.md
`-- README.md
```

</details>

---

## Security and Privacy
- Project policy: [`SECURITY.md`](./SECURITY.md).
- JWT, RBAC, blocklist and CORS: [`docs/Security/README.md`](./docs/Security/README.md).
- Best practices and responsible disclosure in [`SECURITY.md`](./SECURITY.md).

---

## Code of Conduct
- Read the [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) to understand our community expectations.

---

## Contributing
Have a look at [`CONTRIBUTING.md`](./CONTRIBUTING.md) and [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) for more information.
- Changes and versions: [`CHANGELOG.md`](./CHANGELOG.md).

---

## License
Distributed under `GPLv3`. See [LICENSE](./LICENSE) for more information.

---

<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./src/ui/static/img/raccoon_survey_white.png" />
  <source media="(prefers-color-scheme: light)" srcset="./src/ui/static/img/raccoon_survey.png" />
  <img src="./src/ui/static/img/raccoon_survey.png" alt="Raccoon Survey Logo" width="100" height="100" />
</picture>   

© Copyright 2025, Raccoon Survey Team.

</div>
