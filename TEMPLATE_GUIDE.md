# Guía de Creación de Templates con Variables `{{}}`

Esta guía explica cómo diseñar presentaciones de PowerPoint que sirvan como plantillas para la API PPTX utilizando el sistema de variables descriptivas.

## 🚀 Concepto Principal

Ya no necesitas usar la "Vista Maestra" o "Placeholders" complejos. Ahora cualquier elemento de tu diapositiva puede ser una variable si usas la sintaxis de llaves dobles: `{{nombre_variable}}`.

---

## 1. Variables de Texto

Para crear una variable de texto, simplemente inserta un cuadro de texto normal y escribe el nombre entre llaves.

### Ejemplos:

- **Variable Simple**: `{{cliente}}`
- **Varias variables en un cuadro**: `Hola {{nombre}}, tu saldo es {{monto}}.`
- **Variables repetidas**: Puedes poner `{{pagina_actual}}` en todas las diapositivas y la API las actualizará todas al mismo tiempo.

### Ventajas:

- Mantienes el formato (fuente, color, tamaño) que definas en PowerPoint.
- Puedes mezclar texto fijo con variables.
- No hay restricciones de ubicación.

---

## 2. Variables de Imagen

Para las imágenes, utilizamos el campo **Texto Alternativo** (Alt Text) de PowerPoint.

### Pasos:

1. Inserta cualquier imagen en tu diapositiva (será tu imagen de referencia/posición).
2. Haz clic derecho sobre la imagen y selecciona **Editar Texto Alternativo** (Edit Alt Text).
3. En el cuadro que aparece, escribe la variable: `{{foto_perfil}}` o `{{image:logo}}`.
4. Cierra el panel y guarda tu archivo.

### Comportamiento:

- La API reemplazará esta imagen por la que envíes.
- La nueva imagen mantendrá **exactamente la misma posición y tamaño** que la imagen original de referencia.

---

## 3. Cómo verificar las variables de tu Template

Una vez que tengas tu archivo `.pptx` listo:

1. Súbelo usando el endpoint `/api/v1/templates/upload`.
2. Llama a `/api/v1/templates/{id}/variables`.

La API te devolverá un listado como este:

```json
{
  "variables": [
    { "name": "usuario", "type": "text", "slide_index": 0 },
    { "name": "logo", "type": "image", "slide_index": 0 }
  ]
}
```

---

## 4. Mejores Prácticas

1. **Nombres Claros**: Usa nombres descriptivos como `{{fecha_vencimiento}}` en lugar de `{{var1}}`.
2. **Imágenes de Referencia**: Usa imágenes con la misma relación de aspecto (proporción) que las que esperas insertar para evitar que se estiren de forma extraña.
3. **Evita superposiciones**: Asegúrate de que tus cuadros de texto tengan espacio suficiente para crecer si el contenido reemplazado es más largo que la variable.
4. **Fuentes Estándar**: Si la API corre en un servidor Linux/Docker, usa fuentes comunes (Arial, Calibri) o asegúrate de que las fuentes personalizadas estén instaladas en el contenedor.
