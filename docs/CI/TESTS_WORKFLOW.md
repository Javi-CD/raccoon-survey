# Pipeline de Tests (GitHub Actions)

Este documento describe el workflow de GitHub Actions que ejecuta la suite de tests en cada `push` y `pull_request` hacia las ramas `develop` y `features`.

## Archivo de configuración

- Ruta: `.github/workflows/tests.yml`
- Runner: `ubuntu-latest`
- Versión de Python: `3.11`
- Cache de dependencias: `pip` usando `requirements.txt`

## Disparadores

- `push` a:
  - `develop`
  - `features`
  - `features/**` (subramas dentro de `features`)
- `pull_request` con base en:
  - `develop`
  - `features`
  - `features/**`

## Pasos principales

1. Checkout del repositorio (`actions/checkout@v4`).
2. Configuración de Python (`actions/setup-python@v5`) con `python-version: 3.11` y cache de `pip`.
3. Instalación de dependencias:
   ```bash
   uv sync

   # O usando pip
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Ejecución de la suite de tests:
   ```bash
   pytest -q
   ```

## Personalización

- Para añadir más versiones de Python (matriz), modifica el job `tests` con `strategy.matrix.python-version`.
- Para incluir linters (por ejemplo `flake8` o `ruff`) o validación de commits, agrega pasos adicionales antes de `pytest`.
- Para ajustar las ramas de disparo, edita las secciones `on.push.branches` y `on.pull_request.branches`.

## Referencias

- Workflow creado automáticamente y mantenido en `.github/workflows/tests.yml`.
- Documentación adicional de CI en `docs/CI/` (linting, validación de commits).

