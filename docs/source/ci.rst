CI/CD - Tests
=============

Overview
--------
This pipeline automatically runs the test suite and measures coverage on every ``push`` and ``pull_request`` to the target branches. It is defined in ``.github/workflows/tests.yml`` and uses ``ubuntu-latest`` with Python ``3.11`` and ``pip`` cache.

Monitored branches
------------------
- ``develop``
- ``features`` and sub-branches ``features/**``

Sample workflow
---------------
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

Main steps
----------
1. Checkout the repository.
2. Set up Python with ``pip`` cache.
3. Install dependencies from ``requirements.txt`` and install ``pytest-cov``.
4. Run the suite with coverage and upload artifacts (XML, HTML).

Customization
-------------
- Add a Python version matrix:

  .. code-block:: yaml

     strategy:
       matrix:
         python-version: ['3.10', '3.11']

- Include linters (``flake8``, ``ruff``, ``black --check``) before ``pytest``.
- Adjust trigger branches in ``on.push.branches`` and ``on.pull_request.branches``.

.. note::
   The ``features/**`` pattern includes sub-branches such as ``features/auth`` or ``features/tokens-export``.

.. tip::
   Use matrices to test across multiple Python versions and, if applicable, different operating systems.

.. seealso::
   Extended details in :doc:`../CI/TESTS_WORKFLOW` (Markdown) and the official `GitHub Actions documentation <https://docs.github.com/en/actions>`_.
