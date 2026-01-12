# Estructura del Proyecto PPTX API (Sistema de Variables)

Este documento describe la arquitectura y el flujo de datos del sistema de automatización basado en variables descriptivas.

## Estructura de Directorios

```
pptx/
├── app/                          # Directorio principal de la aplicación
│   ├── main.py                  # Entry point de FastAPI
│   ├── api/                     # Módulo de API
│   │   └── routes/             # Rutas (templates.py, presentations.py)
│   ├── models/                  # Modelos de datos
│   │   ├── schemas.py           # Modelos Pydantic (VariableInfo, etc.)
│   │   └── enums.py            # Enumeraciones (TextAlignment)
│   └── services/               # Lógica de negocio
│       ├── file_service.py      # Servicio de archivos
│       └── pptx_service.py    # Lógica de reemplazo de variables {{}}
├── uploads/                     # Directorio de archivos subidos
├── outputs/                     # Directorio de archivos generados
├── Dockerfile                   # Configuración de Docker
└── docker-compose.yml           # Configuración de Docker Compose
```

## Componentes Clave

### [`app/services/pptx_service.py`](app/services/pptx_service.py)

Es el núcleo de la aplicación. Implementa:

- **Escaner de Variables**: Detecta patrones `{{variable}}` en todo el documento.
- **Reemplazo Global**: Busca y reemplaza todas las instancias de una variable en todas las diapositivas.
- **Reemplazo Geométrico**: Intercambia imágenes manteniendo las dimensiones del placeholder original.

### [`app/models/schemas.py`](app/models/schemas.py)

Define la interfaz de la API. Se eliminaron los modelos de "Placeholders" tradicionales en favor de `VariableInfo`.

## Flujo de Datos

### 1. Escaneo de Variables

```
Cliente → GET /api/v1/templates/{id}/variables
    ↓
PPTXService.get_template_variables()
    ↓
Escaneo de:
 - TextFrames: Expresiones regulares para {{var}}
 - Alt Text: Expresiones regulares para {{var}} o {{image:var}}
    ↓
Retornar lista de variables detectadas
```

### 2. Reemplazo de Texto

```
Cliente → POST /api/v1/presentations/{id}/text
    ↓
PPTXService.insert_text()
    ↓
Búsqueda global de la cadena "{{variable_name}}"
    ↓
Reemplazo en cada párrafo para preservar formato
    ↓
Guardar presentación
```

### 3. Reemplazo de Imagen

```
Cliente → POST /api/v1/presentations/{id}/image
    ↓
PPTXService.insert_image()
    ↓
Búsqueda de forma por Alt Text == "{{var}}" o "{{image:var}}"
    ↓
Captura de (Left, Top, Width, Height)
    ↓
Inserción de nueva imagen + Eliminación de original
    ↓
Guardar presentación
```

## Ventajas de esta Arquitectura

- **Desacoplamiento**: El diseño del PowerPoint es independiente de la lógica de la API.
- **Simplicidad**: El usuario final solo necesita saber escribir entre llaves.
- **Escalabilidad**: Fácil de extender para soportar tablas u otros objetos mediante el mismo sistema de identificación.
