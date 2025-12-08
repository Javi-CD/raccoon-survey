.. _ui_introduction:

Introduction
============

**Raccoon Survey UI** is the graphical user interface for the Raccoon Survey system. Its purpose is to allow the user to interact with the backend in an intuitive, fast, and modern way, ensuring a smooth and accessible user experience.

This interface has been designed as a traditional server-side rendered (SSR) web application, where the Flask backend is responsible for generating and serving the HTML pages.

Technologies Used
-----------------

The interface is developed using standard web technologies and a modern CSS framework to ensure compatibility and high development speed:

- **HTML5 and Jinja2**: The structure of the pages is defined with HTML5, while `Jinja2` is used as the server-side template engine. This allows for generating dynamic content and integrating backend logic directly into the views.

- **CSS3 and TailwindCSS**: For styling, **TailwindCSS** is used, a "utility-first" CSS framework that allows for building complex designs quickly without writing custom CSS. This ensures consistency and maintainability throughout the application.

- **JavaScript (ES6)**: Client-side logic and dynamic events are managed with modern JavaScript (ES6+). It is used to add interactivity to pages, validate forms, and communicate with the backend without needing to reload the page.

- **Fetch API**: Asynchronous communication with the Flask backend is handled through the **Fetch API**, a modern standard for making HTTP requests. For example, to get survey data:

  .. code-block:: javascript

    async function getSurveyData(surveyId) {
      try {
        const response = await fetch(`/api/surveys/${surveyId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${your_jwt_token}`
          }
        });
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Survey data:', data);
        return data;
      } catch (error) {
        console.error('Could not fetch survey data:', error);
      }
    }

Architecture and Design
-----------------------

The user interface follows a server-side rendering (SSR) architecture, where the main responsibility lies with the Flask backend.

- **Server-Side Rendering (SSR)**: The routes defined in `src/ui/routes` use Flask to render Jinja2 templates (`.html`) and serve them to the client. This approach improves initial load performance and search engine indexing.

- **File Structure**: The UI code is organized as follows:
  - `src/ui/static/`: Contains all static files, such as compiled CSS stylesheets, images, and client-side JavaScript files.
  - `src/ui/templates/`: Stores the Jinja2 templates, organized into reusable components and full-page views.
  - `src/ui/routes/`: Defines the Flask routes that map URLs to the functions that render the templates.

- **Authentication Middleware**: The interface is protected by a middleware (`session_middleware`) that verifies the user's session before allowing access to protected routes, redirecting to the login page if necessary.

Main Features
-------------

- **Responsive Design**: The interface is designed to work on a wide variety of devices, from desktop computers to mobile phones.
- **Modern and Intuitive Interface**: Thanks to TailwindCSS and a user-centered design, navigation is clear and actions are easy to perform.
- **Smooth User Experience**: The use of JavaScript for dynamic interactions and asynchronous communication with the backend minimizes page reloads, creating a faster and more pleasant experience.
