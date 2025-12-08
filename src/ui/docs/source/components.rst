.. _ui_components:

Main Components
===============

The **UI** module of *Raccoon Survey* is composed of a series of reusable components,
designed under a modular approach.
Each component fulfills a specific function within the application and maintains a clear separation between structure (HTML),
styles (CSS), and behavior (JavaScript).

The main ones are described below:

---

Navbar
------

**Description:**
Top navigation bar that provides quick access to the main sections of the system.

**Features:**
- Includes the system logo and navigation links (Home, Dashboard, Settings, etc.).
- Contains a dropdown menu for the authenticated user's profile.
- It remains fixed (sticky) at the top of the interface.
- Adaptable to small screens through a *hamburger* menu.

**Code Example (Jinja2/HTML):**
The Navbar is included in the base templates using a Jinja2 `include` statement, promoting reusability.

.. code-block:: html

  {% include 'components/navbar.html' %}

**Related Files:**
- `templates/components/navbar.html`
- `static/js/public/hamburger.js`
- `static/css/common/navbar.css`

---

Dashboard
---------

**Description:**
Main panel that presents general and analytical information of the system, including metrics, graphics, and quick access.

**Features:**
- Displays data from the backend through `fetch` requests.
- Contains visual components such as cards, statistical charts, and tables.
- Structure based on `CSS Grid` to maintain a flexible distribution.
- Allows dynamic content reloading without refreshing the entire page.

**Related Files:**
- `templates/pages/private/dashboard.html`
- `static/js/dashboard/`
- `static/css/common/skeleton.css`

---

Forms
-----

**Description:**
Components used for the creation, editing, and deletion of records (users, surveys, tasks, etc.).

**Features:**
- Real-time validations using JavaScript (without reloading the page).
- Dynamic error messages and visual feedback to the user.
- Styles consistent with the global dark mode.
- Data submission via the **Fetch API** to the Flask backend endpoints.

**Related Files:**
- `templates/components/forms/` (example: `templates/components/forms/surveys/create.html`)
- `static/js/surveys/create-modal.js`
- `static/js/utils/http.js`

---

Modals
------

**Description:**
Pop-up windows used to confirm actions, display additional information, or edit items without leaving the current view.

**Features:**
- Implemented with dynamic HTML injected by JavaScript.
- They have smooth appearance and closing animations.
- Support custom events (`onOpen`, `onClose`, `onSubmit`).
- Designed with rounded corners and a translucent background.

**Code Example (JavaScript):**
Modals are often managed by utility functions that handle their lifecycle.

.. code-block:: javascript

  import { openModal, closeModal } from '/static/js/utils/drawer.js';

  const myModal = document.getElementById('my-modal');

  // To open
  openModal(myModal);

  // To close
  closeModal(myModal);


**Related Files:**
- `static/js/utils/drawer.js`
- The HTML for modals is usually part of the page that uses them.

---

Notifications
-------------

**Description:**
Visual alert system to inform the user about successful actions, errors, or warnings.

**Features:**
- Compatible with different types of notifications: *success, error, info, warning*.
- They disappear automatically after a configurable time.
- Implemented in JavaScript using dynamic HTML templates.
- They are displayed in the upper right corner of the screen.

**Code Example (JavaScript):**
A utility function can be used to trigger notifications.

.. code-block:: javascript

  import { showNotification } from '/static/js/utils/dom.js';

  // Show a success notification
  showNotification('The operation was successful', 'success');

  // Show an error notification
  showNotification('Something went wrong', 'error');

**Related Files:**
- `static/js/utils/dom.js`
- The CSS is part of the global styles.
