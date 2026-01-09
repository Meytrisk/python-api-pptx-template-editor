# Documentación de la API PPTX

Esta documentación proporciona información detallada sobre todos los endpoints de la API PPTX, incluyendo los datos que deben enviarse y las respuestas esperadas.

📋 **Guía de creación de templates**: Para aprender cómo crear templates con placeholders en PowerPoint, consulta [`TEMPLATE_GUIDE.md`](TEMPLATE_GUIDE.md:1).

## Tabla de Contenidos

- [Información General](#información-general)
- [Autenticación](#autenticación)
- [Endpoints](#endpoints)
  - [Health Check](#health-check)
  - [Templates](#templates)
  - [Presentaciones](#presentaciones)
- [Códigos de Estado HTTP](#códigos-de-estado-http)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Trabajando con Placeholders](#trabajando-con-placeholders)

---

## Información General

### URL Base

```
http://localhost:8000
```

### Versión de la API

```
v1
```

### Content-Type

La API acepta los siguientes tipos de contenido:

- `application/json` - Para endpoints que envían datos JSON
- `multipart/form-data` - Para endpoints que suben archivos

### Formatos de Respuesta

Todas las respuestas están en formato JSON, excepto el endpoint de descarga que devuelve un archivo binario.

---

## Autenticación

Actualmente, la API no requiere autenticación. En un entorno de producción, se recomienda implementar autenticación JWT o API keys.

---

## Endpoints

### Health Check

#### GET `/`

Verifica el estado de la API.

**No requiere parámetros.**

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

**Campos de Respuesta:**
- `status` (string): Estado de la API ("healthy" o "unhealthy")
- `version` (string): Versión de la API

---

### Templates

#### POST `/api/v1/templates/upload`

Sube un template de PowerPoint (.pptx) al servidor.

**Request:**
- **Method:** POST
- **Content-Type:** `multipart/form-data`
- **Body:**
  - `file` (file, required): Archivo de PowerPoint (.pptx)

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/templates/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@mi_template.pptx"
```

**Response (201 Created):**
```json
{
  "template_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "550e8400-e29b-41d4-a716-446655440000.pptx",
  "message": "Template uploaded successfully"
}
```

**Campos de Respuesta:**
- `template_id` (string): Identificador único del template (UUID)
- `filename` (string): Nombre del archivo guardado
- `message` (string): Mensaje de confirmación

**Errores:**
- `400 Bad Request`: El archivo no es un .pptx válido
- `500 Internal Server Error`: Error al guardar el archivo

---

#### GET `/api/v1/templates/{template_id}/placeholders`

Obtiene todos los placeholders de un template específico.

**Request:**
- **Method:** GET
- **Path Parameters:**
  - `template_id` (string, required): ID del template

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/templates/550e8400-e29b-41d4-a716-446655440000/placeholders" \
  -H "accept: application/json"
```

**Response (200 OK):**
```json
{
  "template_id": "550e8400-e29b-41d4-a716-446655440000",
  "slides": [
    {
      "slide_index": 0,
      "placeholders": [
        {
          "idx": 0,
          "name": "Title 1",
          "type": "TITLE",
          "position": {
            "left": 4572000,
            "top": 2743200
          },
          "size": {
            "width": 9144000,
            "height": 1143000
          }
        },
        {
          "idx": 1,
          "name": "Picture Placeholder 2",
          "type": "PICTURE",
          "position": {
            "left": 457200,
            "top": 1600200
          },
          "size": {
            "width": 8229600,
            "height": 4572000
          }
        }
      ]
    }
  ]
}
```

**Campos de Respuesta:**
- `template_id` (string): ID del template
- `slides` (array): Lista de diapositivas con sus placeholders
  - `slide_index` (integer): Índice de la diapositiva
  - `placeholders` (array): Lista de placeholders en la diapositiva
    - `idx` (integer): Índice del placeholder (usado para insertar contenido)
    - `name` (string): Nombre del placeholder
    - `type` (string): Tipo de placeholder (TITLE, BODY, PICTURE, etc.)
    - `position` (object, optional): Posición del placeholder
      - `left` (number): Posición horizontal en EMUs
      - `top` (number): Posición vertical en EMUs
    - `size` (object, optional): Tamaño del placeholder
      - `width` (number): Ancho en EMUs
      - `height` (number): Alto en EMUs

**Errores:**
- `404 Not Found`: Template no encontrado
- `500 Internal Server Error`: Error al leer el template

---

#### DELETE `/api/v1/templates/{template_id}`

Elimina un template del servidor.

**Request:**
- **Method:** DELETE
- **Path Parameters:**
  - `template_id` (string, required): ID del template a eliminar

**Ejemplo con cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/templates/550e8400-e29b-41d4-a716-446655440000" \
  -H "accept: application/json"
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Template '550e8400-e29b-41d4-a716-446655440000' deleted successfully"
}
```

**Campos de Respuesta:**
- `success` (boolean): Estado de la operación
- `message` (string): Mensaje de confirmación

**Errores:**
- `404 Not Found`: Template no encontrado
- `500 Internal Server Error`: Error al eliminar el template

---

### Presentaciones

#### POST `/api/v1/presentations/create`

Crea una nueva presentación basada en un template existente.

**Request:**
- **Method:** POST
- **Content-Type:** `application/json`
- **Body:**
```json
{
  "template_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Campos del Request:**
- `template_id` (string, required): ID del template a usar

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/presentations/create" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

**Response (201 Created):**
```json
{
  "presentation_id": "660e8400-e29b-41d4-a716-446655440001",
  "template_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Presentation created successfully"
}
```

**Campos de Respuesta:**
- `presentation_id` (string): ID de la presentación creada (UUID)
- `template_id` (string): ID del template usado
- `message` (string): Mensaje de confirmación

**Errores:**
- `400 Bad Request`: Template ID inválido o no encontrado
- `500 Internal Server Error`: Error al crear la presentación

---

#### POST `/api/v1/presentations/{presentation_id}/text`

Inserta texto en un placeholder específico de la presentación.

**Request:**
- **Method:** POST
- **Content-Type:** `application/json`
- **Path Parameters:**
  - `presentation_id` (string, required): ID de la presentación
- **Body:**
```json
{
  "placeholder_name": "titulo_principal",
  "text": "Mi Título",
  "formatting": {
    "font_name": "Arial",
    "font_size": 36,
    "bold": true,
    "italic": false,
    "underline": false,
    "color": "#FF0000",
    "alignment": "CENTER",
    "vertical_alignment": "MIDDLE"
  }
}
```

**Campos del Request:**
- `placeholder_name` (string, required): **Nombre del placeholder** (obtenido del endpoint de placeholders)
- `text` (string, required): Texto a insertar
- `formatting` (object, optional): Opciones de formato del texto
  - `font_name` (string, optional): Nombre de la fuente (ej: "Arial", "Calibri")
  - `font_size` (integer, optional): Tamaño en puntos (1-400)
  - `bold` (boolean, optional): Texto en negrita
  - `italic` (boolean, optional): Texto en cursiva
  - `underline` (boolean, optional): Texto subrayado
  - `color` (string, optional): Color en formato hexadecimal (ej: "#FF0000")
  - `alignment` (string, optional): Alineación horizontal ("LEFT", "CENTER", "RIGHT", "JUSTIFY", "DISTRIBUTE")
  - `vertical_alignment` (string, optional): Alineación vertical ("TOP", "MIDDLE", "BOTTOM")

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/presentations/660e8400-e29b-41d4-a716-446655440001/text" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "placeholder_name": "titulo_principal",
    "text": "Mi Presentación",
    "formatting": {
      "font_size": 36,
      "bold": true,
      "alignment": "CENTER"
    }
  }'
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Text inserted successfully into placeholder 0"
}
```

**Campos de Respuesta:**
- `success` (boolean): Estado de la operación
- `message` (string): Mensaje de confirmación

**Errores:**
- `400 Bad Request`: Placeholder no encontrado o tipo incorrecto
- `404 Not Found`: Presentación no encontrada
- `500 Internal Server Error`: Error al insertar el texto

**Notas:**
- No se puede insertar texto en placeholders de tipo PICTURE
- El formato es opcional; si no se proporciona, se usa el formato por defecto del placeholder

---

#### POST `/api/v1/presentations/{presentation_id}/image`

Inserta una imagen en la presentación, reemplazando una imagen existente identificada por su **Texto Alternativo (Alt Text)**.

**Request:**
- **Method:** POST
- **Content-Type:** `multipart/form-data`
- **Path Parameters:**
  - `presentation_id` (string, required): ID de la presentación
- **Body:**
  - `placeholder_name`: (string, required): El **Texto Alternativo** de la imagen a reemplazar
  - `image` (file, required): Archivo de imagen

**Formatos de Imagen Soportados:**
- PNG
- JPG/JPEG
- GIF
- BMP
- TIFF

**Ejemplo con cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/presentations/660e8400-e29b-41d4-a716-446655440001/image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "placeholder_name=imagen_producto" \
  -F "image=@mi_imagen.png"
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Image inserted successfully into placeholder 1"
}
```

**Campos de Respuesta:**
- `success` (boolean): Estado de la operación
- `message` (string): Mensaje de confirmación

**Errores:**
- `400 Bad Request`: Placeholder no encontrado, tipo incorrecto, o formato de imagen inválido
- `404 Not Found`: Presentación no encontrada
- `500 Internal Server Error`: Error al insertar la imagen

**Notas:**
- **Alt Text**: La imagen original debe tener el Texto Alternativo configurado en PowerPoint.
- La imagen se estira proporcionalmente y se recorta para llenar el placeholder
- Los mejores resultados se obtienen cuando la relación de aspecto de la imagen y el placeholder son similares

---

#### GET `/api/v1/presentations/{presentation_id}/download`

Descarga la presentación generada como archivo .pptx.

**Request:**
- **Method:** GET
- **Path Parameters:**
  - `presentation_id` (string, required): ID de la presentación

**Ejemplo con cURL:**
```bash
curl -X GET "http://localhost:8000/api/v1/presentations/660e8400-e29b-41d4-a716-446655440001/download" \
  -H "accept: application/vnd.openxmlformats-officedocument.presentationml.presentation" \
  --output presentacion_final.pptx
```

**Response (200 OK):**
- **Content-Type:** `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- **Body:** Archivo binario .pptx

**Errores:**
- `404 Not Found`: Presentación no encontrada
- `500 Internal Server Error`: Error al descargar la presentación

---

#### DELETE `/api/v1/presentations/{presentation_id}`

Elimina una presentación del servidor.

**Request:**
- **Method:** DELETE
- **Path Parameters:**
  - `presentation_id` (string, required): ID de la presentación a eliminar

**Ejemplo con cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/presentations/660e8400-e29b-41d4-a716-446655440001" \
  -H "accept: application/json"
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Presentation '660e8400-e29b-41d4-a716-446655440001' deleted successfully"
}
```

**Campos de Respuesta:**
- `success` (boolean): Estado de la operación
- `message` (string): Mensaje de confirmación

**Errores:**
- `404 Not Found`: Presentación no encontrada
- `500 Internal Server Error`: Error al eliminar la presentación

---

## Códigos de Estado HTTP

| Código | Descripción |
|--------|-------------|
| 200 OK | La solicitud fue exitosa |
| 201 Created | El recurso fue creado exitosamente |
| 400 Bad Request | La solicitud es inválida o contiene datos incorrectos |
| 404 Not Found | El recurso solicitado no existe |
| 500 Internal Server Error | Error interno del servidor |

---

## Ejemplos de Uso

### Flujo Completo con Python

```python
import requests
import json

# Configuración
BASE_URL = "http://localhost:8000"

# 1. Subir template
print("1. Subiendo template...")
with open("mi_template.pptx", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/v1/templates/upload",
        files={"file": f}
    )
    template_data = response.json()
    template_id = template_data["template_id"]
    print(f"Template ID: {template_id}")

# 2. Obtener placeholders
print("\n2. Obteniendo placeholders...")
response = requests.get(
    f"{BASE_URL}/api/v1/templates/{template_id}/placeholders"
)
placeholders_data = response.json()
print(f"Placeholders: {json.dumps(placeholders_data, indent=2)}")

# 3. Crear presentación
print("\n3. Creando presentación...")
response = requests.post(
    f"{BASE_URL}/api/v1/presentations/create",
    json={"template_id": template_id}
)
presentation_data = response.json()
presentation_id = presentation_data["presentation_id"]
print(f"Presentation ID: {presentation_id}")

# 4. Insertar texto en título
print("\n4. Insertando texto en título...")
response = requests.post(
    f"{BASE_URL}/api/v1/presentations/{presentation_id}/text",
    json={
        "placeholder_name": "titulo_principal",
        "text": "Mi Presentación Generada",
        "formatting": {
            "font_size": 36,
            "bold": True,
            "alignment": "CENTER",
            "color": "#2E86AB"
        }
    }
)
print(f"Resultado: {response.json()}")

# 5. Insertar texto en cuerpo
print("\n5. Insertando texto en cuerpo...")
response = requests.post(
    f"{BASE_URL}/api/v1/presentations/{presentation_id}/text",
    json={
        "placeholder_name": "descripcion_producto",
        "text": "Esta es una presentación generada automáticamente usando la API PPTX.",
        "formatting": {
            "font_size": 18,
            "alignment": "LEFT"
        }
    }
)
print(f"Resultado: {response.json()}")

# 6. Insertar imagen
print("\n6. Insertando imagen...")
with open("mi_imagen.png", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/v1/presentations/{presentation_id}/image",
        data={"placeholder_name": "imagen_producto"},
        files={"image": f}
    )
    print(f"Resultado: {response.json()}")

# 7. Descargar presentación
print("\n7. Descargando presentación...")
response = requests.get(
    f"{BASE_URL}/api/v1/presentations/{presentation_id}/download"
)
with open("presentacion_final.pptx", "wb") as f:
    f.write(response.content)
print("Presentación descargada como 'presentacion_final.pptx'")

print("\n¡Proceso completado!")
```

### Flujo Completo con JavaScript (Fetch API)

```javascript
const BASE_URL = "http://localhost:8000";

// 1. Subir template
async function uploadTemplate(file) {
  const formData = new FormData();
  formData.append("file", file);
  
  const response = await fetch(`${BASE_URL}/api/v1/templates/upload`, {
    method: "POST",
    body: formData
  });
  
  return await response.json();
}

// 2. Obtener placeholders
async function getPlaceholders(templateId) {
  const response = await fetch(
    `${BASE_URL}/api/v1/templates/${templateId}/placeholders`
  );
  return await response.json();
}

// 3. Crear presentación
async function createPresentation(templateId) {
  const response = await fetch(`${BASE_URL}/api/v1/presentations/create`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ template_id: templateId })
  });
  return await response.json();
}

// 4. Insertar texto
async function insertText(presentationId, placeholderName, text, formatting = {}) {
  const response = await fetch(
    `${BASE_URL}/api/v1/presentations/${presentationId}/text`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        placeholder_name: placeholderName,
        text: text,
        formatting: formatting
      })
    }
  );
  return await response.json();
}

// 5. Insertar imagen
async function insertImage(presentationId, placeholderName, imageFile) {
  const formData = new FormData();
  formData.append("placeholder_name", placeholderName);
  formData.append("image", imageFile);
  
  const response = await fetch(
    `${BASE_URL}/api/v1/presentations/${presentationId}/image`,
    {
      method: "POST",
      body: formData
    }
  );
  return await response.json();
}

// 6. Descargar presentación
async function downloadPresentation(presentationId, filename) {
  const response = await fetch(
    `${BASE_URL}/api/v1/presentations/${presentationId}/download`
  );
  const blob = await response.blob();
  
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}

// Ejemplo de uso completo
async function main() {
  // Subir template
  const templateFile = document.getElementById("templateInput").files[0];
  const templateData = await uploadTemplate(templateFile);
  console.log("Template ID:", templateData.template_id);
  
  // Obtener placeholders
  const placeholders = await getPlaceholders(templateData.template_id);
  console.log("Placeholders:", placeholders);
  
  // Crear presentación
  const presentationData = await createPresentation(templateData.template_id);
  console.log("Presentation ID:", presentationData.presentation_id);
  
  // Insertar texto
  await insertText(
    presentationData.presentation_id,
    "titulo_principal",
    "Mi Título",
    { font_size: 36, bold: true, alignment: "CENTER" }
  );
  
  // Insertar imagen
  const imageFile = document.getElementById("imageInput").files[0];
  await insertImage(presentationData.presentation_id, "imagen_producto", imageFile);
  
  // Descargar presentación
  await downloadPresentation(
    presentationData.presentation_id,
    "presentacion_final.pptx"
  );
}
```

---

## Tipos de Placeholders

| Tipo | Descripción | Acepta Texto | Acepta Imágenes |
|------|-------------|---------------|-----------------|
| TITLE | Título de la diapositiva | ✅ | ❌ |
| BODY | Cuerpo de texto | ✅ | ❌ |
| PICTURE | Imagen | ❌ | ✅ |
| CENTER_TITLE | Título centrado | ✅ | ❌ |
| SUBTITLE | Subtítulo | ✅ | ❌ |
| OBJECT | Objeto genérico | ✅ | ❌ |
| CHART | Gráfico | ✅ | ❌ |
| TABLE | Tabla | ✅ | ❌ |
| DATE | Fecha | ✅ | ❌ |
| SLIDE_NUMBER | Número de diapositiva | ✅ | ❌ |
| FOOTER | Pie de página | ✅ | ❌ |
| HEADER | Encabezado | ✅ | ❌ |

---

## Trabajando con Placeholders

### ¿Qué son los Placeholders?

Los placeholders son elementos predefinidos en una diapositiva de PowerPoint que indican dónde se debe insertar contenido específico. Cada placeholder tiene:

- **Nombre único (`name`)**: Identificador de texto que lo distingue de otros placeholders en la misma diapositiva
- **Índice (`idx`)**: Identificador numérico del placeholder
- **Tipo**: Define qué tipo de contenido puede aceptar (texto, imagen, etc.)
- **Posición y tamaño**: Ubicación y dimensiones predefinidas
- **Formato predeterminado**: Fuente, color, alineación, etc.

### Cómo Obtener los Placeholders de un Template

Antes de insertar contenido en una presentación, debes conocer los placeholders disponibles en el template:

```bash
curl -X GET "http://localhost:8000/api/v1/templates/{template_id}/placeholders" \
  -H "accept: application/json"
```

**Response de ejemplo:**
```json
{
  "template_id": "550e8400-e29b-41d4-a716-446655440000",
  "slides": [
    {
      "slide_index": 0,
      "placeholders": [
        {
          "idx": 0,
          "name": "titulo_principal",
          "type": "TITLE",
          "position": {
            "left": 4572000,
            "top": 2743200
          },
          "size": {
            "width": 9144000,
            "height": 1143000
          }
        },
        {
          "idx": 1,
          "name": "descripcion_producto",
          "type": "BODY",
          "position": {
            "left": 457200,
            "top": 1600200
          },
          "size": {
            "width": 8229600,
            "height": 4572000
          }
        },
        {
          "idx": 2,
          "name": "imagen_producto",
          "type": "PICTURE",
          "position": {
            "left": 457200,
            "top": 1600200
          },
          "size": {
            "width": 8229600,
            "height": 4572000
          }
        }
      ]
    }
  ]
}
```

### Usar el Nombre del Placeholder

**IMPORTANTE**: La API usa el **nombre** del placeholder para insertar contenido, no el índice numérico. Esto hace que los nombres sean más estables y descriptivos.

```python
# Insertar texto en el placeholder con nombre "titulo_principal"
requests.post(
    f"http://localhost:8000/api/v1/presentations/{presentation_id}/text",
    json={
        "placeholder_name": "titulo_principal",  # Usa el NOMBRE del placeholder
        "text": "Mi Título"
    }
)

# Insertar imagen en el placeholder con nombre "imagen_producto"
with open("mi_imagen.png", "rb") as f:
    requests.post(
        f"http://localhost:8000/api/v1/presentations/{presentation_id}/image",
        data={"placeholder_name": "imagen_producto"},  # Usa el NOMBRE del placeholder
        files={"image": f}
    )
```

### Crear Templates con Placeholders

Para crear templates con placeholders, tienes varias opciones:

1. **Usar layouts predefinidos de PowerPoint**
   - PowerPoint incluye layouts con placeholders listos para usar
   - Ve a **Inicio** > **Diseño de diapositiva**
   - Elige un layout que tenga los placeholders que necesitas

2. **Crear un Slide Master personalizado**
   - Ve a **Vista** > **Slide Master**
   - Agrega placeholders personalizados
   - Define el formato predeterminado

3. **Usar python-pptx**
   - Crea templates programáticamente
   - Usa layouts predefinidos de python-pptx

📋 **Guía completa**: Para más detalles sobre cómo crear templates con placeholders, consulta [`TEMPLATE_GUIDE.md`](TEMPLATE_GUIDE.md:1).

### Errores Comunes con Placeholders

#### Error: "Cannot insert text into a picture placeholder"

**Causa**: Intentaste insertar texto en un placeholder de tipo PICTURE.

**Solución**: Usa un placeholder de tipo TITLE, BODY, u otro que acepte texto.

#### Error: "Cannot insert image into a BODY placeholder"

**Causa**: Intentaste insertar una imagen en un placeholder que no es de tipo PICTURE.

**Solución**: Usa un placeholder de tipo PICTURE para insertar imágenes.

#### Error: "Placeholder with name 'X' not found"

**Causa**: El nombre del placeholder no existe en la presentación.

**Solución**:
- Verifica los placeholders del template usando el endpoint `/api/v1/templates/{template_id}/placeholders`
- Usa el `name` correcto del placeholder

---

## Consideraciones Importantes

1. **Nombres de Placeholders**: La API utiliza el `name` del placeholder para insertar contenido. Estos nombres deben obtenerse usando el endpoint `/api/v1/templates/{template_id}/placeholders`.

2. **Persistencia**: Los templates y presentaciones se guardan en el servidor. Se recomienda descargar las presentaciones generadas y eliminarlas del servidor cuando ya no sean necesarias.

3. **Imágenes Temporales**: Las imágenes subidas para insertar en presentaciones se eliminan automáticamente después de ser procesadas.

4. **Tamaño de Archivos**: No hay límite de tamaño de archivo implementado actualmente. En producción, se recomienda implementar límites para evitar problemas de rendimiento.

5. **Concurrencia**: La API no maneja concurrencia de forma explícita. Si múltiples usuarios intentan modificar la misma presentación simultáneamente, pueden ocurrir conflictos.

---

## Soporte

Para preguntas o problemas, por favor abre un issue en el repositorio del proyecto.
