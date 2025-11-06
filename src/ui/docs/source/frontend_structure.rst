Estructura del Frontend
=======================

La estructura de carpetas del módulo **UI** sigue un modelo modular para facilitar el mantenimiento:

.. code-block:: text

    ui/
    ├── static/
    │   ├── css/
    │   ├── js/
    │   │   ├── anonymous/
    │   │   │   └── resolver.js
    │   │   ├── dashboard/
    │   │   │   ├── auth-check.js
    │   │   │   ├── charts-init.js
    │   │   │   ├── logout.js
    │   │   │   ├── metrics.js
    │   │   │   ├── page-config.js
    │   │   │   ├── sidebar.js
    │   │   │   └── tailwind-config.js
    │   │   ├── lib/
    │   │   ├── reports/
    │   │   └── surveys/
    │   └── img/
    │       ├── raccoon_survey.ico
    │       └── raccoon_survey.png
    ├── templates/
    │   ├── base.html
    │   ├── index.html
    │   └── dashboard.html
    ├── components/
    │   ├── footer.html
    │   ├── navbar.html
    │   └── sidebar.html
    └── main.py

**Descripción:**
* `static/`: contiene los recursos estáticos (CSS, JS, imágenes).
    * `js/`: Archivos **JavaScript** para la lógica del frontend.
        * `anonymous/`: Lógica para usuarios no autenticados (e.g., `resolver.js`).
        * `dashboard/`: Lógica específica para las vistas del panel de control (e.g., manejo de autenticación, inicialización de gráficos, configuración de la interfaz).
        * `lib/`, `reports/`, `surveys/`: Otras carpetas para modularizar el JavaScript por funcionalidad o módulo.
    * `img/`: Imágenes e íconos estáticos.
* `templates/`: archivos HTML que representan las vistas principales.
* `components/`: fragmentos reutilizables de interfaz (partials).
* `main.py`: punto de entrada del servidor de desarrollo.