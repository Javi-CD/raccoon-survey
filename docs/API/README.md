# Documentación de Endpoints (API v1)

Este documento resume los endpoints REST disponibles y cómo utilizarlos. Para detalles exhaustivos, consulta el endpoint de Swagger/OpenAPI y la colección de Postman.

## Tabla de Contenidos
- [Referencia Swagger](#referencia-swagger)
- [Autenticación](#autenticación)
- [Equipos](#equipos)
- [Encuestas](#encuestas)
- [Preguntas](#preguntas)
- [Tokens de Encuestas](#tokens-de-encuestas)
- [Anónimo](#anónimo)
- [Reportes](#reportes)
- [Métricas](#métricas)
- [Mantenimiento](#mantenimiento)
- [Salud](#salud)

## Referencia Swagger
- Endpoint: `/api/v1/openapi.json`
- Descripción: Documento OpenAPI 3.0 con la definición completa de la API.
- Nota: servido por el blueprint `docs`. Úsalo en Swagger UI, ReDoc o cualquier visor OpenAPI.
- Enlace a colección de Postman: [Click Here!](https://www.postman.com/javier-prez/workspace/raccoon-surveys-api/collection/43954198-06d34335-49ff-4778-af25-1676be326cb6?action=share&creator=43954198&active-environment=43954198-cabc9e0c-dc39-401d-87b8-72ac404ce002)

---

## Autenticación

Base: `/api/v1/auth`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `POST` | `/login` | No | - | Iniciar sesión y obtener tokens JWT |
| `POST` | `/refresh` | `Bearer` (Refresh) | - | Refrescar token de acceso |
| `POST` | `/logout` | `Bearer` | - | Revocar token de refresh (logout) |
| `GET` | `/me` | `Bearer` | `admin`, `rrhh` | Perfil del usuario autenticado |

<details>
  <summary>Detalles</summary>
  
  - `/login` Body JSON: `{ email: string, password: string }`

  - `/refresh` requiere token de refresh. Respuesta: `{ access_token: string }`

  - `/logout` revoca el refresh token usando `jti` del JWT.

  - `/me` retorna `{ id, role, team_id, name }` basado en claims.
</details>

---

## Equipos

Base: `/api/v1/teams`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | Listar equipos |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Crear equipo |
| `GET` | `/<team_id>` | `Bearer` | `admin`, `rrhh` | Obtener equipo |
| `PUT` | `/<team_id>` | `Bearer` | `admin`, `rrhh` | Actualizar equipo |
| `PATCH` | `/<team_id>/state` | `Bearer` | `admin`, `rrhh` | Cambiar estado |

<details>
  <summary>Detalles</summary>
  
  - `POST /` Body: `{ name: string, description?: string }`

  - `PUT /<team_id>` Body: `{ name?, description?, state? }`

  - `PATCH /<team_id>/state` Body: `{ state: boolean }`
</details>

---

## Encuestas

Base: `/api/v1/surveys`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | Listar encuestas (filtrar por `team_id`) |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Crear encuesta |
| `GET` | `/<survey_id>` | `Bearer` | `admin`, `rrhh` | Obtener encuesta |
| `PUT` | `/<survey_id>` | `Bearer` | `admin`, `rrhh` | Actualizar encuesta |
| `PATCH` | `/<survey_id>/state` | `Bearer` | `admin`, `rrhh` | Cambiar estado |

<details>
  <summary>Detalles</summary>
  
  - `POST /` Body: `{ title, team_id, description?, is_anonymous?, expires_at?, created_by_user_id? }`

  - `PUT /<survey_id>` Body: campos opcionales `{ title?, description?, is_anonymous?, team_id?, created_by_user_id?, expires_at?, state? }`

  - `GET /` Query: `team_id` (opcional)
</details>

---

## Preguntas

Base: `/api/v1/questions`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `GET` | `/` | `Bearer` | `admin`, `rrhh` | Listar preguntas (filtrar por `survey_id`) |
| `POST` | `/` | `Bearer` | `admin`, `rrhh` | Crear pregunta |
| `GET` | `/<question_id>` | `Bearer` | `admin`, `rrhh` | Obtener pregunta |
| `PUT` | `/<question_id>` | `Bearer` | `admin`, `rrhh` | Actualizar pregunta |
| `PATCH` | `/<question_id>/state` | `Bearer` | `admin`, `rrhh` | Cambiar estado |

<details>
  <summary>Detalles</summary>
  
  - `POST /` Body: `{ survey_id, text, type, options?, is_required?, order_position? }`
  - `GET /` Query: `survey_id` (opcional)

  - `PUT /<question_id>` Body: campos opcionales (valida `survey_id` existente si se cambia)

  - `PATCH /<question_id>/state` Body: `{ state: boolean }`
</details>

---

## Tokens de Encuestas

Base: `/api/v1/tokens`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `POST` | `/<survey_id>/generate` | `Bearer` | `admin`, `rrhh` | Generar tokens de encuesta |
| `GET` | `/<survey_id>/list` | `Bearer` | `admin`, `rrhh` | Listar tokens |
| `GET` | `/<survey_id>/export` | `Bearer` | `admin`, `rrhh` | Exportar tokens CSV |

<details>
  <summary>Detalles</summary>
  
  - `POST /<survey_id>/generate` Body: `{ count?, expires_at(ISO), team_id?, employee_identifiers?: string[] }`

  - `GET /<survey_id>/list` Query: `{ is_used?, include_expired? }`

  - `GET /<survey_id>/export` Query: `{ is_used?, include_expired? }` Respuesta: CSV con headers de descarga
</details>

---

## Anónimo

Base: `/api/v1/anonymous`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `POST` | `/responses` | No | - | Enviar respuestas anónimas con token de un solo uso |
| `GET` | `/resolve` | No | - | Obtener encuesta y preguntas por token |

<details>
  <summary>Detalles</summary>
  
  - `POST /responses` Body: `{ token, survey_id?, responses: [{ question_id, answer }] }`

  - `GET /resolve` Query: `{ token, survey_id? }`
</details>

---

## Reportes

Base: `/api/v1/reports`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `GET` | `/surveys/<survey_id>/summary` | `Bearer` | `admin`, `rrhh` | Resumen por encuesta (filtros opcionales) |
| `GET` | `/teams/<team_id>/summary` | `Bearer` | `admin`, `rrhh` | Resumen por equipo (filtros opcionales) |
| `GET` | `/export` | `Bearer` | `admin`, `rrhh` | Exportar resumen (encuesta/equipo) en CSV |

<details>
  <summary>Detalles</summary>
  
  - `/surveys/<id>/summary` Query: `{ team_id?, date_from?, date_to? }`
  - `/teams/<id>/summary` Query: `{ survey_id?, date_from?, date_to? }`
  - `/export` Query: requiere `survey_id` o `team_id`; acepta `{ date_from?, date_to? }`. Respuesta: CSV con archivo acorde.
</details>

---

## Métricas

Base: `/api/v1/metrics`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `GET` | `/dashboard` | `Bearer` | `admin`, `rrhh` | Métricas agregadas para el dashboard admin |

---

## Mantenimiento

Base: `/api/v1/maintenance`

| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `POST` | `/tokens/cleanup` | `Bearer` | `admin`, `rrhh` | Limpieza de tokens expirados |

<details>
  <summary>Detalles</summary>
  
  - Body: `{ survey_id?, team_id?, dry_run?: boolean, older_than?(ISO) }`

    - `survey_id` y `team_id` son opcionales.

    - `dry_run` si se incluye, no se eliminan tokens, solo se cuenta.

    - `older_than` filtra tokens más antiguos que la fecha indicada.

  - Respuesta: `{ matched: number, deleted: number }`
</details>

---

## Salud

Base: `/api/v1/health`


| Método | Ruta | Auth | Roles | Resumen |
|---|---|---|---|---|
| `GET` | `/api/v1/health` | No | - | Healthcheck con `message`, `status` y `timestamp` |