.. _ui_api_connection:

Backend Communication (API)
===========================

The UI communicates with the backend through HTTP requests, consuming a RESTful API that uses JSON as its data exchange format. All communication is handled securely and efficiently using the modern **Fetch API**, abstracted through a centralized utility module.

---

HTTP Utility Module
-------------------

To centralize and simplify API calls, the project uses a wrapper located at `static/js/utils/http.js`. This module encapsulates the logic for making `fetch` requests, automatically including authentication headers and handling responses.

**Core Functions:**

- `get(endpoint)`: Performs a `GET` request.
- `post(endpoint, body)`: Performs a `POST` request with a JSON body.
- `put(endpoint, body)`: Performs a `PUT` request.
- `del(endpoint)`: Performs a `DELETE` request.

**Example: `http.js` wrapper**

This utility simplifies making authenticated API calls from anywhere in the frontend code.

.. code-block:: javascript

  // static/js/utils/http.js

  async function request(endpoint, method = 'GET', body = null) {
      const headers = {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('access_token')}` // Attach JWT
      };

      const options = {
          method,
          headers
      };

      if (body) {
          options.body = JSON.stringify(body);
      }

      const response = await fetch(`/api/v1${endpoint}`, options);

      if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.message || 'API request failed');
      }

      return response.json();
  }

  export const get = (endpoint) => request(endpoint, 'GET');
  export const post = (endpoint, body) => request(endpoint, 'POST', body);
  export const put = (endpoint, body) => request(endpoint, 'PUT', body);
  export const del = (endpoint) => request(endpoint, 'DELETE');


---

Authentication and JWT
----------------------

For protected routes, the frontend sends a **JSON Web Token (JWT)** in the `Authorization` header of each request. This token is obtained during login and stored securely in `localStorage`. The `http.js` utility automatically attaches this token to every outgoing request, simplifying session management.

---

Usage Example
-------------

With the `http.js` module, fetching data from the backend becomes clean and straightforward.

**Example: Fetching a list of surveys**

.. code-block:: javascript

  import { get } from '/static/js/utils/http.js';

  async function loadSurveys() {
      try {
          const surveys = await get('/surveys/');
          console.log('Surveys loaded:', surveys);
          // --> Render surveys in the UI
      } catch (error) {
          console.error('Failed to load surveys:', error.message);
          // --> Show an error notification to the user
      }
  }

  loadSurveys();
