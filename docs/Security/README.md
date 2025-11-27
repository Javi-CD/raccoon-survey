# Security

This guide explains how security works in Raccoon Survey across the backend (API) and frontend (UI). It covers JWT, role-based access control (RBAC), token blocklist, CORS, and the UI page guard.

---

## Table of Contents
- [Overview](#overview)
- [Security Coverage](#security-coverage)
- [Backend](#backend)
  - [JWT Authentication](#jwt-authentication)
  - [Role-Based Authorization (RBAC)](#role-based-authorization-rbac)
  - [User Validation (`user_required`)](#user-validation-user_required)
  - [Token Blocklist](#token-blocklist)
  - [CORS](#cors)
  - [Swagger Security Scheme](#swagger-security-scheme)
- [Frontend](#frontend)
  - [Private Page Guard](#private-page-guard)
  - [Login, Tokens and Refresh Flow](#login-tokens-and-refresh-flow)
  - [API Consumption with Authorization](#api-consumption-with-authorization)
- [Troubleshooting](#troubleshooting)
  - [401 Unauthorized](#401-unauthorized)
  - [403 Forbidden](#403-forbidden)
  - [404 Not Found](#404-not-found)
  - [500 Internal Server Error](#500-internal-server-error)
  - [Cookies and CORS](#cookies-and-cors)
  - [Useful Snippets](#useful-snippets)

---

## Overview

- Security based on JWT + RBAC.
- Access and refresh tokens; revocation via blocklist.
- CORS with `supports_credentials` enabled.
- UI protects pages by checking session cookies and tokens.


- The API uses `flask_jwt_extended` to issue and validate JWT: `access_token` and `refresh_token`.
- Permissions are controlled via decorators: `@jwt_required()` and `@role_required(...)`.
- Tokens are revoked through an in-memory blocklist (non-persistent); migrating to DB persistence is recommended.
- The frontend stores tokens in cookies and applies a guard before rendering private pages.

## Security Coverage

- Run tests with security-focused coverage:
  - ```bash
    pytest -q --cov=src/core --cov=src/ui --cov-report=term-missing --cov-report=html
    ```
  - HTML report: open `htmlcov/index.html`.
- Critical modules to cover (target ≥ 90%):
  - `src/core/middlewares/rbac.py` (roles and `@role_required`).
  - `src/core/services/auth_service.py` (issue/refresh/logout/profile).
  - `src/core/services/jwt_blocklist.py` (revocation by `jti`).
  - `src/core/__init__.py` (CORS: `supports_credentials`, allowed origins).
  - `src/ui/routes/pages.py` (private page guard).
  - Error responses in routes: `src/core/routes/*` (structure `{ "message": ... }`).
- Per-file coverage:
  - ```bash
    pytest -q test/unitests/test_auth_service.py --cov=src/core/services/auth_service.py --cov-report=term-missing
    ```
- Tips:
  - Simulate invalid/expired JWTs to trigger `401` and `403`.
  - Test routes with incorrect roles to validate RBAC.
  - Include CORS tests when possible (multiple origins in `.env`).

---

## Backend

- JWT authentication: issuing, refresh, logout, and profile.
- RBAC based on role claims.
- User existence validation.
- Token revocation.
- CORS and allowed origins.
- Swagger and Bearer scheme.


### JWT Authentication

- Token issuance:
  - Route `POST /api/v1/auth/login`.
  - Processes `email` and `password` and validates:
    - User exists (`@user_required(source="json", key="email", field="email")`).
    - Active role (`verify_user_active_role`).
    - Correct password (`check_password`).
  - Generates tokens with `create_tokens(user, access_expires, refresh_expires)` and claims:
    - `role`, `team_id`, `name`, and `identity = user.id`.

- Access token refresh:
  - Route `POST /api/v1/auth/refresh` with `@jwt_required(refresh=True)`.
  - Reuses `identity` and claims from the refresh token and issues a new `access_token`.

- Logout (revocation):
  - Route `POST /api/v1/auth/logout` with `@jwt_required()`.
  - Revokes the token by `jti` using `auth_service.revoke_token(jti)`.

- Profile:
  - Route `GET /api/v1/auth/me` with `@role_required("admin", "rrhh")`.
  - Returns `{ id, role, team_id, name }` extracted from the JWT.

Key code references:
- `src/core/services/auth_service.py` (claims, issue, refresh, revoke, profile).
- `src/core/routes/auth.py` (login, refresh, logout, me).

### Role-Based Authorization (RBAC)

- Decorator `@role_required(*allowed_roles)` (`src/core/middlewares/rbac.py`):
  - Requires `@jwt_required()` and then reads `role` from the JWT.
  - Responds with `403` if `role` is missing or not in `allowed_roles`.

- Usage examples:
  - Metrics and maintenance: roles `admin` and `rrhh`.
  - Reports: typically `admin`/`rrhh`.

Example table:

| Endpoint (example) | Method | Decorators | Allowed roles |
|--------------------|--------|------------|----------------|
| `/api/v1/metrics/dashboard` | GET | `@role_required("admin","rrhh")` | admin, rrhh |
| `/api/v1/maintenance/tokens/cleanup` | POST | `@role_required("admin","rrhh")` | admin, rrhh |

### User Validation (`user_required`)

- The `user_required` decorator (`src/core/middlewares/user_required.py`) ensures the user exists:
  - `source="jwt"` (default): validates JWT and uses `get_jwt_identity()`.
  - `source="param"`: looks for `user_id` in the route or query.
  - `source="json"`: looks for `user_id` (or `email`) in the body.
- Supports `field` to search by `id`, `email`, or another field.
- Option `require_active_role=True` enforces the role is active.

### Token Blocklist

- Simple in-memory implementation (`src/core/services/jwt_blocklist.py`):
  - `revoke_token(jti)` adds the `jti` to the `REVOKED_TOKENS` set.
  - `is_token_revoked(jti)` checks if it is revoked.

- Integration in `create_app` (`src/core/__init__.py`):
  - Callback `@jwt.token_in_blocklist_loader` uses `is_token_revoked`.

> On app restart the state is lost.
> Pending implementation: DB persistence with expiration.

### CORS

- Configured in `create_app` with `flask_cors.CORS`:
  - `resources={r"/*": {"origins": BaseConfig.CORS_ORIGINS}}`.
  - `supports_credentials=True` to allow cookies/credentials.

- Allowed origins via `.env`:
  - ```js
    CORS_ORIGINS="https://{{base_url}},https://admin.{{base_url}}"
    ```

### Swagger Security Scheme

- OpenAPI available at `GET /api/v1/openapi.json`.
- `Bearer` scheme (header `Authorization: Bearer <access_token>`).

---

## Frontend

- Private page guard with cookies.
- Login flow and token storage.
- Refresh and use of `Authorization`.


### Private Page Guard

- Before each request, the UI blueprint validates private pages (`/dashboard`, `/surveys`, `/reports`).
- Implementation: `src/ui/routes/pages.py` (`@bp.before_app_request`).
- Access rules:
  - Allowed if `rs_has_session == "1"` or both `rs_access_token` and `rs_refresh_token` exist.
  - Otherwise, redirect to `/login`.

### Login, Tokens and Refresh Flow

- Login:
  - The frontend sends `POST /api/v1/auth/login` with `{ email, password }`.
  - On receiving `{ access_token, refresh_token }`, it stores them in cookies:
    - `rs_access_token` and `rs_refresh_token`.
    - Optionally `rs_has_session = "1"` as a session flag.
  - Use `HttpOnly` + `Secure` cookies (configured by the server) for greater protection.

- Refresh:
  - When the `access_token` expires, send `POST /api/v1/auth/refresh` with the `refresh_token`.
  - Update `rs_access_token`.

- Logout:
  - `POST /api/v1/auth/logout` and clear cookies.

### API Consumption with Authorization

- For protected endpoints, add the header:
  - `Authorization: Bearer <value of rs_access_token>`.
- Error handling:
  - `401` → renew `access_token` with `/auth/refresh`.
  - `403` → verify role and route.

Pseudocode example (fetch):

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

## Troubleshooting

### 401 Unauthorized

- Causes:
  - Missing `Authorization` header or expired `access_token`.
  - Invalid `refresh_token` when using `/auth/refresh`.
- Typical API response:
  - `{ "message": "missing authorization header" }` or `{ "msg": "Token has expired" }` (from `flask_jwt_extended`).
- Related UI page:
  - Redirect to `login` by the guard (`src/ui/routes/pages.py`).
  - Template: `src/ui/templates/pages/auth/login.html`.
- Quick check:
  - ```bash
    curl -i -H "Authorization: Bearer <token>" http://{{base_url}}/api/v1/auth/me
    ```

### 403 Forbidden

- Causes:
  - Missing `role` claim or not allowed by `@role_required("admin","rrhh")`.
- API response (RBAC middleware):
  - `{ "message": "forbidden" }` or similar (customizable in `rbac.py`).
- Related UI behavior:
  - Hides the Settings link if you are not `admin` (`src/ui/static/js/dashboard/nav-admin-link.js`).
- Quick check:
  - `curl -i -H "Authorization: Bearer <token-no-admin>" http://{{base_url}}/api/v1/metrics/dashboard`

### 404 Not Found

- Common causes:
  - Non-existent entity: `role not found`, `team not found`, `category not found`.
  - Invalid anonymous token: does not exist or already used.
- API responses (real examples):
  - Roles: `{ "message": "role not found" }` (`src/core/routes/roles.py`).
  - Teams: `{ "message": "team not found" }` (`src/core/routes/teams.py`).
  - Categories: `{ "message": "category not found" }` (`src/core/routes/categories.py`).
  - Anonymous: `{ "message": "token not found" }` or similar (`src/core/routes/anonymous.py`).
- Related UI behavior:
  - The UI typically shows `alert(...)` or `console.error(...)` and retries/reloads (see `src/ui/static/js/config/categories.js`, `users.js`).

### 500 Internal Server Error

- Common causes:
  - Database errors, unchecked validations, service exceptions.
- API responses (example):
  - Anonymous: `except RuntimeError as e → return jsonify({ "message": str(e) }), 500` (`src/core/routes/anonymous.py`).
- Diagnostic steps:
  - Review server logs and stack trace.
  - Validate payloads with `Content-Type: application/json` and expected structure.

### Cookies and CORS

- Recommended cookie attributes:
  - `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict`, depending on the case.
  - If you use `HttpOnly`, you cannot read tokens with `document.cookie` (safer). Serve tokens via the backend with `Set-Cookie`.
- CORS configuration:
  - `supports_credentials=True` and origins in `.env`:
    ```js
      CORS_ORIGINS="https://{{base_url}},https://admin.{{base_url}}"
    ```

  - See `src/core/__init__.py` for integration.

### Useful Snippets

- Login:
  - ```bash
    curl -s -X POST http://{{base_url}}/api/v1/auth/login -H 'Content-Type: application/json' -d '{"email":"admin@raccoon.local","password":"<pass>"}'
    ```
- Refresh:
  - ```bash
    curl -s -X POST http://{{base_url}}/api/v1/auth/refresh -H 'Authorization: Bearer <refresh_token>'
    ```
- Access a protected endpoint:
  - ```bash
    curl -i -H 'Authorization: Bearer <access_token>' http://{{base_url}}/api/v1/metrics/dashboard
    ```
