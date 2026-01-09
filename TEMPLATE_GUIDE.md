# Guía de Creación de Templates con Placeholders

Esta guía explica cómo crear templates de PowerPoint con placeholders para usar con la API PPTX.

## Tabla de Contenidos

- [¿Qué son los Placeholders?](#qué-son-los-placeholders)
- [Tipos de Placeholders Disponibles](#tipos-de-placeholders-disponibles)
- [Cómo Crear un Template con Placeholders](#cómo-crear-un-template-con-placeholders)
- [Ejemplos de Templates](#ejemplos-de-templates)
- [Verificar Placeholders en un Template](#verificar-placeholders-en-un-template)
- [Mejores Prácticas](#mejores-prácticas)
- [Solución de Problemas Comunes](#solución-de-problemas-comunes)

---

## ¿Qué son los Placeholders?

Los **placeholders** (marcadores de posición) son elementos predefinidos en una diapositiva de PowerPoint que indican dónde se debe insertar contenido específico como texto, imágenes, tablas, etc.

### Características de los Placeholders

- ✅ Tienen un **nombre único** (`name`) que los identifica (¡Este es el que usa la API!)
- ✅ Tienen un **índice único** (`idx`) (Usado internamente por PowerPoint)
- ✅ Tienen un **tipo** que define qué contenido pueden aceptar
- ✅ Tienen una **posición y tamaño** predefinidos
- ✅ Pueden tener **formato predeterminado** (fuente, color, etc.)
- ✅ La API puede **leer y modificar** su contenido

### Por qué usar Placeholders

- **Consistencia**: Mantienen el diseño uniforme en todas las presentaciones
- **Flexibilidad**: Permiten insertar contenido dinámico sin modificar el diseño
- **Eficiencia**: Automatizan la creación de presentaciones
- **Control**: Definen exactamente dónde y cómo se muestra el contenido

---

## Tipos de Placeholders Disponibles

La API PPTX soporta los siguientes tipos de placeholders:

| Tipo | Descripción | Acepta Texto | Acepta Imágenes | Uso Típico |
|------|-------------|---------------|-----------------|--------------|
| **TITLE** | Título de la diapositiva | ✅ | ❌ | Título principal de la diapositiva |
| **BODY** | Cuerpo de texto | ✅ | ❌ | Párrafos, listas, contenido extenso |
| **PICTURE** | Imagen (Reemplazo) | ❌ | ✅ | Usar Alt Text `{{nombre}}` en una imagen normal |
| **CENTER_TITLE** | Título centrado | ✅ | ❌ | Títulos de portada |
| **SUBTITLE** | Subtítulo | ✅ | ❌ | Subtítulos, descripciones cortas |
| **OBJECT** | Objeto genérico | ✅ | ❌ | Contenido variado |
| **CHART** | Gráfico | ✅ | ❌ | Gráficos de datos |
| **TABLE** | Tabla | ✅ | ❌ | Datos tabulares |
| **DATE** | Fecha | ✅ | ❌ | Fecha de presentación |
| **SLIDE_NUMBER** | Número de diapositiva | ✅ | ❌ | Numeración de páginas |
| **FOOTER** | Pie de página | ✅ | ❌ | Información adicional al pie |
| **HEADER** | Encabezado | ✅ | ❌ | Información en el encabezado |

---

## Cómo Crear un Template con Placeholders

### Método 1: Usar Layouts Predefinidos de PowerPoint

PowerPoint incluye layouts predefinidos con placeholders listos para usar.

#### Pasos:

1. **Abrir PowerPoint**
   - Inicia Microsoft PowerPoint
   - Crea una nueva presentación

2. **Seleccionar un Layout**
   - Ve a la pestaña **Inicio**
   - Haz clic en **Diseño de diapositiva** (Slide Layout)
   - Elige un layout que tenga los placeholders que necesitas

3. **Layouts Comunes y sus Placeholders**

   **a) Título y Contenido (Title and Content)**
   ```
   Placeholders típicos:
   - idx 0: TITLE (Título)
   - idx 1: BODY (Contenido)
   ```

   **b) Título y Dos Contenidos (Title and Two Content)**
   ```
   Placeholders típicos:
   - idx 0: TITLE (Título)
   - idx 1: BODY (Contenido izquierdo)
   - idx 2: BODY (Contenido derecho)
   ```

   **c) Título, Contenido y Texto (Title, Content, and Text)**
   ```
   Placeholders típicos:
   - idx 0: TITLE (Título)
   - idx 1: BODY (Contenido principal)
   - idx 2: BODY (Texto lateral)
   ```

   **d) Título y Subtítulo (Title and Subtitle)**
   ```
   Placeholders típicos:
   - idx 0: TITLE (Título)
   - idx 1: SUBTITLE (Subtítulo)
   ```

4. **Personalizar el Layout**
   - Puedes cambiar el tamaño y posición de los placeholders
   - Puedes cambiar el formato predeterminado (fuente, color, etc.)
   - Puedes agregar o eliminar placeholders

5. **Guardar como Template**
   - Ve a **Archivo** > **Guardar como**
   - Selecciona **Plantilla de PowerPoint (*.potx)**
   - O guarda como **Presentación de PowerPoint (*.pptx)** para usar directamente

### Método 2: Crear un Slide Master Personalizado

Para mayor control, puedes crear un Slide Master con placeholders personalizados.

#### Pasos:

1. **Abrir el Slide Master**
   - Ve a la pestaña **Vista**
   - Haz clic en **Slide Master**

2. **Agregar Placeholders**
   - En la pestaña **Slide Master**, haz clic en **Insertar Placeholder**
   - Selecciona el tipo de placeholder que necesitas:
     - Título (Title)
     - Contenido (Content)
     - Texto (Text)
     - Imagen (Picture)
     - Gráfico (Chart)
     - Tabla (Table)
     - Etc.

3. **Posicionar y Dar Formato a los Placeholders**
   - Arrastra los placeholders a la posición deseada
   - Cambia el tamaño según necesites
   - Aplica formato predeterminado (fuente, color, alineación)

4. **Crear Layouts Personalizados**
   - En el panel izquierdo, haz clic derecho en el Slide Master
   - Selecciona **Insertar diseño de diapositiva**
   - Agrega los placeholders que necesites a este layout

5. **Cerrar el Slide Master**
   - Ve a la pestaña **Slide Master**
   - Haz clic en **Cerrar vista maestra**

6. **Guardar como Template**
   - Ve a **Archivo** > **Guardar como**
   - Selecciona **Plantilla de PowerPoint (*.potx)**

### Método 3: Usar python-pptx para Crear Templates

También puedes crear templates programáticamente usando python-pptx.

#### Ejemplo: Crear un Template Básico

```python
from pptx import Presentation
from pptx.util import Inches, Pt

# Crear una nueva presentación
prs = Presentation()

# Agregar una diapositiva con layout de título
slide_layout = prs.slide_layouts[0]  # Title slide
slide = prs.slides.add_slide(slide_layout)

# Los placeholders ya están creados por el layout
# Puedes acceder a ellos para verificar
for placeholder in slide.placeholders:
    print(f"idx: {placeholder.idx}, name: {placeholder.name}, type: {placeholder.placeholder_format.type}")

# Guardar como template
prs.save('mi_template.pptx')
```

#### Ejemplo: Crear un Template con Placeholders Personalizados

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.shapes import MSO_SHAPE

# Crear una nueva presentación
prs = Presentation()

# Agregar una diapositiva en blanco
blank_slide_layout = prs.slide_layouts[6]
slide = prs.slides.add_slide(blank_slide_layout)

# Agregar un placeholder de título
# Nota: python-pptx no permite crear placeholders directamente
# Debes usar layouts predefinidos o crear el template en PowerPoint

# Guardar como template
prs.save('template_basico.pptx')
```

**Nota**: Para crear placeholders personalizados, es más fácil usar PowerPoint directamente y luego subir el template a la API.

---

## Ejemplos de Templates

### Ejemplo 1: Template de Portada

**Estructura:**
```
Diapositiva 1 (Portada)
├── Placeholder idx 0: TITLE (Título principal)
└── Placeholder idx 1: SUBTITLE (Subtítulo)
```

**Uso:**
- Insertar el título de la presentación en `idx 0`
- Insertar el subtítulo o descripción en `idx 1`

**Código de ejemplo:**
```python
import requests

# Crear presentación
response = requests.post(
    "http://localhost:8000/api/v1/presentations/create",
    json={"template_id": "template_portada_id"}
)
presentation_id = response.json()["presentation_id"]

# Insertar título
requests.post(
    f"http://localhost:8000/api/v1/presentations/{presentation_id}/text",
    json={
        "placeholder_name": "Title 1",
        "text": "Mi Presentación Anual 2024",
        "formatting": {
            "font_size": 44,
            "bold": True,
            "alignment": "CENTER",
            "color": "#2E86AB"
        }
    }
)

# Insertar subtítulo
requests.post(
    f"http://localhost:8000/api/v1/presentations/{presentation_id}/text",
    json={
        "placeholder_name": "Subtitle 2",
        "text": "Reporte de resultados y proyecciones",
        "formatting": {
            "font_size": 24,
            "alignment": "CENTER",
            "color": "#565656"
        }
    }
)
```

### Ejemplo 2: Template de Contenido con Imagen

**Estructura:**
```
Diapositiva 1 (Contenido con imagen)
├── Placeholder idx 0: TITLE (Título)
├── Placeholder idx 1: BODY (Texto descriptivo)
└── Placeholder idx 2: PICTURE (Imagen)
```

**Uso:**
- Insertar el título en `idx 0`
- Insertar el texto descriptivo en `idx 1`
- Insertar una imagen en la diapositiva y asignarle Alt Text `{{imagen_producto}}`

**Código de ejemplo:**
```python
import requests

# Crear presentación
response = requests.post(
    "http://localhost:8000/api/v1/presentations/create",
    json={"template_id": "template_contenido_id"}
)
presentation_id = response.json()["presentation_id"]

# Insertar título
requests.post(
    f"http://localhost:8000/api/v1/presentations/{presentation_id}/text",
    json={
        "placeholder_name": "Title 1",
        "text": "Análisis de Ventas",
        "formatting": {
            "font_size": 36,
            "bold": True,
            "color": "#2E86AB"
        }
    }
)

# Insertar texto
requests.post(
    f"http://localhost:8000/api/v1/presentations/{presentation_id}/text",
    json={
        "placeholder_name": "Content Placeholder 2",
        "text": "Las ventas han aumentado un 25% respecto al trimestre anterior. Este crecimiento se debe principalmente a la expansión en nuevos mercados.",
        "formatting": {
            "font_size": 18,
            "alignment": "LEFT"
        }
    }
)

# Insertar imagen
with open("grafico_ventas.png", "rb") as f:
    requests.post(
        f"http://localhost:8000/api/v1/presentations/{presentation_id}/image",
        data={"placeholder_name": "{{imagen_producto}}"},
        files={"image": f}
    )
```

### Ejemplo 3: Template de Múltiples Diapositivas

**Estructura:**
```
Diapositiva 1 (Portada)
├── Placeholder idx 0: TITLE
└── Placeholder idx 1: SUBTITLE

Diapositiva 2 (Contenido)
├── Placeholder idx 0: TITLE
└── Placeholder idx 1: BODY

Diapositiva 3 (Imagen)
├── Placeholder idx 0: TITLE
└── Placeholder idx 1: PICTURE
```

**Uso:**
- Cada diapositiva tiene sus propios placeholders
- Los índices se reinician en cada diapositiva
- Debes especificar el `slide_index` al insertar contenido

**Nota**: Los placeholders se identifican por su **nombre** (ej: "Title 1"). Si tu template tiene varias diapositivas, la API actual insertará el contenido en el primer placeholder que encuentre con ese nombre.

---

## Verificar Placeholders en un Template

### Usando la API

La forma más fácil de verificar los placeholders de un template es usando la API:

```bash
# Subir el template
curl -X POST "http://localhost:8000/api/v1/templates/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@mi_template.pptx"

# Obtener los placeholders
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
          "name": "Content Placeholder 2",
          "type": "BODY",
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

### Usando PowerPoint

También puedes verificar los placeholders directamente en PowerPoint:

1. **Abrir el template en PowerPoint**
2. **Ir a la vista Slide Master**
   - Pestaña **Vista** > **Slide Master**
3. **Seleccionar el layout**
4. **Ver los placeholders**
   - Los placeholders aparecen como cajas con etiquetas como "Título", "Contenido", etc.
   - Puedes hacer clic en ellos para ver sus propiedades

### Usando python-pptx

```python
from pptx import Presentation

# Cargar el template
prs = Presentation('mi_template.pptx')

# Iterar sobre las diapositivas
for slide_idx, slide in enumerate(prs.slides):
    print(f"\nDiapositiva {slide_idx}:")
    
    # Iterar sobre los placeholders
    for placeholder in slide.placeholders:
        print(f"  idx: {placeholder.idx}")
        print(f"  name: {placeholder.name}")
        print(f"  type: {placeholder.placeholder_format.type}")
        print(f"  position: left={placeholder.left}, top={placeholder.top}")
        print(f"  size: width={placeholder.width}, height={placeholder.height}")
```

---

## Mejores Prácticas

### 1. Diseño de Placeholders

✅ **Hacer:**
- Usar tamaños de placeholder apropiados para el contenido
- Mantener suficiente espacio entre placeholders
- Usar nombres descriptivos para los placeholders
- Considerar la relación de aspecto para imágenes
- Probar el template con contenido de ejemplo

❌ **No hacer:**
- Crear placeholders demasiado pequeños
- Superponer placeholders
- Usar demasiados placeholders en una diapositiva
- Ignorar la relación de aspecto de las imágenes

### 2. Formato Predeterminado

✅ **Hacer:**
- Definir fuentes, tamaños y colores predeterminados
- Usar fuentes estándar (Arial, Calibri, etc.)
- Mantener consistencia en el formato
- Considerar la legibilidad

❌ **No hacer:**
- Usar fuentes poco comunes
- Definir tamaños de fuente extremos
- Usar colores con poco contraste

### 3. Organización de Templates

✅ **Hacer:**
- Crear templates para diferentes propósitos (portada, contenido, etc.)
- Documentar el propósito de cada template
- Mantener una biblioteca de templates reutilizables
- Versionar los templates

❌ **No hacer:**
- Crear un solo template para todo
- No documentar el uso de los templates
- Modificar templates en producción sin pruebas

### 4. Pruebas

✅ **Hacer:**
- Probar el template con la API antes de usarlo en producción
- Verificar que todos los placeholders funcionan correctamente
- Probar con diferentes tipos de contenido
- Validar el resultado final

❌ **No hacer:**
- Asumir que el template funcionará sin pruebas
- Usar templates sin verificar los placeholders

---

## Solución de Problemas Comunes

### Problema 1: No puedo insertar texto en un placeholder

**Causa posible**: El placeholder es de tipo PICTURE.

**Solución**: 
- Verifica el tipo de placeholder usando la API
- Usa un placeholder de tipo TITLE, BODY, u otro que acepte texto
- Si necesitas insertar texto donde hay una imagen, usa un placeholder de texto

### Problema 2: No puedo insertar una imagen
 
 **Causa posible**: El Alt Text no coincide o no se encuentra.
 
 **Solución**:
 - Verifica que la imagen en PowerPoint tenga el Texto Alternativo correcto.
 - Recuerda que para imágenes ya NO se usan placeholders del Slide Master.

### Problema 3: La imagen se ve distorsionada

**Causa posible**: La relación de aspecto de la imagen no coincide con el placeholder.

**Solución**:
- Ajusta el tamaño del placeholder para que coincida con la relación de aspecto de la imagen
- O redimensiona la imagen antes de subirla
- La API recorta la imagen para llenar el placeholder, lo que puede causar distorsión

### Problema 4: El texto no se ve bien

**Causa posible**: El formato predeterminado del placeholder no es apropiado.

**Solución**:
- Usa el parámetro `formatting` al insertar texto
- Ajusta el tamaño de fuente, color, alineación, etc.
- O modifica el template para tener un mejor formato predeterminado

### Problema 5: No encuentro los placeholders en mi template

**Causa posible**: El template no tiene placeholders o usa cajas de texto normales.

**Solución**:
- Verifica que estás usando un layout con placeholders
- En PowerPoint, los placeholders tienen etiquetas como "Título", "Contenido", etc.
- Las cajas de texto normales NO son placeholders
- Crea un nuevo template usando layouts predefinidos

### Problema 6: No sé qué nombres de placeholder usar

**Solución**:
- Siempre verifica los nombres usando la API antes de intentar insertar contenido
- Usa `GET /api/v1/templates/{template_id}/placeholders` para ver el campo `"name"` de cada objeto
- No asumas que el nombre será simplemente "Title" o "Image"
- Documenta los nombres de cada template para facilitar su uso posterior

---

## Recursos Adicionales

- [Documentación de python-pptx](https://python-pptx.readthedocs.io/)
- [Documentación de la API PPTX](API_DOCUMENTATION.md)
- [Estructura del Proyecto](PROJECT_STRUCTURE.md)
- [README Principal](README.md)

---

## Soporte

Si tienes problemas creando templates o usando la API, por favor:
1. Revisa esta guía
2. Consulta la documentación de la API
3. Abre un issue en el repositorio del proyecto
