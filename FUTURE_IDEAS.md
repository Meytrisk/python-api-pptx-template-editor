# Ideas Futuras y Mejoras Pendientes

Este documento registra funcionalidades planificadas para el futuro que no se desarrollarán en la fase actual.

## 1. Procesamiento por Lote (Batch Content)

- **Objetivo**: Permitir inyectar múltiples textos e imágenes en una sola llamada API para reducir la latencia y el número de peticiones desde herramientas como n8n.
- **Implementación**:
  - Endpoint `POST /api/v1/presentations/{id}/batch`.
  - Soporte para imágenes en formato **Base64** dentro del JSON.
  - Procesamiento secuencial o paralelo de reemplazos en una sola sesión de apertura del archivo PPTX.

## 2. Soporte para Tablas Dinámicas

- **Objetivo**: Poder inyectar filas de datos en tablas existentes identificadas por variables en sus descripciones.

## 3. Previsualización de diapositivas

- **Objetivo**: Endpoint para generar una imagen (PNG/JPG) de una diapositiva específica para previsualizar cambios.

## 4. Inserción de Videos (`{{video:nombre}}`)

- **Objetivo**: Reemplazar figuras por videos (.mp4) manteniendo posición y controlando el aspect ratio.
- **Notas Técnicas**:
  - Usar el método experimental `shapes.add_movie()` de `python-pptx`.
  - Requiere una "poster frame image" (imagen estática de previsualización) obligatoria.
  - Gestión de Aspect Ratio: Implementar lógica de "Letterboxing" (añadir barras) o "Zoom/Crop" para que el video no se deforme si la figura original tiene dimensiones distintas.
  - Posible dependencia adicional (`moviepy` o similar) si se desea extraer el poster frame del video automáticamente.

## 5. Nombres Personalizados para Templates

- **Objetivo**: Permitir que el usuario asigne un nombre descriptivo al subir un template (ej: "Propuesta_Comercial_V1") en lugar de depender solo del ID o el nombre del archivo original.

## 6. Persistencia de Metadatos de Presentación

- **Objetivo**: Cuando se crea una presentación, guardar la relación con su template de origen (ID y Nombre del template).
- **Caso de Uso**: Poder consultar una presentación y saber exactamente qué diseño base utilizó.
