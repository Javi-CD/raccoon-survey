# API Endpoints Documentation (API v1)

This document summarizes the available REST endpoints and how to use them. For full details, refer to the Swagger/OpenAPI endpoint and the Postman collection.

## Table of Contents
- [Swagger Reference](#swagger-reference)
- [Authentication](#authentication)
- [Roles](#roles)
- [Users](#users)
- [Teams](#teams)
- [Surveys](#surveys)
- [Questions](#questions)
- [Categories](#categories)
- [Survey Tokens](#survey-tokens)
- [Anonymous](#anonymous)
- [Reports](#reports)
- [Metrics](#metrics)
- [Maintenance](#maintenance)
- [Health](#health)

---

## Swagger Reference
- Endpoint: `/api/v1/openapi.json`
- Description: OpenAPI 3.0 document with the complete API definition.
- Note: served by the `docs` blueprint. Use it with Swagger UI, ReDoc, or any OpenAPI viewer.
- Postman collection link: [Click Here!](https://www.postman.com/javier-prez/workspace/raccoon-surveys-api/collection/43954198-06d34335-49ff-4778-af25-1676be326cb6?action=share&creator=43954198&active-environment=43954198-cabc9e0c-dc39-401d-87b8-72ac404ce002)

---

## Authentication

Base: `/api/v1/auth`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `POST` | `/login` | No | - | Log in and get JWT tokens |
| `POST` | `/refresh` | `Bearer` (Refresh) | - | Refresh access token |
| `POST` | `/logout` | `Bearer` | - | Revoke refresh token (logout) |
| `GET` | `/me` | `Bearer` | `admin`, `rrhh` | Authenticated user profile |

<details>
  <summary>Details</summary>
  
  - `/login` JSON Body: `{ email: string, password: string }`

  - `/refresh` requires a refresh token. Response: `{ access_token: string }`

  - `/logout` revokes the refresh token using the JWT `jti`.

  - `/me` returns `{ id, role, team_id, name }` based on claims.
</details>

---

## Roles

Base: `/api/v1/roles`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | List active roles |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Create role |
| `GET` | `/<role_id>` | `Bearer` | `admin`, `rrhh` | Get role |
| `PUT` | `/<role_id>` | `Bearer` | `admin`, `rrhh` | Update role |
| `DELETE` | `/<role_id>` | `Bearer` | `admin`, `rrhh` | Deactivate role (soft‑delete) |

<details>
  <summary>Details</summary>
  
  - `POST /` Body: `{ name: string, description?: string }`

  - `PUT /<role_id>` Body: `{ name?, description?, state? }`

  - `DELETE /<role_id>` performs soft‑delete: sets `state=false` and returns the updated role.
</details>

---

## Users

Base: `/api/v1/users`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | List active users |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Create user |
| `GET` | `/<user_id>` | `Bearer` | `admin`, `rrhh` | Get user |
| `PUT` | `/<user_id>` | `Bearer` | `admin`, `rrhh` | Update user |
| `PATCH` | `/<user_id>/state` | `Bearer` | `admin`, `rrhh` | Change user state |

<details>
  <summary>Details</summary>
  
  - `POST /` Body: `{ name: string, email: string, password: string, role_id?: number, team_id?: number }`

  - `PUT /<user_id>` Body: optional fields `{ name?, email?, password?, role_id?, team_id?, state? }`

  - `PATCH /<user_id>/state` Body: `{ state: boolean }` (soft‑delete/restore)
</details>

---

## Teams

Base: `/api/v1/teams`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | List teams |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Create team |
| `GET` | `/<team_id>` | `Bearer` | `admin`, `rrhh` | Get team |
| `PUT` | `/<team_id>` | `Bearer` | `admin`, `rrhh` | Update team |
| `PATCH` | `/<team_id>/state` | `Bearer` | `admin`, `rrhh` | Change team state |

<details>
  <summary>Details</summary>
  
  - `POST /` Body: `{ name: string, description?: string }`

  - `PUT /<team_id>` Body: `{ name?, description?, state? }`

  - `PATCH /<team_id>/state` Body: `{ state: boolean }`
</details>

---

## Surveys

Base: `/api/v1/surveys`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | List surveys (filter by `team_id`) |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Create survey |
| `GET` | `/<survey_id>` | `Bearer` | `admin`, `rrhh` | Get survey |
| `PUT` | `/<survey_id>` | `Bearer` | `admin`, `rrhh` | Update survey |
| `PATCH` | `/<survey_id>/state` | `Bearer` | `admin`, `rrhh` | Change survey state |

<details>
  <summary>Details</summary>
  
  - `POST /` Body: `{ title, team_id, description?, is_anonymous?, expires_at?, created_by_user_id? }`

  - `PUT /<survey_id>` Body: optional fields `{ title?, description?, is_anonymous?, team_id?, created_by_user_id?, expires_at?, state? }`

  - `GET /` Query: `team_id` (optional)
</details>

---

## Questions

Base: `/api/v1/questions`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | List questions (filter by `survey_id`) |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Create question |
| `GET` | `/<question_id>` | `Bearer` | `admin`, `rrhh` | Get question |
| `PUT` | `/<question_id>` | `Bearer` | `admin`, `rrhh` | Update question |
| `PATCH` | `/<question_id>/state` | `Bearer` | `admin`, `rrhh` | Change question state |

<details>
  <summary>Details</summary>
  
  - `POST /` Body: `{ survey_id, text, type, options?, is_required?, order_position? }`
  - `GET /` Query: `survey_id` (optional)

  - `PUT /<question_id>` Body: optional fields (validates existing `survey_id` if changed)

  - `PATCH /<question_id>/state` Body: `{ state: boolean }`
</details>

---

## Categories

Base: `/api/v1/categories`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | List categories |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Create category |
| `GET` | `/<category_id>` | `Bearer` | `admin`, `rrhh` | Get category |
| `PUT` | `/<category_id>` | `Bearer` | `admin`, `rrhh` | Update category |
| `PATCH` | `/<category_id>/state` | `Bearer` | `admin`, `rrhh` | Change category state |

<details>
  <summary>Details</summary>
  
  - `POST /` Body: `{ name: string, description?: string }`

  - `PUT /<category_id>` Body: `{ name?, description?, state? }` (validates duplicates by `name`)

  - `PATCH /<category_id>/state` Body: `{ state: boolean }`
</details>

---

## Survey Tokens

Base: `/api/v1/tokens`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `POST` | `/<survey_id>/generate` | `Bearer` | `admin`, `rrhh` | Generate survey tokens |
| `GET` | `/<survey_id>/list` | `Bearer` | `admin`, `rrhh` | List tokens |
| `GET` | `/<survey_id>/export` | `Bearer` | `admin`, `rrhh` | Export tokens CSV |

<details>
  <summary>Details</summary>
  
  - `POST /<survey_id>/generate` Body: `{ count?, expires_at(ISO), team_id?, employee_identifiers?: string[] }`

  - `GET /<survey_id>/list` Query: `{ is_used?, include_expired? }`

  - `GET /<survey_id>/export` Query: `{ is_used?, include_expired? }` Response: CSV with download headers
</details>

---

## Anonymous

Base: `/api/v1/anonymous`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `POST` | `/responses` | No | - | Submit anonymous responses using a single-use token |
| `GET` | `/resolve` | No | - | Resolve survey and questions by token |

<details>
  <summary>Details</summary>
  
  - `POST /responses` Body: `{ token, survey_id?, responses: [{ question_id, answer }] }`

  - `GET /resolve` Query: `{ token, survey_id? }`
</details>

---

## Reports

Base: `/api/v1/reports`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/surveys/<survey_id>/summary` | `Bearer` | `admin`, `rrhh` | Survey summary (optional filters) |
| `GET` | `/teams/<team_id>/summary` | `Bearer` | `admin`, `rrhh` | Team summary (optional filters) |
| `GET` | `/export` | `Bearer` | `admin`, `rrhh` | Export summary (survey/team) as CSV |

<details>
  <summary>Details</summary>
  
  - `/surveys/<id>/summary` Query: `{ team_id?, date_from?, date_to? }`
  - `/teams/<id>/summary` Query: `{ survey_id?, date_from?, date_to? }`
  - `/export` Query: requires `survey_id` or `team_id`; accepts `{ date_from?, date_to? }`. Response: CSV with appropriate file.
</details>

---

## Metrics

Base: `/api/v1/metrics`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/dashboard` | `Bearer` | `admin`, `rrhh` | Aggregated metrics for admin dashboard |

---

## Maintenance

Base: `/api/v1/maintenance`

| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `POST` | `/tokens/cleanup` | `Bearer` | `admin`, `rrhh` | Cleanup expired tokens |

<details>
  <summary>Details</summary>
  
  - Body: `{ survey_id?, team_id?, dry_run?: boolean, older_than?(ISO) }`

    - `survey_id` and `team_id` are optional.

    - If `dry_run` is included, tokens are not deleted, only counted.

    - `older_than` filters tokens older than the given date.

  - Response: `{ matched: number, deleted: number }`
</details>

---

## Health

Base: `/api/v1/health`


| Method | Path | Auth | Roles | Summary |
|---|---|---|---|---|
| `GET` | `/api/v1/health` | No | - | Healthcheck with `message`, `status`, and `timestamp` |
