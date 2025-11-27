# Pipeline de Tests (GitHub Actions)

Este documento describe el workflow de GitHub Actions que ejecuta la suite de tests en cada `push` y `pull_request` hacia las ramas `develop` y `features`, incluyendo medición de cobertura con `pytest-cov`.

## Archivo de configuración

- Ruta: `.github/workflows/tests.yml`
- Runner: `ubuntu-latest`
- Versión de Python: `3.11`
- Cache de dependencias: `pip` usando `requirements.txt`
- Cobertura configurada vía `.coveragerc` (origen `src`, branch coverage, exclusiones básicas)

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
3. Instalación de dependencias (incluye plugin de cobertura):
   ```bash
   uv sync

   # O usando pip
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   pip install pytest-cov
   ```
4. Ejecución de la suite de tests con cobertura:
   ```bash
   pytest --cov=src --cov-report=term-missing:skip-covered \
          --cov-report=xml:coverage.xml \
          --cov-report=html
   ```
5. Publicación de artefactos de cobertura:
   - `coverage.xml` (para integraciones externas)
   - Carpeta `htmlcov` (reporte navegable)

## Personalización

- Para añadir más versiones de Python (matriz), modifica el job `tests` con `strategy.matrix.python-version`.
- Para incluir linters (por ejemplo `flake8` o `ruff`) o validación de commits, agrega pasos adicionales antes de `pytest`.
- Para ajustar las ramas de disparo, edita las secciones `on.push.branches` y `on.pull_request.branches`.

## Artefactos generados

- `coverage.xml`: reporte en formato XML compatible con servicios de cobertura.
- `htmlcov/`: reporte HTML navegable que resume líneas cubiertas y faltantes.

## Ejecución local con cobertura

```bash
pytest --cov=src --cov-report=term-missing:skip-covered --cov-report=xml --cov-report=html
```
Notas:
- Requiere `pytest-cov` instalado (`pip install pytest-cov`).
- Configuración de cobertura en `.coveragerc`.

## Referencias

- Workflow creado automáticamente y mantenido en `.github/workflows/tests.yml`.
- Documentación adicional de CI en `docs/CI/` (linting, validación de commits).

