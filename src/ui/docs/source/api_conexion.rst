Comunicación con el Backend
===========================

La interfaz se comunica con el backend mediante peticiones HTTP usando la **Fetch API**.

**Ejemplo de solicitud:**

.. code-block:: javascript

   fetch('/api/tasks', {
       method: 'GET',
       headers: { 'Content-Type': 'application/json' }
   })
   .then(response => response.json())
   .then(data => {
       console.log(data);
   })
   .catch(error => console.error('Error:', error));

**Endpoints comunes:**
- `/api/tasks` → obtiene las tareas disponibles.
- `/api/projects` → consulta o crea proyectos.
- `/api/users` → gestión de usuarios y roles.
