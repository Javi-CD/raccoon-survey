Guía de Testing
===============

Resumen
-------
Cómo ejecutar la suite y cómo está organizada la carpeta de pruebas.

Requisitos
----------
- Python 3.11
- Dependencias de ``requirements.txt``

Instalación
-----------
.. code-block:: bash

   python -m pip install --upgrade pip
   pip install -r requirements.txt

Ejecución completa
------------------
.. code-block:: bash

   pytest -q

Subconjuntos
------------
- Integración:

  .. code-block:: bash

     pytest -q test/integration

- E2E:

  .. code-block:: bash

     pytest -q test/e2e

- Unitarios:

  .. code-block:: bash

     pytest -q test/unitests

Estructura
----------
- ``test/integration``: pruebas de endpoints de la API.
- ``test/e2e``: flujos completos (ej. anonimato, exportación de tokens).
- ``test/unitests``: servicios internos y utilidades.
- ``test/utils/helpers.py``: helpers compartidos (equipos, encuestas, preguntas, tokens y expiraciones).

Helpers clave (ejemplos)
------------------------
- Crear equipo: ``_create_team(client, auth_header_admin) -> dict``
- Crear encuesta: ``_create_survey(client, auth_header_admin, team_id) -> dict``
- Crear pregunta: ``_create_question(client, auth_header_admin, survey_id, ...) -> dict``
- Generar token: ``_generate_token(client, auth_header_admin, survey_id, expires_at=...) -> dict``
- Utilidades de expiración: ``expires_at_future()``, ``expires_at_past()``

Variables de entorno
--------------------
- Archivo base: ``.env.example``
- Ajusta valores necesarios para el entorno de ejecución local.

.. note::
   Los tests aíslan la base de datos por prueba mediante fixtures definidas en ``test/integration/conftest.py`` y ``test/conftest.py``.

.. tip::
   Usa los helpers compartidos para evitar duplicaciones y mantener consistencia entre casos de prueba.

Referencias
-----------
- Más detalle en :doc:`../Testing/README` (Markdown).
