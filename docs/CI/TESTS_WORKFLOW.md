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

## Variables de entorno para CI (Secrets y Variables)

El workflow de tests requiere ciertas variables de entorno para que la configuración de la app (`BaseConfig`) no falle al importarse. En CI se gestionan de la siguiente forma:

### Qué crear en GitHub

- Secrets (valores sensibles):
  - `SECRET_KEY`
  - `JWT_SECRET_KEY`
  - `DATABASE_URL`
  - `DEFAULT_USER_ADMIN_PASSWORD`

- Variables (no sensibles):
  - `DEFAULT_USER_ADMIN_EMAIL`
  - `DEFAULT_USER_ADMIN_NAME`

### Dónde crearlas

- En el repositorio: `Settings → Secrets and variables → Actions`.
  - Secrets: `New repository secret`
  - Variables: `New repository variable`

### Cómo se referencian en el workflow

Bloque `env` del job `tests` en `.github/workflows/tests.yml`:

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

### Recomendaciones de valores

- `DATABASE_URL` en CI:
  - `sqlite:///./test.db` (persistente durante el job y simple de usar), o
  - `sqlite:///:memory:` (solo memoria; puede reiniciarse entre procesos).
- Usa valores distintos a producción para `SECRET_KEY` y `JWT_SECRET_KEY`.

### Consideraciones de seguridad

- Workflows disparados desde forks no tienen acceso a `secrets.*` por defecto. Para PRs externos, ejecuta tests en `push` o evalúa `pull_request_target` con precaución.
- Evita exponer valores sensibles en logs; las referencias `${{ secrets.* }}` ya ocultan el contenido.

### Desarrollo local

- Para desarrollo local, puedes copiar `.env.example` a `.env` y completar los valores requeridos.
- Los tests locales también pueden funcionar si defines estas variables en tu entorno de shell o en el archivo `.env`.

