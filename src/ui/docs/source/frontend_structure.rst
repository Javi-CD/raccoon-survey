.. _ui_frontend_structure:

Frontend Structure
==================

The folder structure of the **UI** module follows a modular and organized model to facilitate scalability and maintenance. The separation between static assets (`static`) and server-rendered templates (`templates`) is fundamental to this design.

.. code-block:: text

    ui/
    ├── static/
    │   ├── css/
    │   │   ├── common/
    │   │   └── pages/
    │   ├── js/
    │   │   ├── auth/
    │   │   ├── dashboard/
    │   │   ├── public/
    │   │   ├── surveys/
    │   │   └── utils/
    │   └── img/
    │       ├── raccoon_survey.ico
    │       └── raccoon_survey.png
    ├── templates/
    │   ├── base.html
    │   ├── components/
    │   │   ├── forms/
    │   │   ├── navbar.html
    │   │   └── ...
    │   ├── pages/
    │   │   ├── auth/
    │   │   ├── private/
    │   │   └── public/
    │   └── ...
    └── __init__.py

---

Key Directories
---------------

**`static/`**

This directory contains all the static assets that are served directly to the client without server-side processing.

- **`css/`**: Contains the project's stylesheets.
  - `common/`: Global styles applied throughout the application (e.g., `navbar.css`, `skeleton.css`).
  - `pages/`: Styles specific to certain pages (e.g., `login.css`).

- **`js/`**: Contains the JavaScript files responsible for the frontend logic and interactivity.
  - `auth/`: Scripts related to authentication (login, registration).
  - `dashboard/`: Logic for the main dashboard, including charts and metrics.
  - `public/`: Scripts for public-facing pages (e.g., the hamburger menu).
  - `surveys/`: JavaScript for creating, viewing, and managing surveys.
  - `utils/`: Reusable utility functions (e.g., `http.js` for API calls, `dom.js` for DOM manipulation).

- **`img/`**: Static images, icons, and other graphical assets.

---

**`templates/`**

This directory holds all the Jinja2 HTML templates, which are rendered on the server by Flask before being sent to the client.

- **`base.html`**: The main layout template that other pages extend. It typically includes the `<html>`, `<head>`, and `<body>` structure, as well as global assets.

- **`components/`**: Contains reusable UI fragments (partials) that can be included in multiple pages to avoid code duplication.
  - `forms/`: Reusable form components.
  - `navbar.html`: The top navigation bar.

- **`pages/`**: Contains the main templates for each page of the application, organized by access level.
  - `auth/`: Authentication pages (e.g., `login.html`, `register.html`).
  - `private/`: Pages that require authentication (e.g., `dashboard.html`).
  - `public/`: Pages accessible to everyone (e.g., `index.html`).

---

**`__init__.py`**

This file marks the `ui` directory as a Python package and contains the Flask Blueprint definition. The Blueprint organizes the UI-related routes and allows them to be registered with the main Flask application, effectively modularizing the UI as a self-contained component of the project.
