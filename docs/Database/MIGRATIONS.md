# Migraciones de Base de Datos (Alembic)

Este documento explica cómo están implementadas las migraciones en el proyecto y cómo usarlas en desarrollo, CI y producción.

## Tabla de Contenidos
- [Visión General](#visión-general)
- [Cómo está implementado en el programa](#cómo-está-implementado-en-el-programa)
- [Prerrequisitos](#prerrequisitos)
- [Comandos Básicos de Alembic](#comandos-básicos-de-alembic)
- [Flujo de Trabajo Típico (Dev)](#flujo-de-trabajo-típico-dev)
- [Integración con Flask y Configuración](#integración-con-flask-y-configuración)
- [Directorio de Migraciones](#directorio-de-migraciones)
- [Semillas de Datos (Opcional)](#semillas-de-datos-opcional)
- [CI/CD y Despliegue](#cicd-y-despliegue)
- [Notas y Consideraciones](#notas-y-consideraciones)
- [Problemas Comunes](#problemas-comunes)
- [Ejemplos Rápidos (PowerShell)](#ejemplos-rápidos-powershell)

---

## Visión General


- Herramienta: `Alembic` sobre `SQLAlchemy`.
- ORM: modelos en `src/core/models` (p. ej. `User`, `Survey`, `Question`, etc.).
- Configuración: `alembic.ini` y entorno Flask via `create_app()`.
- Ubicación de scripts: `src/core/database/migrations/`.
- Metadata objetivo para autogeneración: `db.metadata` de `src/core/database/__init__.py`.

---

## Cómo está implementado en el programa

- `src/core/database/__init__.py` expone `db: SQLAlchemy` usado por todos los modelos.

- `src/core/__init__.py` define `create_app()`, que:
  - Carga configuración desde `src/core/config.py` (incluye `DATABASE_URL`).
  - Inicializa `SQLAlchemy` (`db.init_app(app)`).

- `alembic.ini` apunta a `script_location = src/core/database/migrations` y usa `sqlalchemy.url`.

- `src/core/database/migrations/env.py`:
  - Importa `create_app()` para leer `SQLALCHEMY_DATABASE_URI` de Flask.
  - Establece `config.set_main_option("sqlalchemy.url", db_url)`.
  - Define `target_metadata = db.metadata` para `--autogenerate`.

- Revisions existentes (ejemplos):
  - `31cd4e25f1e6_create_core_tables.py`: crea tablas base (`roles`, `teams`, `users`, `surveys`, `questions`, `survey_tokens`, `responses`).
  - `5dfb7cd4abc5_add_audit_categories_question_categories.py`: agrega `audit_logs`, `categories`, `question_categories` e índices.

---

## Prerrequisitos

Tabla de variables clave:

| Variable | Descripción | Ejemplo |
|---|---|---|
| `DATABASE_URL` | URL de conexión usada por Alembic | `postgresql+psycopg2://user:pass@localhost:5432/raccoon_survey` |
| `FLASK_ENV` | Entorno de ejecución | `development` |
| `DATABASE_ECHO` | Log de SQL en consola | `1` |

### Como definir la variable `DATABASE_URL`
  
 - PowerShell (Windows):
    
    ```powershell
    $env:DATABASE_URL = "postgresql+psycopg2://user:pass@localhost:5432/raccoon_survey"
    ```
- Bash (Linux/macOS):
    
```bash
export DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/raccoon_survey"
```

---

## Comandos Básicos de Alembic

- Estado actual
- Historial
- Crear migración (autogenerate)
- Upgrade
- Downgrade
- Stamp

<br/>

| Comando | Uso | Ejemplo |
|---|---|---|
| `alembic current` | Mostrar revisión aplicada actualmente | `alembic current` |
| `alembic history --verbose` | Mostrar historial de revisiones | `alembic history --verbose` |
| `alembic revision --autogenerate -m "<mensaje>"` | Crear migración desde cambios en modelos | `alembic revision --autogenerate -m "add new field"` |
| `alembic upgrade head` | Aplicar migraciones hasta la última | `alembic upgrade head` |
| `alembic upgrade <revision_id>` | Aplicar hasta una revisión específica | `alembic upgrade 31cd4e25f1e6` |
| `alembic downgrade -1` | Revertir una migración | `alembic downgrade -1` |
| `alembic downgrade base` | Volver al estado inicial | `alembic downgrade base` |
| `alembic stamp head` | Marcar estado sin ejecutar migraciones | `alembic stamp head` |

<details>
 <summary><b>Ejemplos rápidos por shell</b></summary>
  
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

1. Modifica/añade modelos en `src/core/models` (columnas, índices, relaciones).

2. Genera una migración:
   - `alembic revision --autogenerate -m "add new field to Question"`

3. Revisa el archivo en `src/core/database/migrations/versions/` y ajusta manualmente si hace falta.

4. Aplica migraciones:
   - `alembic upgrade head`

5. Verifica la app y/o corre tests.

---

## Integración con Flask y Configuración


Tabla de archivos clave:

| Archivo | Rol |
|---|---|
| `src/core/config.py` | Expone `DATABASE_URL` y opciones SQLAlchemy |
| `src/core/__init__.py` | Define `create_app()` e inicializa `db` |
| `src/core/database/migrations/env.py` | Configura `sqlalchemy.url` y `target_metadata` |
| `alembic.ini` | Ubicación de scripts y parámetros Alembic |

## Directorio de Migraciones
Estructura y propósito:

| Ruta | Descripción |
|---|---|
| `src/core/database/migrations/env.py` | Puente Alembic ↔ Flask/SQLAlchemy (`db.metadata`) |
| `src/core/database/migrations/script.py.mako` | Plantilla de nuevas revisiones |
| `src/core/database/migrations/versions/` | Carpeta con migraciones versionadas |
| `src/core/database/migrations/README` | Notas internas |

---

## Semillas de Datos (Opcional)

Funciones principales:

| Función | Propósito |
|---|---|
| `get_or_create_role` | Crear/obtener rol inicial |
| `get_or_create_team` | Crear/obtener equipo |
| `get_or_create_user` | Usuario admin temporal y relaciones |
| `get_or_create_category` | Categorías para preguntas |
| `get_or_create_survey` | Encuestas de ejemplo |
| `get_or_create_question` | Preguntas vinculadas a encuestas |

---

## Problemas Comunes

<details>
  <summary>No se encuentra `sqlalchemy.url`</summary>
  
  - Causa: `DATABASE_URL` no está definida.
  - Solución: Exporta `DATABASE_URL` y vuelve a ejecutar:
    
    ```powershell
    $env:DATABASE_URL = "postgresql+psycopg2://user:pass@localhost:5432/raccoon_survey"
    alembic current
    ```
</details>

<br/>

<details>
  <summary>Autogenerate no detecta cambios</summary>
  
  - Causa: el modelo no está importado por `src/core/models/__init__.py`.
  - Solución: asegúrate de importarlo y ejecutar:
    
    ```bash
    alembic revision --autogenerate -m "sync models"
    ```
</details>

<br/>

<details>
  <summary>Error de importación en `env.py`</summary>
  
  - Causa: Alembic ejecutado fuera de la raíz del repo.
  - Solución: ejecuta desde la raíz o ajusta rutas en `alembic.ini` (`%(here)s`).
</details>

<br/>

---

<div align="center">

© Copy. 2025 Raccoon Survey.

</div>