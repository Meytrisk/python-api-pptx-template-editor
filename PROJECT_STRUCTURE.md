# Estructura del Proyecto PPTX API

Este documento describe la estructura del proyecto y la arquitectura de la API PPTX.

## Estructura de Directorios

```
pptx/
├── app/                          # Directorio principal de la aplicación
│   ├── __init__.py              # Inicialización del paquete app
│   ├── main.py                  # Entry point de FastAPI
│   ├── api/                     # Módulo de API
│   │   ├── __init__.py          # Inicialización del paquete api
│   │   └── routes/             # Rutas de la API
│   │       ├── __init__.py      # Inicialización del paquete routes
│   │       ├── templates.py      # Endpoints para templates
│   │       └── presentations.py # Endpoints para presentaciones
│   ├── models/                  # Modelos de datos
│   │   ├── __init__.py         # Inicialización del paquete models
│   │   ├── schemas.py           # Modelos Pydantic para validación
│   │   └── enums.py            # Enumeraciones de la aplicación
│   └── services/               # Lógica de negocio
│       ├── __init__.py         # Inicialización del paquete services
│       ├── file_service.py      # Servicio de manejo de archivos
│       └── pptx_service.py    # Servicio de manipulación de PowerPoint
├── uploads/                     # Directorio de archivos subidos
│   ├── templates/              # Templates de PowerPoint
│   └── images/                 # Imágenes temporales
├── outputs/                     # Directorio de presentaciones generadas
├── Dockerfile                   # Configuración de Docker
├── docker-compose.yml           # Configuración de Docker Compose
├── requirements.txt             # Dependencias de Python
├── README.md                   # Documentación principal
├── API_DOCUMENTATION.md        # Documentación detallada de la API
├── PROJECT_STRUCTURE.md        # Este archivo
└── .gitignore                 # Archivos ignorados por Git
```

## Descripción de Componentes

### [`app/main.py`](app/main.py:1)

**Propósito**: Entry point de la aplicación FastAPI.

**Responsabilidades**:
- Inicializar la aplicación FastAPI
- Configurar middleware (CORS)
- Incluir routers de la API
- Definir endpoints de health check
- Manejo global de excepciones

**Componentes principales**:
```python
app = FastAPI(
    title="PPTX API",
    description="API for creating and modifying PowerPoint presentations",
    version="1.0.0"
)
```

### [`app/api/routes/templates.py`](app/api/routes/templates.py:1)

**Propósito**: Endpoints para el manejo de templates.

**Endpoints**:
- `POST /api/v1/templates/upload` - Subir template
- `GET /api/v1/templates/{template_id}/placeholders` - Obtener placeholders
- `DELETE /api/v1/templates/{template_id}` - Eliminar template

**Responsabilidades**:
- Validar archivos subidos
- Coordinar con FileService y PPTXService
- Manejar errores específicos de templates

### [`app/api/routes/presentations.py`](app/api/routes/presentations.py:1)

**Propósito**: Endpoints para el manejo de presentaciones.

**Endpoints**:
- `POST /api/v1/presentations/create` - Crear presentación
- `POST /api/v1/presentations/{presentation_id}/text` - Insertar texto
- `POST /api/v1/presentations/{presentation_id}/image` - Insertar imagen
- `GET /api/v1/presentations/{presentation_id}/download` - Descargar presentación
- `DELETE /api/v1/presentations/{presentation_id}` - Eliminar presentación

**Responsabilidades**:
- Validar requests de presentaciones
- Coordinar con FileService y PPTXService
- Manejar subida de imágenes
- Proveer descarga de archivos

### [`app/models/schemas.py`](app/models/schemas.py:1)

**Propósito**: Modelos Pydantic para validación de datos.

**Modelos principales**:
- `PlaceholderInfo` - Información de un placeholder
- `TemplatePlaceholders` - Placeholders de un template
- `TextInsertRequest` - Request para insertar texto
- `ImageInsertRequest` - Request para insertar imagen
- `TextFormatting` - Opciones de formato de texto
- `PresentationCreateRequest` - Request para crear presentación
- `TemplateUploadResponse` - Response de subida de template
- `PresentationCreateResponse` - Response de creación de presentación
- `ContentInsertResponse` - Response de inserción de contenido
- `ErrorResponse` - Response de error
- `HealthResponse` - Response de health check

**Responsabilidades**:
- Validar datos de entrada
- Definir estructura de respuestas
- Documentar campos y tipos de datos

### [`app/models/enums.py`](app/models/enums.py:1)

**Propósito**: Enumeraciones de la aplicación.

