# PPTX API

API REST para crear y modificar presentaciones de PowerPoint utilizando la librería python-pptx.

- [Documentación Detallada de la API](API_DOCUMENTATION.md)
- [Guía de Creación de Templates](TEMPLATE_GUIDE.md)
- [Guía de Imágenes (Alt Text)](IMAGE_GUIDE.md)
- [Guía de Despliegue (PAAS)](DEPLOY.md)

✨ **IMPORTANTE**: La API usa **nombres de placeholders** para insertar contenido, no índices numéricos. Esto hace que los nombres sean más estables y descriptivos.

## Características

- ✅ Subir templates de PowerPoint (.pptx)
- ✅ Crear presentaciones desde templates
- ✅ Insertar texto en placeholders con formato avanzado
- ✅ Insertar imágenes que se adaptan automáticamente a los placeholders
- ✅ Descargar presentaciones generadas
- ✅ Documentación interactiva con Swagger UI

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd pptx
```

2. Crear un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Iniciar el servidor de desarrollo:

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O ejecutar directamente:
```bash
python app/main.py
```

La API estará disponible en:
- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

## Despliegue con Docker

### Requisitos Previos

- Docker instalado en tu sistema
- Docker Compose instalado (opcional, para docker-compose)

### Opción 1: Usar Docker Compose (Recomendado)

Esta es la forma más sencilla de desplegar la API con persistencia de datos.

1. **Construir y ejecutar el contenedor:**
```bash
docker-compose up -d
```

2. **Verificar que el contenedor está corriendo:**
```bash
docker-compose ps
```

3. **Ver los logs:**
```bash
docker-compose logs -f pptx-api
```

4. **Detener el contenedor:**
```bash
docker-compose down
```

5. **Reiniciar el contenedor:**
```bash
docker-compose restart
```

### Opción 2: Usar Docker Directamente

1. **Construir la imagen:**
```bash
docker build -t pptx-api .
```

2. **Ejecutar el contenedor:**
```bash
docker run -d \
  --name pptx-api \
  -p 8000:8000 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  pptx-api
```

**En Windows (PowerShell):**
```powershell
docker run -d `
  --name pptx-api `
  -p 8000:8000 `
  -v ${PWD}/uploads:/app/uploads `
  -v ${PWD}/outputs:/app/outputs `
  pptx-api
```

3. **Verificar que el contenedor está corriendo:**
```bash
docker ps
```

4. **Ver los logs:**
```bash
docker logs -f pptx-api
```

5. **Detener el contenedor:**
```bash
docker stop pptx-api
```

6. **Eliminar el contenedor:**
```bash
docker rm pptx-api
```

### Volumenes y Persistencia

La API utiliza volúmenes de Docker para persistir los archivos:

- **`/app/uploads/templates`**: Templates subidos por los usuarios
- **`/app/uploads/images`**: Imágenes temporales (se eliminan después de usarlas)
- **`/app/outputs`**: Presentaciones generadas

En el archivo [`docker-compose.yml`](docker-compose.yml:1), estos volúmenes están mapeados a directorios locales:
```yaml
volumes:
  - ./uploads:/app/uploads
  - ./outputs:/app/outputs
```

Esto significa que:
- Los templates subidos se guardarán en `./uploads/templates/` en tu máquina
- Las presentaciones generadas se guardarán en `./outputs/` en tu máquina
- Los datos persisten incluso si el contenedor se detiene o se elimina

### Health Check

El contenedor incluye un health check que verifica si la API está funcionando correctamente:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

Para verificar el estado de salud del contenedor:
```bash
docker inspect --format='{{.State.Health.Status}}' pptx-api
```

### Variables de Entorno

Actualmente, la API no requiere variables de entorno obligatorias. Sin embargo, puedes configurar:

- `PYTHONUNBUFFERED=1`: Deshabilita el buffering de salida de Python (ya configurado por defecto)

### Despliegue en Producción

Para despliegue en producción, considera:

1. **Usar un servidor de producción:**
Modifica el [`Dockerfile`](Dockerfile:1) para usar un servidor de producción como Gunicorn:
```dockerfile
CMD ["gunicorn", "app.main:app", "--workers", "4", "--bind", "0.0.0.0:8000"]
```

2. **Configurar límites de recursos:**
```bash
docker run -d \
  --name pptx-api \
  -p 8000:8000 \
  --memory="512m" \
  --cpus="1.0" \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/outputs:/app/outputs \
  pptx-api
```

3. **Usar un reverse proxy (Nginx):**
Configura Nginx como reverse proxy para manejar SSL, compresión, y balanceo de carga.

4. **Configurar CORS:**
Modifica el archivo [`app/main.py`](app/main.py:1) para especificar los orígenes permitidos en producción:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-dominio.com"],  # Especificar dominios reales
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Solución de Problemas

