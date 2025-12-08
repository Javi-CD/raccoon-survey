.. _ui_styles:

Styles and Design
=================

The UI of *Raccoon Survey* is built with a **"Dark Mode First"** philosophy, ensuring a modern, elegant, and visually comfortable experience. The design relies on a utility-first CSS framework, **TailwindCSS**, which allows for rapid development and a highly maintainable codebase.

---

Design Philosophy
-----------------

- **Dark Mode First**: The entire interface is designed primarily for a dark theme, using a palette of neutral grays, deep blues, and vibrant accent colors for interactive elements. This reduces eye strain and provides a sleek, professional look.
- **Minimalism and Clarity**: The design prioritizes simplicity, with generous whitespace, clean typography, and a clear visual hierarchy to guide the user.
- **Consistency**: A consistent design language is used across all components, from buttons and forms to modals and notifications, creating a cohesive and predictable user experience.

---

Technology Stack
----------------

- **TailwindCSS**: A utility-first CSS framework that provides low-level utility classes to build custom designs directly in the HTML. This avoids the need for writing custom CSS and ensures a consistent and scalable styling system.
- **PostCSS**: Used to process the TailwindCSS directives and generate the final CSS bundle.
- **Google Fonts**: The project uses modern, readable fonts like *Inter* and *Poppins*, imported from Google Fonts to ensure high-quality typography.

---

Responsive Design
-----------------

The application is fully responsive and adapts to a wide range of screen sizes, from mobile phones to large desktop monitors. The responsive design is achieved using Tailwind's breakpoint prefixes (`sm:`, `md:`, `lg:`, `xl:`), which make it easy to apply different styles at different screen sizes.

**Example: Responsive Grid**

.. code-block:: html

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- This will be a single column on mobile, two columns on medium screens, and three columns on large screens -->
    <div class="bg-gray-800 p-4 rounded-lg">Item 1</div>
    <div class="bg-gray-800 p-4 rounded-lg">Item 2</div>
    <div class="bg-gray-800 p-4 rounded-lg">Item 3</div>
  </div>

---

Global Styles and Configuration
-------------------------------

- **`tailwind.config.js`**: This file, located in the `src/ui/` directory, is used to customize the default TailwindCSS configuration. It defines the color palette, fonts, spacing, and other design tokens to match the project's brand identity.
- **`static/css/main.css`**: This is the main stylesheet where the TailwindCSS directives (`@tailwind base;`, `@tailwind components;`, `@tailwind utilities;`) are included. It is processed by PostCSS to generate the final CSS file with all the utility classes.
