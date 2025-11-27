# Raccoon Survey Security Policy

This policy describes how to report vulnerabilities, the scope of security testing, response times, and project-specific recommended practices.

---

## Vulnerability Reporting
- Channel: [GitHub Security Advisory](https://github.com/Javi-CD/raccoon-survey/security/advisories)
- Include: version/commit, environment (dev/prod), affected endpoints, reproduction steps, expected impact, non-destructive PoC, and relevant logs.
- Do not include personal data or real survey results. Use synthetic data.
- Suggested subject: `[SECURITY] <short title>`.

---

## Response Times
- Acknowledgement: 72 business hours.
- Triage: up to 7 days for classification and severity (approximate CVSS).
- Mitigation/fix:
  - Critical/High: 30 days.
  - Medium: 60 days.
  - Low: next planned release.

---

## Scope
- Backend API: routes under `/api/v1/*` (auth, teams, surveys, questions, tokens, anonymous, reports, metrics, maintenance, health).
- Frontend UI: pages `/dashboard`, `/surveys`, `/reports` and login flow (`/login`).
- CI/CD: workflows in `.github/workflows/` and helper scripts.
- Configuration and secrets: `.env`, environment variables, and deployment credentials.

---

## Out of Scope
- DDoS, spam, or deliberate denial-of-service attacks.
- Social engineering against contributors or third parties.
- Vulnerabilities in external dependencies without project-specific configuration.
- Findings without security impact (e.g., micro performance optimizations).

---

## Safe Harbor and Responsible Disclosure
- Good-faith research within scope will not be pursued; avoid exfiltration of real data.
- Do not access third-party data or personal data; use test environments.
- Do not disclose publicly before coordinating fix and release. We will work together toward responsible disclosure.

---

## Recommended Practices (Project-Specific)
- Authentication/Authorization:
  - JWT Bearer in `Authorization: Bearer <access_token>`; refresh via `POST /api/v1/auth/refresh`.
  - RBAC with `role` in claims; sensitive endpoints require `admin` or `rrhh`.
  - Revocation: blocklist by `jti`.
- Cookies and CORS:
  - UI uses `rs_access_token`, `rs_refresh_token`, `rs_has_session`. Configure `HttpOnly`, `Secure`, `SameSite`.
  - CORS restricted with `CORS_ORIGINS`, `supports_credentials=true`.
- Headers and configuration:
  - Add `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Content-Security-Policy` aligned with the frontend.
- Secrets and dependencies:
  - Never commit real values in `.env`. Periodic rotation and least privilege.
  - Keep dependencies up to date and monitor CVEs; apply security patches.

---

## Supported Versions
- The `develop` branch and latest stable releases receive security patches. Older versions may require updating.

---

## References
- Project Security Guide: `docs/Security/README.md`.
- OpenAPI: `GET /api/v1/openapi.json`.

---

<div align="center">
<img src="./src/ui/static/img/raccoon_survey.png" alt="Raccoon Survey Logo" width="100" height="100">

© Copyright 2025, Raccoon Survey Team.

</div>
