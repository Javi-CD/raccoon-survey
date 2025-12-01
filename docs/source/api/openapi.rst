OpenAPI (Swagger)
=================

.. ifconfig:: has_openapi

   Overview
   --------
   This section presents the backend OpenAPI specification for Raccoon Survey.
   From this document, HTTP endpoints are generated and documented together with their parameters,
   request/response bodies, status codes, and data schemas.
   The source specification lives in ``src/core/openapi.json`` and acts as the integration contract
   for external clients and validation tools.

   How to Read and Use
   -------------------
   - Endpoints are grouped by tags for easier navigation.
   - Each endpoint details the HTTP method, path, parameters, request body, responses, and schemas.
   - Use this page as a reference when integrating, testing, or validating API behavior.

   Common Conventions
   ------------------
   - Set ``Content-Type: application/json`` for JSON requests.
   - Use ``Authorization: Bearer <token>`` for endpoints that require authentication.
   - Error responses include clear codes and messages aligned with the schema definitions.

   Quickstart with curl
   --------------------
   Authenticate and call typical endpoints from the command line.

   .. code-block:: bash

      # 1) Login (replace credentials if needed)
      curl -s -X POST http://localhost:3000/api/v1/auth/login \
        -H 'Content-Type: application/json' \
        -d '{"email":"admin@docs.local","password":"pass_doc_local"}'

      # 2) Capture access token (requires jq)
      TOKEN=$(curl -s -X POST http://localhost:3000/api/v1/auth/login \
        -H 'Content-Type: application/json' \
        -d '{"email":"admin@docs.local","password":"pass_doc_local"}' | jq -r '.access_token')

      # 3) Authenticated profile
      curl -s http://localhost:3000/api/v1/auth/me \
        -H "Authorization: Bearer $TOKEN"

      # 4) List surveys
      curl -s http://localhost:3000/api/v1/surveys \
        -H "Authorization: Bearer $TOKEN"

      # 5) Create a survey (example payload)
      curl -s -X POST http://localhost:3000/api/v1/surveys \
        -H 'Content-Type: application/json' \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"title":"Quarterly Satisfaction","team_id":1}'

   .. tip::
      On Windows PowerShell, replace environment variables with ``$env:TOKEN`` and use backticks or backquotes to escape.

   Postman Collection
   ------------------
   Use the shared Postman collection for ready-to-run requests and environments:

   - Postman collection link: `Click Here! <https://www.postman.com/javier-prez/workspace/raccoon-surveys-api/collection/43954198-06d34335-49ff-4778-af25-1676be326cb6?action=share&creator=43954198&active-environment=43954198-cabc9e0c-dc39-401d-87b8-72ac404ce002>`_

   Rendered Specification
   ----------------------

=================

   .. openapi:: ../../../src/core/openapi.json
      :encoding: utf-8

.. ifconfig:: not has_openapi

   .. warning::
      The ``sphinxcontrib-openapi`` plugin is not installed.
      Install dependencies with ``python -m pip install -r requirements.txt`` to visualize this section.
