# Guía de Contribución — Raccoon Survey

Gracias por tu interés en contribuir. Esta guía resume cómo preparar el entorno, el flujo de trabajo recomendado y los estándares de calidad para mantener el proyecto sano y seguro.

---

## Principios
- Respeto y colaboración ([`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md)).
- Seguridad ([`SECURITY.md`](./SECURITY.md)).
- Cambios pequeños y bien probados.
- Documentación y trazabilidad de los cambios.

---

## Requisitos
- `Python 3.11+`, `uv`.
- `Node.js 18+` y `npm`.
- Git.

---

## Configuración local

```bash

# Clonar repositorio
git clone https://github.com/Javi-CD/raccoon-survey.git

# Copiar .env.example a .env
cp .env.example .env

# ...Ajustar variables en .env (JWT, CORS, DB, etc)
```

### Backend

```bash

# Instalar Dependencias
uv sync

# Usando pip

python -m venv .venv && .\\.venv\\Scripts\\Activate.ps1 && pip install -r requirements.txt

```

### Frontend

```bash

# Instalar Dependencias
npm install

```

### Ejecutar servidor de desarrollo

```bash

uv run main.py

# Alternativa
python main.py

```

Verifica si se ejecuto correctamente el servidor de desarrollo.

```bash

curl --location  http://localhost:5000/api/v1/openapi.json
curl --location  http://localhost:5000/api/v1/health

```

> Si no se ha definifo la variable ``PORT`` en el archivo ``.env`` por defecto sera ``5000``

--

## Flujo de ramas
- Rama `develop`: estable.
- Crea ramas por cambio:
  ```plaintext

  tipo/nombre-de-rama

  ejemplo:

  feature/auth-middlewares
  fix/truncate-database
  ```
- Hacer `merge --no-ff` en la rama `features` y pobrar funcionalidades antes de abrir pull request en la rama `develop`


---

## Convenciones de commits
- Usa Conventional Commits:
  - `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
- Ejemplos:
  - `feat(api): agregar refresh token a /auth/refresh`
  - `fix(ui): corregir redirección en /dashboard sin sesión`
- Los hooks de `husky` y `commitlint` validan mensajes (ver [`commitlint.config.js`](./commitlint.config.js) y [`husky`](./.husky/)).

---

## Lint y formato
- Python: ver [`docs/CI/PYTHON_LINTING.md`](./docs/CI/PYTHON_LINTING.md).
- JavaScript/CSS: configura y usa:
  - ESLint: `npx eslint .` (ver [`eslintrc.js`](./.eslintrc.js))
  - Prettier: `npx prettier --check .` (ver [`prettierrc.js`](./.prettierrc.js))
  - Stylelint: `npx stylelint "src/ui/**/*.css"` (ver [`stylelintrc.js`](./.stylelintrc.js))

---

## Pruebas
- Ubicación: `test/` (`unitests/`, `integration/`, `e2e/`).
- Ejecuta: `pytest`.
- Añade pruebas para nueva funcionalidad y casos de error.

---

## Documentación
- Seguridad: [`docs/Security/README.md`](./docs/Security/README.md).
- API: [`docs/API/README.md`](./docs/API/README.md) y `src/core/openapi.json`.
- Base de datos: [`docs/Database/schema_db.md`](./docs/Database/schema_db.md) y [`docs/Database/MIGRATIONS.md`](./docs/Database/MIGRATIONS.md).
- Sphinx: [`docs/source/index.rst`](./docs/source/index.rst), build local: `docs\make.bat html`.
- Swagger: `curl --location http://localhost:<PORT>/docs`
- Enlace a colección de Postman: [Click Here!](https://www.postman.com/javier-prez/workspace/raccoon-surveys-api/collection/43954198-06d34335-49ff-4778-af25-1676be326cb6?action=share&creator=43954198&active-environment=43954198-cabc9e0c-dc39-401d-87b8-72ac404ce002)

---

## Migraciones de base de datos
- Configuración: `alembic.ini`.
- Sigue la guía: [`docs/Database/MIGRATIONS.md`](./docs/Database/MIGRATIONS.md).
- Incluye notas en PR sobre cambios de esquemas.

---

## Checklist de Pull Request
- Lint y formato pasan (ESLint/Prettier/Stylelint/Python).
- Pruebas agregadas y/o actualizadas; `pytest` en verde.
- Documentación actualizada (README/Docs/API/DB/Seguridad si aplica).
- Cambios scope limitado y motivación clara.
- Sin secretos ni credenciales en el commit.
- CI verde: `docs.yml`, `release.yml`, `changelog.yml`.

---

## Changelog y releases
- [`CHANGELOG.md`](./CHANGELOG.md) se mantiene vía CI; no editar manualmente.
- Versionado y paquetes: ver [`scripts/update_package_version.py`](./scripts/update_package_version.py), [`scripts/update_pyproject_version.py`](./scripts/update_pyproject_version.py), [`scripts/update_package_lock.js`](./scripts/update_package_lock.js).
- Pipeline de release: [`release.yml`](./.github/workflows/release.yml).

---

## Estándares de código
- Python: tipado estático donde sea posible, funciones pequeñas, evita nombres crípticos.
- Flask: rutas en `src/core/routes/`, servicios en `src/core/services/`, utilidades en `src/core/utils/`.
- UI: rutas/guards en `src/ui/routes/`, evita lógica compleja en plantillas.
- Seguridad: usa decoradores `role_required` y `user_required`, y respeta JWT/blocklist.

---

## Reporte de issues y seguridad
- Bugs: abre un issue con pasos reproducibles y logs relevantes.
- Vulnerabilidades: sigue [`SECURITY.md`](./SECURITY.md) (responsible disclosure). No exploits en producción.

---

## Licencia
- El proyecto está bajo `GPLv3` (ver [`LICENSE`](./LICENSE)).
- Al contribuir, aceptas que tu código se publica bajo la misma licencia.

---

<div align="center">
<img src="./src/ui/static/img/raccoon_survey.png" alt="Raccoon Survey Logo" width="100" height="100">   

© Copyright 2025, Raccoon Survey Team.

<div>
