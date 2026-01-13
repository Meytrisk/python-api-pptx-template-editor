# Documentación de la API PPTX (Sistema de Variables)

Esta API permite crear y modificar presentaciones de PowerPoint utilizando un sistema de **Variables Globales** con la sintaxis `{{variable}}`.

---

## Tabla de Contenidos

- [Información General](#información-general)
- [Endpoints de Templates](#endpoints-de-templates)
- [Endpoints de Presentaciones](#endpoints-de-presentaciones)
- [Sistema de Variables `{{}}`](#sistema-de-variables)

---

## Información General

**URL Base:** `http://localhost:8000`
**Autenticación:** Bearer Token

- Header: `Authorization: Bearer <API_TOKEN>`
- Configuración: Variable de entorno `API_TOKEN`.

---

## Endpoints de Templates

### 1. Listar Templates

`GET /api/v1/templates`  
Devuelve todos los templates subidos al servidor.

### 2. Subir Template

`POST /api/v1/templates/upload`  
**Body (multipart/form-data):** `file` (archivo .pptx)

### 3. Escanear Variables

`GET /api/v1/templates/{template_id}/variables`  
Analiza el archivo y extrae todos los patrones `{{}}`.

### 4. Eliminar Template

`DELETE /api/v1/templates/{template_id}`

---

## Endpoints de Presentaciones

### 1. Listar Presentaciones

`GET /api/v1/presentations`  
Lista todas las presentaciones generadas actualmente.

### 2. Crear Presentación (Instancia)

`POST /api/v1/presentations/create`  
**Body (JSON):** `{"template_id": "uuid"}`  
_Este endpoint crea una copia de trabajo del template y devuelve un `presentation_id`._

### 3. Reemplazar Texto

`POST /api/v1/presentations/{presentation_id}/text`  
**Body (JSON):**

```json
{
  "variable_name": "nombre",
  "text": "Nuevo Valor",
  "formatting": { "bold": true, "font_size": 20 }
}
```

### 4. Reemplazar Imagen

`POST /api/v1/presentations/{presentation_id}/image`  
**Body (multipart/form-data):**

- `variable_name`: "foto_perfil"
- `image`: [Archivo binario]

#### POST `/api/v1/presentations/{presentation_id}/video`

Reemplaza una figura por un video (.mp4) identificado por su variable en el Alt Text.

**Body (multipart/form-data):**

- `variable_name`: "video_demo"
- `video`: [Archivo binario .mp4]
- `poster` (opcional): [Archivo binario imagen] - Si no se envía, se extraerá automáticamente del video.

---

### 5. Descargar Archivo

`GET /api/v1/presentations/{presentation_id}/download`  
Devuelve el archivo `.pptx` resultante.

### 6. Eliminar Presentación

`DELETE /api/v1/presentations/{presentation_id}`

---

## Sistema de Variables `{{}}`

- **Texto**: Escribe `{{nombre}}` en cualquier cuadro de texto.
- **Imagen**: Escribe `{{nombre}}` en el **Texto Alternativo** de una imagen.
