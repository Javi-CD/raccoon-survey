# Tests Pipeline (GitHub Actions)

This document describes the GitHub Actions workflow that runs the test suite on every `push` and `pull_request` to the `develop` and `features` branches, including coverage measurement with `pytest-cov`.

## Configuration File

- Path: `.github/workflows/tests.yml`
- Runner: `ubuntu-latest`
- Python version: `3.11`
- Dependency cache: `pip` using `requirements.txt`
- Coverage configured via `.coveragerc` (source `src`, branch coverage, basic exclusions)

## Triggers

- `push` to:
  - `develop`
  - `features`
  - `features/**` (sub-branches under `features`)
- `pull_request` targeting:
  - `develop`
  - `features`
  - `features/**`

## Main Steps

1. Checkout the repository (`actions/checkout@v4`).
2. Set up Python (`actions/setup-python@v5`) with `python-version: 3.11` and `pip` cache.
3. Install dependencies (includes coverage plugin):
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   pip install pytest-cov
   ```
4. Run the test suite with coverage:
   ```bash
   pytest --cov=src --cov-report=term-missing:skip-covered \
          --cov-report=xml:coverage.xml \
          --cov-report=html
   ```
5. Publish coverage artifacts:
   - `coverage.xml` (for external integrations)
   - `htmlcov` folder (navigable report)

## Customization

- To add more Python versions (matrix), modify the `tests` job with `strategy.matrix.python-version`.
- To include linters (e.g., `flake8` or `ruff`) or commit validation, add steps before `pytest`.
- To adjust trigger branches, edit `on.push.branches` and `on.pull_request.branches` sections.

## Generated Artifacts

- `coverage.xml`: XML report compatible with coverage services.
- `htmlcov/`: HTML report summarizing covered and missed lines.

## Local Execution with Coverage

```bash
pytest --cov=src --cov-report=term-missing:skip-covered --cov-report=xml --cov-report=html
```
Notes:
- Requires `pytest-cov` installed (`uv add pytest-cov`).
- Coverage configuration in `.coveragerc`.

## References

- Workflow created automatically and maintained in `.github/workflows/tests.yml`.
- Additional CI documentation in `docs/CI/` (linting, commit validation).

## Environment Variables for CI (Secrets and Variables)

The tests workflow requires certain environment variables so that the app configuration (`BaseConfig`) does not fail upon import. In CI they are managed as follows:

### What to Create in GitHub

- Secrets (sensitive values):
  - `SECRET_KEY`
  - `JWT_SECRET_KEY`
  - `DATABASE_URL`
  - `DEFAULT_USER_ADMIN_PASSWORD`

- Variables (non-sensitive):
  - `DEFAULT_USER_ADMIN_EMAIL`
  - `DEFAULT_USER_ADMIN_NAME`

### Where to Create Them

- In the repository: `Settings → Secrets and variables → Actions`.
  - Secrets: `New repository secret`
  - Variables: `New repository variable`

### How They Are Referenced in the Workflow

`env` block of the `tests` job in `.github/workflows/tests.yml`:

```yaml
jobs:
  tests:
    runs-on: ubuntu-latest
    env:
      FLASK_ENV: testing
      SECRET_KEY: ${{ secrets.SECRET_KEY }}
      JWT_SECRET_KEY: ${{ secrets.JWT_SECRET_KEY }}
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      DEFAULT_USER_ADMIN_EMAIL: ${{ vars.DEFAULT_USER_ADMIN_EMAIL }}
      DEFAULT_USER_ADMIN_PASSWORD: ${{ secrets.DEFAULT_USER_ADMIN_PASSWORD }}
      DEFAULT_USER_ADMIN_NAME: ${{ vars.DEFAULT_USER_ADMIN_NAME }}
```

### Recommended Values

- `DATABASE_URL` in CI:
  - `sqlite:///./test.db` (persistent during the job and simple to use), or
  - `sqlite:///:memory:` (in-memory only; may reset between processes).
- Use values different from production for `SECRET_KEY` and `JWT_SECRET_KEY`.

### Security Considerations

- Workflows triggered from forks do not have access to `secrets.*` by default. For external PRs, run tests on `push` or evaluate `pull_request_target` with caution.
- Avoid exposing sensitive values in logs; `${{ secrets.* }}` references already mask content.

### Local Development

- For local development, you can copy `.env.example` to `.env` and fill in the required values.
- Local tests can also work if you define these variables in your shell environment or in the `.env` file.

