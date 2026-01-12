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
