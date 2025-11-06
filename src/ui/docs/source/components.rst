Componentes Principales
=======================

El módulo de interfaz de usuario (**UI**) de *Raccoon Survey* está compuesto por una serie de componentes reutilizables,
diseñados bajo un enfoque modular.  
Cada componente cumple una función específica dentro de la aplicación y mantiene una separación clara entre estructura (HTML),
estilos (CSS) y comportamiento (JavaScript).

A continuación, se describen los principales:

---

Navbar
------

**Descripción:**  
Barra de navegación superior que proporciona acceso rápido a las secciones principales del sistema.

**Características:**
- Incluye el logotipo del sistema y enlaces de navegación (Inicio, Dashboard, Configuración, etc.).
- Contiene un menú desplegable para el perfil del usuario autenticado.
- Se mantiene fija (sticky) en la parte superior de la interfaz.
- Adaptable a pantallas pequeñas mediante menú tipo *hamburguesa*.

**Archivos relacionados:**
- `components/navbar.html`
- `static/js/navbar.js`
- `static/css/navbar.css`

---

Dashboard
---------

**Descripción:**  
Panel principal que presenta información general y analítica del sistema, incluyendo métricas, gráficos y accesos rápidos.

**Características:**
- Muestra datos provenientes del backend mediante peticiones `fetch`.
- Contiene componentes visuales como tarjetas, gráficos estadísticos y tablas.
- Estructura basada en `CSS Grid` para mantener una distribución flexible.
- Permite recarga dinámica de contenido sin refrescar la página completa.

**Archivos relacionados:**
- `templates/dashboard.html`
- `static/js/dashboard.js`
- `static/css/dashboard.css`

---

Formularios
------------

**Descripción:**  
Componentes utilizados para la creación, edición y eliminación de registros (usuarios, encuestas, tareas, etc.).

**Características:**
- Validaciones en tiempo real mediante JavaScript (sin recargar la página).
- Mensajes de error dinámicos y retroalimentación visual al usuario.
- Estilos coherentes con el modo oscuro global.
- Envío de datos mediante la **Fetch API** hacia los endpoints del backend Flask.

**Archivos relacionados:**
- `components/forms.html`
- `static/js/forms.js`
- `static/css/forms.css`

---

Modales
-------

**Descripción:**  
Ventanas emergentes utilizadas para confirmar acciones, mostrar información adicional o editar elementos sin salir de la vista actual.

**Características:**
- Implementados con HTML dinámico inyectado por JavaScript.
- Cuentan con animaciones suaves de aparición y cierre.
- Soportan eventos personalizados (`onOpen`, `onClose`, `onSubmit`).
- Diseñados con esquinas redondeadas y fondo translúcido.

**Archivos relacionados:**
- `components/modal.html`
- `static/js/modal.js`
- `static/css/modal.css`

---

Notificaciones
---------------

**Descripción:**  
Sistema de alertas visuales para informar al usuario sobre acciones exitosas, errores o advertencias.

**Características:**
- Compatible con diferentes tipos de notificación: *éxito, error, información, advertencia*.
- Desaparecen automáticamente tras un tiempo configurable.
- Implementadas en JavaScript mediante plantillas HTML dinámicas.
- Se muestran en la esquina superior derecha de la pantalla.

**Archivos relacionados:**
- `components/alerts.html`
- `static/js/alerts.js`
- `static/css/alerts.css`
