# Documentación de la API PPTX (Sistema de Variables)

Esta API permite crear y modificar presentaciones de PowerPoint utilizando un sistema de **Variables Globales** con la sintaxis `{{variable}}`.

A diferencia de los métodos tradicionales de PowerPoint, no es necesario configurar "Placeholders" en la Vista Maestra. Puedes escribir variables directamente en cuadros de texto o en el Texto Alternativo de las imágenes.

📋 **Guía de creación de templates**: Para aprender cómo diseñar tus presentaciones consulta [`TEMPLATE_GUIDE.md`](TEMPLATE_GUIDE.md).

## Tabla de Contenidos

- [Información General](#información-general)
- [Sistema de Variables `{{}}`](#sistema-de-variables)
- [Endpoints](#endpoints)
  - [Templates](#templates)
  - [Presentaciones](#presentaciones)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## Información General

### URL Base

`http://localhost:8000`

### Funcionamiento

1. **Subes un Template (.pptx)** que contenga patrones como `{{nombre}}`.
2. **Creas una Presentación** basada en ese template.
3. **Reemplazas las Variables** enviando el nombre de la variable y el nuevo contenido.
4. **Descargas** el archivo final.

---

## Sistema de Variables `{{}}`

### Variables de Texto

Puedes poner `{{variable}}` en cualquier cuadro de texto.

- **Global**: Si repites `{{fecha}}` en 5 diapositivas, un solo llamado a la API actualizará todas.
- **Mixto**: Puedes escribir "Hola {{cliente}}, bienvenido" en un solo cuadro.

### Variables de Imagen

Para las imágenes, se utiliza el **Texto Alternativo (Alt Text)**.

1. Inserta una imagen cualquiera como referencia.
2. En sus propiedades, busca "Texto Alternativo".
3. Escribe `{{mi_imagen}}` o `{{image:mi_imagen}}`.

---

## Endpoints

### Templates

#### GET `/api/v1/templates`

Obtiene la lista de todos los templates subidos.

**Ejemplo con cURL:**

```bash
curl -X GET "http://localhost:8000/api/v1/templates"
```

**Response (200 OK):**

```json
{
  "templates": [
    {
      "template_id": "uuid-1",
      "filename": "uuid-1.pptx"
    }
  ]
}
```

---

#### POST `/api/v1/templates/upload`

Sube un nuevo template PPTX.

**Body (multipart/form-data):**

- `file`: [Archivo binario .pptx]

**Response (201 Created):**

```json
{
  "template_id": "uuid-of-new-template",
  "filename": "uploaded_template.pptx"
}
```

#### GET `/api/v1/templates/{template_id}/variables`

Escanea el template y devuelve todas las variables encontradas.

**Response:**

```json
{
  "template_id": "uuid",
  "variables": [
    { "name": "cliente", "type": "text", "slide_index": 0 },
    { "name": "foto_perfil", "type": "image", "slide_index": 1 }
  ]
}
```

---

### Presentaciones

#### GET `/api/v1/presentations`

Obtiene la lista de todas las presentaciones generadas.

**Ejemplo con cURL:**

```bash
curl -X GET "http://localhost:8000/api/v1/presentations"
```

**Response (200 OK):**

```json
{
  "presentations": [
    {
      "presentation_id": "uuid-pptx",
      "filename": "uuid-pptx.pptx"
    }
  ]
}
```

#### POST `/api/v1/presentations/{presentation_id}/text`

Reemplaza todas las ocurrencias de una variable de texto.

**Body:**

```json
{
  "variable_name": "cliente",
  "text": "Juan Pérez",
  "formatting": {
    "font_size": 24,
    "bold": true,
    "color": "#FF0000"
  }
}
```

#### POST `/api/v1/presentations/{presentation_id}/image`

Reemplaza una imagen identificada por su variable en el Alt Text.

**Body (multipart/form-data):**

- `variable_name`: "foto_perfil"
- `image`: [Archivo binario]

#### DELETE `/api/v1/templates/{template_id}`

Elimina un template del servidor.

**Ejemplo con cURL:**

```bash
curl -X DELETE "http://localhost:8000/api/v1/templates/{id}"
```

#### DELETE `/api/v1/presentations/{presentation_id}`

Elimina una presentación del servidor.

**Ejemplo con cURL:**

```bash
curl -X DELETE "http://localhost:8000/api/v1/presentations/{id}"
```

---

## Ejemplos de Uso (cURL)

**1. Reemplazar texto:**

```bash
curl -X POST "http://localhost:8000/api/v1/presentations/{id}/text" \
  -H "Content-Type: application/json" \
  -d '{
    "variable_name": "titulo",
    "text": "Reporte Anual 2024"
  }'
```

**2. Reemplazar imagen:**

```bash
curl -X POST "http://localhost:8000/api/v1/presentations/{id}/image" \
  -F "variable_name=logo_empresa" \
  -F "image=@logo.png"
```