**Enumeraciones**:
- `PlaceholderType` - Tipos de placeholders (TITLE, BODY, PICTURE, etc.)
- `TextAlignment` - Alineaciones de texto (LEFT, CENTER, RIGHT, etc.)
- `VerticalAlignment` - Alineaciones verticales (TOP, MIDDLE, BOTTOM)

**Responsabilidades**:
- Definir valores constantes
- Proporcionar autocompletado en IDEs
- Validar valores enumerados

### [`app/services/file_service.py`](app/services/file_service.py:1)

**Propósito**: Servicio para manejo de archivos.

**Responsabilidades**:
- Crear y gestionar directorios
- Guardar archivos subidos (templates e imágenes)
- Generar IDs únicos
- Validar formatos de archivo
- Eliminar archivos
- Proporcionar rutas de archivos

**Métodos principales**:
```python
async def save_template(file: UploadFile) -> tuple[str, str]
async def save_image(file: UploadFile) -> tuple[str, str]
def get_template_path(template_id: str) -> Path
def get_image_path(image_id: str) -> Path
def create_presentation_path(presentation_id: str) -> Path
def get_presentation_path(presentation_id: str) -> Path
def delete_template(template_id: str) -> bool
def delete_presentation(presentation_id: str) -> bool
def cleanup_image(image_id: str) -> bool
```

### [`app/services/pptx_service.py`](app/services/pptx_service.py:1)

**Propósito**: Servicio para manipulación de PowerPoint usando python-pptx.

**Responsabilidades**:
- Cargar y analizar templates
- Extraer información de placeholders
- Crear presentaciones desde templates
- Insertar texto con formato
- Insertar imágenes en placeholders
- Aplicar formato de texto

**Métodos principales**:
```python
def get_template_placeholders(template_id: str) -> TemplatePlaceholders
def create_presentation(template_id: str, presentation_id: str) -> str
def insert_text(presentation_id: str, placeholder_name: str, text: str, formatting: Optional[TextFormatting]) -> bool
def insert_image(presentation_id: str, placeholder_name: str, image_path: str) -> bool
```

## Flujo de Datos

### 1. Subir Template

```
Cliente → POST /api/v1/templates/upload
    ↓
templates.py (route)
    ↓
FileService.save_template()
    ↓
Guardar en uploads/templates/
    ↓
Retornar template_id
```

### 2. Obtener Placeholders

```
Cliente → GET /api/v1/templates/{template_id}/placeholders
    ↓
templates.py (route)
    ↓
PPTXService.get_template_placeholders()
    ↓
FileService.get_template_path()
    ↓
python-pptx: Cargar presentación
    ↓
python-pptx: Extraer placeholders
    ↓
Retornar TemplatePlaceholders
```

### 3. Crear Presentación

```
Cliente → POST /api/v1/presentations/create
    ↓
presentations.py (route)
    ↓
FileService.generate_id()
    ↓
PPTXService.create_presentation()
    ↓
FileService.get_template_path()
    ↓
python-pptx: Cargar template
    ↓
python-pptx: Guardar como nueva presentación
    ↓
Retornar presentation_id
```

### 4. Insertar Texto

```
Cliente → POST /api/v1/presentations/{presentation_id}/text
    ↓
presentations.py (route)
    ↓
PPTXService.insert_text()
    ↓
FileService.get_presentation_path()
    ↓
python-pptx: Cargar presentación
    ↓
python-pptx: Encontrar placeholder
    ↓
python-pptx: Insertar texto
    ↓
python-pptx: Aplicar formato (si se proporciona)
    ↓
python-pptx: Guardar presentación
    ↓
Retornar success
```

### 5. Insertar Imagen

```
Cliente → POST /api/v1/presentations/{presentation_id}/image
    ↓
presentations.py (route)
    ↓
FileService.save_image()
    ↓
Guardar en uploads/images/
    ↓
PPTXService.insert_image()
    ↓
FileService.get_presentation_path()
    ↓
FileService.get_image_path()
    ↓
python-pptx: Cargar presentación
    ↓
python-pptx: Encontrar imagen por Alt Text
    ↓
python-pptx: Reemplazar imagen (manteniendo posición y tamaño)
    ↓
python-pptx: Guardar presentación
    ↓
FileService.cleanup_image()
    ↓
Retornar success
```

### 6. Descargar Presentación

```
Cliente → GET /api/v1/presentations/{presentation_id}/download
    ↓
presentations.py (route)
    ↓
FileService.get_presentation_path()
    ↓
Retornar archivo .pptx
```

## Arquitectura en Capas

