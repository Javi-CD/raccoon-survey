# Seguridad

Esta guía explica cómo funciona la seguridad en Raccoon Survey, tanto en el backend (API) como en el frontend (UI). Incluye JWT, control de acceso por roles (RBAC), bloqueo de tokens (blocklist), CORS, y el guard de páginas en la UI.

---

## Tabla de Contenidos
- [Visión General](#visión-general)
- [Backend](#backend)
  - [Autenticación JWT](#autenticación-jwt)
  - [Autorización por Roles (RBAC)](#autorización-por-roles-rbac)
  - [Validación de Usuario (`user_required`)](#validación-de-usuario-user_required)
  - [Blocklist de Tokens](#blocklist-de-tokens)
  - [CORS](#cors)
  - [Esquema de Seguridad en Swagger](#esquema-de-seguridad-en-swagger)
- [Frontend](#frontend)
  - [Guard de Páginas Privadas](#guard-de-páginas-privadas)
  - [Flujo de Login, Tokens y Refresh](#flujo-de-login-tokens-y-refresh)
  - [Consumo de API con Authorization](#consumo-de-api-con-authorization)
- [Solución de Problemas](#solución-de-problemas)

---

## Visión General

- Seguridad basada en JWT + RBAC.
- Tokens de acceso y refresh; revocación con blocklist.
- CORS con `supports_credentials` habilitado.
- UI protege páginas revisando cookies de sesión y tokens.


- La API usa `flask_jwt_extended` para emitir y validar JWT: `access_token` y `refresh_token`.
- Los permisos se controlan con decoradores: `@jwt_required()` y `@role_required(...)`.
- Se revocan tokens mediante un blocklist en memoria (no persistente) y se aconseja migrarlo a BD.
- El frontend guarda tokens en cookies y aplica un guard antes de renderizar páginas privadas.

---

## Backend

- Autenticación JWT: emisión, refresh, logout y perfil.
- RBAC por claims de rol.
- Verificación de existencia de usuario.
- Revocación de tokens.
- CORS y orígenes permitidos.
- Swagger y esquema Bearer.


### Autenticación JWT

- Emisión de tokens:
  - Ruta `POST /api/v1/auth/login`.
  - Procesa `email` y `password` y valida:
    - Usuario existe (`@user_required(source="json", key="email", field="email")`).
    - Rol activo (`verify_user_active_role`).
    - Password correcta (`check_password`).
  - Genera tokens con `create_tokens(user, access_expires, refresh_expires)` y claims:
    - `role`, `team_id`, `name` y `identity = user.id`.

- Refresh de `access_token`:
  - Ruta `POST /api/v1/auth/refresh` con `@jwt_required(refresh=True)`.
  - Reusa `identity` y claims del refresh token y emite nuevo `access_token`.

- Logout (revocación):
  - Ruta `POST /api/v1/auth/logout` con `@jwt_required()`.
  - Revoca el token por `jti` usando `auth_service.revoke_token(jti)`.

- Perfil:
  - Ruta `GET /api/v1/auth/me` con `@role_required("admin", "rrhh")`.
  - Devuelve `{ id, role, team_id, name }` extraído de JWT.

Referencias de código clave:
- `src/core/services/auth_service.py` (claims, emisión, refresh, revoke, perfil).
- `src/core/routes/auth.py` (login, refresh, logout, me).

### Autorización por Roles (RBAC)

- Decorador `@role_required(*allowed_roles)` (`src/core/middlewares/rbac.py`):
  - Exige `@jwt_required()` y luego lee `role` del JWT.
  - Responde `403` si falta `role` o no está en `allowed_roles`.

- Ejemplos de uso:
  - Métricas y mantenimiento: roles `admin` y `rrhh`.
  - Reportes: típicamente `admin`/`rrhh`.

Tabla de ejemplos:

| Endpoint (ejemplo) | Método | Decoradores | Roles permitidos |
|--------------------|--------|-------------|------------------|
| `/api/v1/metrics/dashboard` | GET | `@role_required("admin","rrhh")` | admin, rrhh |
| `/api/v1/maintenance/tokens/cleanup` | POST | `@role_required("admin","rrhh")` | admin, rrhh |

### Validación de Usuario (`user_required`)

- Decorador `user_required` (`src/core/middlewares/user_required.py`) asegura que el usuario exista:
  - `source="jwt"` (default): valida JWT y usa `get_jwt_identity()`.
  - `source="param"`: busca `user_id` en la ruta o query.
  - `source="json"`: busca `user_id` (o `email`) en el body.
- Soporta `field` para buscar por `id`, `email` u otro campo.
- Opción `require_active_role=True` fuerza que el rol esté activo.

### Blocklist de Tokens

- Implementación simple en memoria (`src/core/services/jwt_blocklist.py`):
  - `revoke_token(jti)` agrega el `jti` al set `REVOKED_TOKENS`.
  - `is_token_revoked(jti)` verifica si está revocado.

- Integración en `create_app` (`src/core/__init__.py`):
  - Callback `@jwt.token_in_blocklist_loader` usa `is_token_revoked`.

> Al reiniciar la app se pierde el estado. 
> Pendiente por implementar: Persistencia en BD con expiración.

### CORS

- Configurado en `create_app` con `flask_cors.CORS`:
  - `resources={r"/*": {"origins": BaseConfig.CORS_ORIGINS}}`.
  - `supports_credentials=True` para permitir envío de cookies/credenciales.

- Orígenes permitidos via `.env`:
  - `CORS_ORIGINS="https://tu-frontend.com,https://admin.tu-frontend.com"`.

### Esquema de Seguridad en Swagger

- OpenAPI disponible en `GET /api/v1/openapi.json`.
- Esquema `Bearer` (header `Authorization: Bearer <access_token>`).
- Recomendación: generar ejemplos de `401/403` y de respuesta para `me`.

---

## Frontend

- Guard de páginas privadas con cookies.
- Flujo de login y almacenamiento de tokens.
- Refresh y uso de `Authorization`.


### Guard de Páginas Privadas

- Antes de cada request, el UI blueprint valida páginas privadas (`/dashboard`, `/surveys`, `/reports`).
- Implementación: `src/ui/routes/pages.py` (`@bp.before_app_request`).
- Reglas de acceso:
  - Permite si `rs_has_session == "1"` o existen `rs_access_token` y `rs_refresh_token`.
  - Si no, redirige a `/login`.

### Flujo de Login, Tokens y Refresh

- Login:
  - El frontend envía `POST /api/v1/auth/login` con `{ email, password }`.
  - Al recibir `{ access_token, refresh_token }`, los guarda en cookies:
    - `rs_access_token` y `rs_refresh_token`.
    - Opcionalmente `rs_has_session = "1"` como bandera de sesión.
  - Sugerencia: usar cookies `HttpOnly` + `Secure` (configuradas por el servidor) para mayor protección.

- Refresh:
  - Cuando el `access_token` expira, enviar `POST /api/v1/auth/refresh` con el `refresh_token`.
  - Actualizar `rs_access_token`.

- Logout:
  - `POST /api/v1/auth/logout` y limpiar cookies.

### Consumo de API con Authorization

- Para endpoints protegidos, añadir header:
  - `Authorization: Bearer <valor de rs_access_token>`.
- Manejo de errores:
  - `401` → renovar `access_token` con `/auth/refresh`.
  - `403` → verificar rol y ruta.

Ejemplo pseudocódigo (fetch):

```js
const apiFetch = async (path, opts = {}) => {
  const access = getCookie('rs_access_token');
  const headers = { ...(opts.headers || {}), Authorization: `Bearer ${access}` };
  const res = await fetch(`/api/v1${path}`, { ...opts, headers });

  if (res.status === 401) {
    await refreshAccessToken();
    return apiFetch(path, opts); // Retry
  }

  return res;
}
```

---

## Solución de Problemas

- 401/403 y causas típicas.
- Tokens inválidos o expirados.
- Rol faltante o inactivo.
- CORS y cookies no enviadas.


- 401 Unauthorized:
  - Falta header `Authorization` o `access_token` expirado.
  - Solución: refrescar token con `/auth/refresh` y reintentar.
- 403 Forbidden:
  - Rol faltante en JWT o no permitido por `@role_required`.
  - Solución: iniciar sesión con usuario correcto o ajustar roles.
- Token inválido o revocado:
  - El `jti` fue revocado; no permite acceso.
  - Solución: volver a autenticarse para obtener tokens nuevos.
- CORS / cookies:
  - Cookies no viajan si falta `supports_credentials` o `SameSite` conflictúa.
  - Solución: revisar configuración CORS y atributos de cookies.

---

