# Guía Detallada: Placeholders de Imagen con Alt Text
 
 Para que la API pueda intercambiar imágenes correctamente, el proceso actual **NO usa placeholders del Slide Master**. En su lugar, usa el **Texto Alternativo (Alt Text)** de una imagen de referencia.
 
 ## 1. Lógica del Sistema
 1.  Tú colocas una imagen de muestra en tu diapositiva (puede ser un logo genérico o un recuadro de color).
 2.  Le asignas un **Texto Alternativo** único (ej: `{{logo_cliente}}`).
 3.  La API busca esa imagen por su Alt Text.
 4.  Si la encuentra, **la reemplaza** por la imagen nueva que subiste, manteniendo exactamente la misma posición y dimensiones (alto y ancho).
 
 ## 2. Pasos para Configurar tu Template
 ### Paso 1: Insertar Imagen de Referencia
 - Inserta una imagen cualquiera en tu diapositiva (`Insertar` -> `Imagen`).
 - Ajusta su tamaño y posición exactamente como quieres que quede la imagen final.
 - **Nota**: La relación de aspecto (proporción ancho/alto) será heredada.
 
 ### Paso 2: Asignar Alt Text
 1.  Haz clic derecho sobre la imagen.
 2.  Selecciona **Ver Texto Alternativo...** (View Alt Text).
 3.  En el cuadro de texto (a veces dice "Descripción"), escribe el nombre de tu variable.
     *   *Recomendación*: Usa llaves para diferenciarlo, ej: `{{foto_portada}}`.
 
 *¡Listo! Esa imagen ahora es una "variable".*
 
 ## 3. Uso en la API
 Cuando llames al endpoint de inserción de imagen, en el campo `placeholder_name`, envía exactamente el texto que pusiste en el Alt Text.
 
 **Ejemplo:**
 *   Alt Text en PowerPoint: `{{logo_empresa}}`
 *   Campo `placeholder_name` en API: `{{logo_empresa}}`
 
 ## 4. Formatos Soportados
 La API acepta y reemplaza imágenes en formatos:
 *   ✅ PNG, JPG, JPEG, GIF, BMP, TIFF
 
 ## 5. Ventajas de este Método
 *   **WYSIWYG**: Lo que ves en el editor es exactamente donde quedará tu imagen.
 *   **Flexibilidad**: Puedes usar cualquier imagen como placeholder, incluso iconos o fotos de stock temporal.
 *   **Sin Master Slides**: No necesitas modificar el Patrón de Diapositivas necesariamente.
