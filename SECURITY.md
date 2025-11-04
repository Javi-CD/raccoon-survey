# Política de Seguridad de Raccoon Survey

Esta política describe cómo reportar vulnerabilidades, el alcance de pruebas de seguridad, tiempos de respuesta y prácticas recomendadas específicas del proyecto.

## Reporte de Vulnerabilidades
- Canal: [Github Security Advisoy](https://github.com/Javi-CD/raccoon-survey/security/advisories)
- Incluye: versión/commit, entorno (dev/prod), endpoints afectados, pasos de reproducción, impacto esperado, PoC no destructivo y logs relevantes.
- No incluyas datos personales ni resultados reales de encuestas. Usa datos sintéticos.
- Asunto sugerido: `[SECURITY] <título corto>`.

## Tiempos de Respuesta
- Acuse de recibo: 72 horas hábiles.
- Triage: hasta 7 días para clasificación y severidad (CVSS aproximado).
- Mitigación/fix: 
  - Crítico/Alto: 30 días.
  - Medio: 60 días.
  - Bajo: próxima release planificada.

## Alcance
- Backend API: rutas bajo `/api/v1/*` (auth, teams, surveys, questions, tokens, anonymous, reports, metrics, maintenance, health).
- Frontend UI: páginas `/dashboard`, `/surveys`, `/reports` y flujo de login (`/login`).
- CI/CD: workflows en `.github/workflows/` y scripts auxiliares.
- Configuración y secretos: `.env`, variables de entorno y credenciales de despliegue.

## Fuera de Alcance
- Ataques de DDoS, spam o denegación de servicio deliberada.
- Ingeniería social contra colaboradores o terceros.
- Vulnerabilidades en dependencias externas sin configuración propia del proyecto.
- Hallazgos sin impacto de seguridad (p. ej., micro-optimización de rendimiento).

## Safe Harbor y Divulgación Responsable
- Investigación de buena fe dentro del alcance no será perseguida; evita exfiltración de datos reales.
- No accedas a datos de terceros ni datos personales; usa entornos de prueba.
- No divulgues públicamente antes de coordinar fix y release. Trabajaremos en conjunto para una divulgación responsable.

## Prácticas Recomendadas (Específicas del Proyecto)
- Autenticación/Autorización:
  - JWT Bearer en `Authorization: Bearer <access_token>`; refresh vía `POST /api/v1/auth/refresh`.
  - RBAC con `role` en claims; endpoints sensibles exigen `admin` o `rrhh`.
  - Revocación: blocklist por `jti`.
- Cookies y CORS:
  - UI usa `rs_access_token`, `rs_refresh_token`, `rs_has_session`. Configura `HttpOnly`, `Secure`, `SameSite`.
  - CORS restringido con `CORS_ORIGINS`, `supports_credentials=true`.
- Cabeceras y configuración:
  - Añade `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy` ajustado al frontend.
- Secretos y dependencias:
  - Nunca commitees valores reales en `.env`. Rotación periódica y least privilege.
  - Mantén dependencias al día y monitorea CVEs; aplica parches de seguridad.

## Versiones Soportadas
- Rama `develop` y últimas releases estables reciben parches de seguridad. Versiones antiguas pueden requerir actualización.

## Referencias
- Guía de Seguridad del proyecto: `docs/Security/README.md`.
- OpenAPI: `GET /api/v1/openapi.json`.

---

<div align="center">
<img src="./src/ui/static/img/raccoon_survey.png" alt="Raccoon Survey Logo" width="100" height="100">   

© Copyright 2025, Raccoon Survey Team.

<div>