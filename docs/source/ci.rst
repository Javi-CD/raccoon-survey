CI/CD - Tests
=============

Resumen
-------
Este pipeline ejecuta automáticamente la suite de tests y mide cobertura en cada ``push`` y ``pull_request`` a las ramas objetivo. Está definido en ``.github/workflows/tests.yml`` y usa ``ubuntu-latest`` con Python ``3.11`` y cache de ``pip``.

Ramas monitoreadas
------------------
- ``develop``
- ``features`` y subramas ``features/**``

Workflow de ejemplo
-------------------
.. code-block:: yaml

   name: CI - Tests

   on:
     push:
       branches:
         - develop
         - features
         - 'features/**'
     pull_request:
       branches:
         - develop
         - features
         - 'features/**'

   jobs:
     tests:
       runs-on: ubuntu-latest
       permissions:
         contents: read
       steps:
         - name: Checkout repository
           uses: actions/checkout@v4

         - name: Set up Python
           uses: actions/setup-python@v5
           with:
             python-version: '3.11'
             cache: 'pip'
             cache-dependency-path: 'requirements.txt'

         - name: Install dependencies
           run: |
             python -m pip install --upgrade pip
             pip install -r requirements.txt
             pip install pytest-cov

         - name: Run tests with coverage
           run: |
             pytest --cov=src --cov-report=term-missing:skip-covered \
                    --cov-report=xml:coverage.xml \
                    --cov-report=html

         - name: Upload coverage XML artifact
           uses: actions/upload-artifact@v4
           with:
             name: coverage-xml
             path: coverage.xml

         - name: Upload HTML coverage artifact
           uses: actions/upload-artifact@v4
           with:
             name: coverage-html
             path: htmlcov

Pasos principales
-----------------
1. Checkout del repositorio.
2. Configuración de Python con cache de ``pip``.
3. Instalación de dependencias desde ``requirements.txt`` e instalación de ``pytest-cov``.
4. Ejecución de la suite con cobertura y publicación de artifacts (XML, HTML).

Personalización
---------------
- Añadir matriz de versiones de Python:

  .. code-block:: yaml

     strategy:
       matrix:
         python-version: ['3.10', '3.11']

- Incluir linters (``flake8``, ``ruff``, ``black --check``) antes de ``pytest``.
- Ajustar ramas de disparo en ``on.push.branches`` y ``on.pull_request.branches``.

.. note::
   El patrón ``features/**`` incluye subramas como ``features/auth`` o ``features/tokens-export``.

.. tip::
   Usa matrices para probar en múltiples versiones de Python y, si aplica, en diferentes sistemas operativos.

.. seealso::
   Detalle ampliado en :doc:`../CI/TESTS_WORKFLOW` (Markdown) y la documentación oficial de `GitHub Actions <https://docs.github.com/en/actions>`_.
