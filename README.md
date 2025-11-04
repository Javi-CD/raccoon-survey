<div align="center">

<img src="./src/ui/static/img/raccoon_survey.png" alt="Raccoon Survey Logo" width="100" height="100">  

# Raccoon Survey

[![License GPLv3](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-339933?logo=node.js)

_Plataforma empresarial para gestionar, distribuir y analizar clima en entorno laborales a travez de encuestas anonimas._

</div>

---


## Indice

<details>

<summary>Ver indice</summary>

<br/>

- [Caracteristicas](#caracteristicas)
- [Requisitos](#requisitos)
- [Instalacion](#instalacion)
- [Ejecucion](#ejecucion)
- [Pruebas](#pruebas)
- [Documentacion](#documentacion)
- [Seguridad](#seguridad)
- [Estructura](#estructura)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

</details>

---

## Caracteristicas
- Autenticacion JWT con roles.
- Revocacion de tokens y proteccion de rutas privadas.
- Gestion de encuestas y respuestas anonimas.
- Documentacion de API y seguridad integrada.

---

## Requisitos
- `Python 3.11+`, `uv (recomendado)` o `pip` .
- `Node.js 18+` y `npm`.

- Archivo de entorno: copia `/.env.example` a `/.env`.

---

## Instalacion

Configurar variables en `.env`1

```bash

copy .env.example .env

```

## Backend(API)

```bash

# Intalar Dependencias - Crear y activa el entorno virtual de manera automatica
uv sync

# Usando pip
python -m venv .venv && .\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt

```

## Frontend(UI)

```bash
# Instalar Dependencias
npm install
```

---

## Ejecucion

```bash

# Ejecutar servidor local
uv run main.py

# Otra opcion
python main.py

```

> El servidor quedara disponible en el puerto que hayas definido en el archivo `.env` (por defecto `5000`).

- **API Url Base:** `http://localhost:<PORT>/api/v1/`
- **UI Url Base:** `http://localhost:<PORT>/`

---

## Documentación

- Guia de seguridad: [`docs/Security/README.md`](./docs/Security/README.md).

- Documentacion API: [`docs/API/README.md`](./docs/API/README.md).

- Base de datos: [`docs/Database/schema_db.md`](./docs/Database/schema_db.md) y [`docs/Database/MIGRATIONS.md`](./docs/Database/MIGRATIONS.md).

- Sphinx: [`docs/source/index.rst`](./docs/source/index.rst) (build CI en `.github/workflows/docs.yml`).
    - Puedes generar la documentación ejecutando el builder [`make.bat`](./docs/make.bat)
- Swagger: [`GET /docs`](http://localhost:<PORT>/docs).

- Enlace a colección de Postman: [Click Here!](https://www.postman.com/javier-prez/workspace/raccoon-surveys-api/collection/43954198-06d34335-49ff-4778-af25-1676be326cb6?action=share&creator=43954198&active-environment=43954198-cabc9e0c-dc39-401d-87b8-72ac404ce002)

---

## Estructura

Este proyecto tiene la siguiente estructura:

<details>

<summary>Ver estructura</summary>

```plaintext
raccoon-survey/
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
|-- requirements.txt
|-- CODE_OF_CONDUCT.md
|-- LICENSE
|-- SECURITY.md
`-- README.md
```

</details>

---

## Seguridad
- Politica del proyecto: [`SECURITY.md`](./SECURITY.md).
- JWT, RBAC, blocklist y CORS: [`docs/Security/README.md`](./docs/Security/README.md).
- Buenas practicas y divulgacion responsable en [`SECURITY.md`](./SECURITY.md).

---

## Códigos de Conducta
- Lee el archivo [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) para entender nuestras expectativas en la comunidad.

---

## Quieres contribuir? 
Echale un vistazo al archivo [`CONTRIBUTING.md`](./CONTRIBUTING.md) y [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) para mas información.
- Cambios y versiones: [`CHANGELOG.md`](./CHANGELOG.md).

---

## Licencia
Distribuido bajo `GPLv3`. Ver [LICENSE](./LICENSE) para mas información.

---

<div align="center">
<img src="./src/ui/static/img/raccoon_survey.png" alt="Raccoon Survey Logo" width="100" height="100">   

© Copyright 2025, Raccoon Survey Team.

<div>