# Guía Detallada: Variables de Imagen con Alt Text

Para que la API pueda intercambiar imágenes correctamente, utilizamos el **Texto Alternativo (Alt Text)** de una imagen de referencia dentro de tu PowerPoint.

## 1. Lógica del Sistema

1.  Colocas una imagen de muestra en tu diapositiva.
2.  Le asignas un **Texto Alternativo** con el formato `{{nombre}}`.
3.  La API busca esa imagen por su Alt Text.
4.  Si la encuentra, la reemplaza por la imagen nueva, manteniendo posición y dimensiones.

## 2. Pasos para Configurar tu Template

### Paso 1: Insertar Imagen de Referencia

- Inserta una imagen cualquiera en tu diapositiva (`Insertar` -> `Imagen`).
- Ajusta su tamaño y posición exactamente como quieres que quede la imagen final.

### Paso 2: Asignar Alt Text

1.  Haz clic derecho sobre la imagen.
2.  Selecciona **Ver Texto Alternativo...** (View Alt Text) o **Editar Texto Alternativo**.
3.  Escribe tu variable entre llaves, por ejemplo: `{{foto_perfil}}`.
    - _Nota_: También soportamos el formato `{{image:foto_perfil}}` por si quieres ser más explícito.

## 3. Uso en la API

Al llamar al endpoint `/image`, usa el nombre que pusiste dentro de las llaves.

**Ejemplo:**

- **En PowerPoint (Alt Text)**: `{{logo_empresa}}`
- **En API (`variable_name`)**: `logo_empresa` (solo el nombre interno)

> [!TIP]
> Si envías `logo_empresa` a la API, ésta buscará tanto `{{logo_empresa}}` como `{{image:logo_empresa}}` en el PowerPoint.

## 4. Ventajas

- **Precisión**: La nueva imagen heredará el tamaño exacto de la de referencia, evitando que rompa tu diseño.
- **Simplicidad**: Cualquier imagen que pongas en el PPT puede convertirse en una variable en segundos.