#### El contenedor no inicia
```bash
# Ver logs del contenedor
docker logs pptx-api

# Verificar que el puerto 8000 no está en uso
netstat -tuln | grep 8000  # Linux/Mac
netstat -ano | findstr :8000  # Windows
```

#### Error de permisos en volúmenes
```bash
# Asegúrate de que los directorios locales existen
mkdir -p uploads/templates uploads/images outputs

# Ajustar permisos si es necesario
chmod -R 755 uploads outputs
```

#### El health check falla
```bash
# Verificar que la API responde
curl http://localhost:8000/health

# Ver logs del contenedor
docker logs pptx-api
```

### Actualizar la Aplicación

Para actualizar la aplicación después de hacer cambios:

1. **Detener y eliminar el contenedor:**
```bash
docker-compose down
```

2. **Reconstruir la imagen:**
```bash
docker-compose build --no-cache
```

3. **Iniciar el contenedor:**
```bash
docker-compose up -d
```

### Limpieza

Para eliminar todos los recursos de Docker relacionados con el proyecto:

```bash
# Detener y eliminar contenedores
docker-compose down

# Eliminar imágenes
docker rmi pptx-api

# Eliminar volúmenes (¡CUIDADO! Esto eliminará todos los datos)
docker-compose down -v
```

## Estructura del Proyecto

```
pptx/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point de FastAPI
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── templates.py    # Endpoints de templates
│   │       └── presentations.py # Endpoints de presentaciones
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py          # Pydantic models
│   │   └── enums.py            # Enumeraciones
│   └── services/
│       ├── __init__.py
│       ├── file_service.py     # Manejo de archivos
│       └── pptx_service.py     # Lógica de python-pptx
├── uploads/
│   ├── templates/              # Templates subidos
│   └── images/                 # Imágenes temporales
├── outputs/                    # Presentaciones generadas
├── requirements.txt
└── README.md
```

## API Endpoints

### Health Check

#### GET `/`
Verifica el estado de la API.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Templates

#### POST `/api/v1/templates/upload`
Sube un template de PowerPoint.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (archivo .pptx)

**Response:**
```json
{
  "template_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "550e8400-e29b-41d4-a716-446655440000.pptx",
  "message": "Template uploaded successfully"
}
```

#### GET `/api/v1/templates/{template_id}/placeholders`
Obtiene todos los placeholders de un template.

**Response:**
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

#### DELETE `/api/v1/templates/{template_id}`
Elimina un template del servidor.

**Response:**
```json
{
  "success": true,
  "message": "Template '550e8400-e29b-41d4-a716-446655440000' deleted successfully"
}
```

### Presentaciones

#### POST `/api/v1/presentations/create`
Crea una nueva presentación desde un template.

**Request Body:**
```json
{
  "template_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response:**
```json
{
  "presentation_id": "660e8400-e29b-41d4-a716-446655440001",
  "template_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Presentation created successfully"
}
```

#### POST `/api/v1/presentations/{presentation_id}/text`
Inserta texto en un placeholder de la presentación.

**Request Body:**
```json
{
  "placeholder_name": "Title 1",
  "text": "Mi Título",
  "formatting": {
    "font_name": "Arial",
    "font_size": 36,
    "bold": true,
    "color": "#FF0000",
    "alignment": "CENTER"
  }
}
```

**Opciones de Formato:**
- `font_name`: Nombre de la fuente (ej: "Arial", "Calibri")
- `font_size`: Tamaño en puntos (1-400)
- `bold`: Texto en negrita (true/false)
- `italic`: Texto en cursiva (true/false)
- `underline`: Texto subrayado (true/false)
- `color`: Color en formato hexadecimal (ej: "#FF0000")
- `alignment`: Alineación horizontal ("LEFT", "CENTER", "RIGHT", "JUSTIFY", "DISTRIBUTE")
- `vertical_alignment`: Alineación vertical ("TOP", "MIDDLE", "BOTTOM")

**Response:**
```json
{
  "success": true,
  "message": "Text inserted successfully into placeholder 'Title 1'"
}
```

#### POST `/api/v1/presentations/{presentation_id}/image`
Inserta una imagen en un placeholder de la presentación.

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `placeholder_name`: El **Texto Alternativo** de la imagen a reemplazar
  - `image`: Archivo de imagen (PNG, JPG, JPEG, GIF, BMP, TIFF)

**Response:**
```json
{
  "success": true,
  "message": "Image inserted successfully into placeholder 'Picture Placeholder 2'"
}
```

**Nota:** La imagen se adapta automáticamente al tamaño del placeholder. Solo se pueden insertar imágenes en placeholders de tipo PICTURE.

#### GET `/api/v1/presentations/{presentation_id}/download`
Descarga la presentación generada.

**Response:**
- Content-Type: `application/vnd.openxmlformats-officedocument.presentationml.presentation`
- Body: Archivo .pptx

#### DELETE `/api/v1/presentations/{presentation_id}`
Elimina una presentación del servidor.

**Response:**
```json
{
  "success": true,
  "message": "Presentation '660e8400-e29b-41d4-a716-446655440001' deleted successfully"
}
```

## Ejemplo de Uso

### Flujo Completo con cURL

#### 1. Subir un Template
```bash
curl -X POST "http://localhost:8000/api/v1/templates/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@mi_template.pptx"
```

#### 2. Obtener Placeholders del Template
```bash
curl -X GET "http://localhost:8000/api/v1/templates/{template_id}/placeholders" \
  -H "accept: application/json"
