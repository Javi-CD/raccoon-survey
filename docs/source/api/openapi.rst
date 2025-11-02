OpenAPI (Swagger)
=================

.. ifconfig:: has_openapi

   Esta sección presenta la especificación OpenAPI del backend de Raccoon Survey.
   A partir de este documento se generan y documentan los endpoints HTTP, sus parámetros,
   cuerpos de petición y respuesta, códigos de estado y esquemas de datos.
   La especificación fuente reside en ``src/core/openapi.json`` y actúa como contrato de integración
   para clientes externos y herramientas de validación.

=================

   .. openapi:: ../../../src/core/openapi.json
      :encoding: utf-8

.. ifconfig:: not has_openapi

   .. warning::
      El complemento ``sphinxcontrib-openapi`` no está instalado.
      Instala las dependencias con ``python -m pip install -r requirements.txt`` para visualizar esta sección.