```
┌─────────────────────────────────────┐
│         Capa de Presentación       │
│  (FastAPI Routes - api/routes/)   │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│          Capa de Servicios         │
│  (Business Logic - services/)      │
│  - FileService                   │
│  - PPTXService                  │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│         Capa de Datos             │
│  (File System & python-pptx)      │
│  - uploads/                      │
│  - outputs/                      │
│  - python-pptx library          │
└─────────────────────────────────────┘
```

## Patrones de Diseño Utilizados

### 1. Separación de Responsabilidades (Separation of Concerns)

Cada componente tiene una responsabilidad clara:
- **Routes**: Manejo de HTTP requests/responses
- **Services**: Lógica de negocio
- **Models**: Validación de datos

### 2. Inyección de Dependencias

Los servicios reciben dependencias a través del constructor:
```python
class PPTXService:
    def __init__(self, file_service: FileService):
        self.file_service = file_service
```

### 3. Repository Pattern

FileService actúa como un repository para operaciones de archivos:
```python
file_service.get_template_path(template_id)
file_service.save_template(file)
```

### 4. DTO Pattern (Data Transfer Objects)

Los modelos Pydantic actúan como DTOs para transferir datos entre capas:
```python
class TextInsertRequest(BaseModel):
    placeholder_name: str
    text: str
    formatting: Optional[TextFormatting]
```

## Manejo de Errores

### Tipos de Errores

1. **HTTPException** - Errores HTTP estándar
   - 400 Bad Request - Datos inválidos
   - 404 Not Found - Recurso no encontrado
   - 500 Internal Server Error - Error del servidor

2. **Exception** - Errores generales
   - Capturados por el manejador global
   - Convertidos a HTTP 500

### Estrategia de Manejo

```python
try:
    # Operación
    result = service.do_something()
except HTTPException:
    raise  # Re-lanzar excepciones HTTP
except Exception as e:
    # Convertir a HTTP 500
    raise HTTPException(status_code=500, detail=str(e))
```

## Consideraciones de Escalabilidad

### Mejoras Futuras

1. **Base de Datos**
   - Actualmente: Sistema de archivos
   - Futuro: PostgreSQL/MongoDB para metadatos

2. **Almacenamiento en la Nube**
   - Actualmente: Sistema de archivos local
   - Futuro: AWS S3, Google Cloud Storage

3. **Colas de Tareas**
   - Actualmente: Procesamiento síncrono
   - Futuro: Celery/Redis para tareas asíncronas

4. **Caching**
   - Actualmente: Sin caché
   - Futuro: Redis para caché de templates

5. **Autenticación y Autorización**
   - Actualmente: Sin autenticación
   - Futuro: JWT, OAuth2

6. **Rate Limiting**
   - Actualmente: Sin límites
   - Futuro: slowapi, fastapi-limiter

7. **Logging y Monitoreo**
   - Actualmente: Logs básicos
   - Futuro: ELK Stack, Prometheus, Grafana

## Seguridad

### Consideraciones Actuales

1. **Validación de Archivos**
   - Verificación de extensiones
   - Validación de tipos MIME

2. **CORS**
   - Configurado para permitir todos los orígenes (desarrollo)
   - Debe restringirse en producción

3. **Sanitización de Entradas**
   - Validación con Pydantic
   - Tipos de datos estrictos

### Mejoras de Seguridad Recomendadas

1. **Autenticación**
   - Implementar JWT tokens
   - API keys para integraciones

2. **Autorización**
   - Roles y permisos
   - Aislamiento de usuarios

3. **Rate Limiting**
   - Prevenir abuso de la API
   - Limitar tamaño de archivos

4. **HTTPS**
   - Forzar conexiones seguras
   - Certificados SSL/TLS

5. **Input Sanitization**
   - Validar contenido de archivos
   - Prevenir inyección de código

## Testing

### Estrategia de Testing Recomendada

1. **Unit Tests**
   - Testear servicios individualmente
   - Mock de dependencias externas

2. **Integration Tests**
   - Testear endpoints completos
   - Usar TestClient de FastAPI

3. **End-to-End Tests**
   - Flujos completos de usuario
   - Pruebas con archivos reales

### Herramientas Sugeridas

- **pytest** - Framework de testing
- **pytest-asyncio** - Soporte para async
- **httpx** - Cliente HTTP asíncrono
- **pytest-cov** - Cobertura de código

## Contribución

### Guía de Estilo

- Seguir PEP 8
- Usar type hints
- Documentar funciones con docstrings
- Mantener funciones pequeñas y enfocadas

### Flujo de Trabajo

1. Crear branch desde `main`
2. Implementar cambios
3. Escribir tests
4. Actualizar documentación
5. Crear pull request

## Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [python-pptx Documentation](https://python-pptx.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Docker Documentation](https://docs.docker.com/)