```

#### 3. Crear una Presentación
```bash
curl -X POST "http://localhost:8000/api/v1/presentations/create" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "{template_id}"
  }'
```

#### 4. Insertar Texto
```bash
curl -X POST "http://localhost:8000/api/v1/presentations/{presentation_id}/text" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "placeholder_name": "Title 1",
    "text": "Mi Presentación",
    "formatting": {
      "font_size": 36,
      "bold": true,
      "alignment": "CENTER"
    }
  }'
```

#### 5. Insertar Imagen
```bash
curl -X POST "http://localhost:8000/api/v1/presentations/{presentation_id}/image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "placeholder_name=Picture Placeholder 2" \
  -F "image=@mi_imagen.png"
```

#### 6. Descargar la Presentación
```bash
curl -X GET "http://localhost:8000/api/v1/presentations/{presentation_id}/download" \
  -H "accept: application/vnd.openxmlformats-officedocument.presentationml.presentation" \
  --output presentacion_final.pptx
```

### Ejemplo con Python

```python
import requests

# Configuración
BASE_URL = "http://localhost:8000"

# 1. Subir template
with open("mi_template.pptx", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/v1/templates/upload",
        files={"file": f}
    )
template_id = response.json()["template_id"]

# 2. Obtener placeholders
response = requests.get(
    f"{BASE_URL}/api/v1/templates/{template_id}/placeholders"
)
placeholders = response.json()

# 3. Crear presentación
response = requests.post(
    f"{BASE_URL}/api/v1/presentations/create",
    json={"template_id": template_id}
)
presentation_id = response.json()["presentation_id"]

# 4. Insertar texto
response = requests.post(
    f"{BASE_URL}/api/v1/presentations/{presentation_id}/text",
    json={
        "placeholder_name": "Title 1",
        "text": "Mi Título",
        "formatting": {
            "font_size": 36,
            "bold": True,
            "alignment": "CENTER"
        }
    }
)

# 5. Insertar imagen
with open("mi_imagen.png", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/v1/presentations/{presentation_id}/image",
        data={"placeholder_name": "Picture Placeholder 2"},
        files={"image": f}
    )

# 6. Descargar presentación
response = requests.get(
    f"{BASE_URL}/api/v1/presentations/{presentation_id}/download"
)
with open("presentacion_final.pptx", "wb") as f:
    f.write(response.content)
```

## Tipos de Placeholders

La API soporta los siguientes tipos de placeholders:

- **TITLE**: Título de la diapositiva
- **BODY**: Cuerpo de texto
- **PICTURE**: Imagen (solo acepta imágenes)
- **CENTER_TITLE**: Título centrado
- **SUBTITLE**: Subtítulo
- **OBJECT**: Objeto genérico
- **CHART**: Gráfico
- **TABLE**: Tabla
- **DATE**: Fecha
- **SLIDE_NUMBER**: Número de diapositiva
- **FOOTER**: Pie de página
- **HEADER**: Encabezado

## Formatos de Imagen Soportados

- PNG
- JPG/JPEG
- GIF
- BMP
- TIFF

## Errores Comunes

### 400 Bad Request
- Archivo inválido (no es .pptx o formato de imagen incorrecto)
- Placeholder no encontrado
#### Error: "No image found with Alt Text 'X'"
 
 **Causa**: No se encontró ninguna imagen en la presentación cuyo Texto Alternativo coincida con `X`.
 
 **Solución**:
 - Abre el PowerPoint en tu PC.
 - Haz clic derecho en la imagen que quieres reemplazar -> "Ver Texto Alternativo".
 - Asegúrate de que el texto coincida exactamente con lo que envías a la API.
- Tipo de placeholder incorrecto (ej: intentar insertar texto en placeholder de imagen)

### 404 Not Found
- Template no encontrado
- Presentación no encontrada

### 500 Internal Server Error
- Error al procesar el archivo
- Error al guardar la presentación

## Desarrollo

### Ejecutar con recarga automática:
```bash
python -m uvicorn app.main:app --reload
```

### Ejecutar pruebas (cuando estén disponibles):
```bash
pytest
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para construir APIs
- **python-pptx**: Librería para crear y modificar presentaciones de PowerPoint
- **Pydantic**: Validación de datos usando anotaciones de tipo
- **Uvicorn**: Servidor ASGI de alta velocidad

## Licencia

Este proyecto está bajo la Licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request para cualquier mejora.

## Soporte

Para preguntas o problemas, por favor abre un issue en el repositorio.
