# Guía de Testing

Esta guía resume cómo ejecutar la suite de tests y cómo está organizada la carpeta `test/` del proyecto.

## Requisitos

- Python 3.11
- Dependencias definidas en `requirements.txt`

Instalación:

```bash
uv sync

# O Usando Pip
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecutar la suite completa

```bash
pytest -q
```

## Ejecutar con cobertura

Requisitos:
- Instala el plugin: `pip install pytest-cov`
- Configuración de cobertura: `.coveragerc` en la raíz del proyecto (``source=src`` y branch coverage).

Comandos:
```bash
pytest --cov=src --cov-report=term-missing:skip-covered --cov-report=html --cov-report=xml
```

Resultados:
- `coverage.xml`: reporte en formato XML para integraciones externas.
- `htmlcov/`: reporte HTML navegable con detalle de líneas cubiertas y faltantes.

## Ejecutar subconjuntos

- Solo integración:
  ```bash
  pytest -q test/integration
  ```
- Solo E2E:
  ```bash
  pytest -q test/e2e
  ```
- Solo unitarios:
  ```bash
  pytest -q test/unitests
  ```

## Organización de tests

- `test/integration/`: pruebas de endpoints de la API (CRUD, validaciones, estados).
- `test/e2e/`: flujos completos (tokens, anonimato, resúmenes por equipo).
- `test/unitests/`: pruebas de servicios internos y utilidades.
- `test/utils/helpers.py`: helpers compartidos para crear equipos, encuestas, preguntas, generar tokens y utilidades de expiración.

## Variables de entorno

- Archivo base: `.env.example`
- Ajusta valores necesarios para el entorno de ejecución.

## Consejos

- Los tests usan fixtures para inicializar la aplicación y aislar la base de datos por prueba.
- Usa los helpers compartidos para evitar duplicar lógica (por ejemplo `_create_team`, `_create_survey`, `_create_question`, `_generate_token`).
- Para generar tokens, provee `expires_at` en formato ISO (usa `expires_at_future()` o `expires_at_past()`).

