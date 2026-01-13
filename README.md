# PPTX API (Variable System)

API REST profesional para la automatización de presentaciones de PowerPoint. Olvídate de los complejos "Placeholders" y el "Slide Master". Diseña tu presentación de forma natural y usa variables `{{como_esta}}` para inyectar contenido.

## 🚀 Documentación

- [Documentación Detallada de la API](API_DOCUMENTATION.md)
- [Guía de Creación de Templates](TEMPLATE_GUIDE.md)
- [Guía de Imágenes (Alt Text)](IMAGE_GUIDE.md)
- [Guía de Despliegue (PAAS)](DEPLOY.md)

## ✨ Características Principales

- **Variables Globales**: Usa `{{variable}}` en cualquier cuadro de texto. Se reemplazan todas las ocurrencias en todo el documento automáticamente.
- **Imágenes vía Alt Text**: Reemplaza imágenes manteniendo posición y tamaño usando `{{variable}}` en el Texto Alternativo.
- **Escaneo de Variables**: La API analiza tu archivo y te dice qué variables encontró.
- **Formato Dinámico**: Cambia fuente, color, tamaño y alineación al insertar texto.
- **Persistencia**: Diseñado para funcionar en la nube con volúmenes persistentes.
- **Docker-Ready**: Incluye Dockerfile y Docker Compose optimizados.

## 🛠️ Instalación y Uso

### Local

1. Instalar dependencias: `pip install -r requirements.txt`
2. Ejecutar: `python app/main.py`
3. Swagger UI: `http://localhost:8000/docs`

```bash
docker-compose up -d
```

## 🛡️ Control de Calidad (Antes de hacer Push)

Para evitar que errores de sintaxis o importaciones falten lleguen a producción, puedes ejecutar:

1. **Verificación rápida de importaciones**:
   ```bash
   python scripts/verify_build.py
   ```
2. **Prueba de construcción Docker**:
   ```bash
   docker build -t pptx-test .
   ```

## 💪 Robustez y Rendimiento

La API ha sido sometida a pruebas de estrés con **50 usuarios concurrentes**, demostrando una estabilidad del **100% (cero fallos)** bajo carga intensa:

| Operación            | Rendimiento | Latencia Media |
| :------------------- | :---------- | :------------- |
| **Lectura (Listar)** | ~240 req/s  | 200ms          |
| **Creación PPTX**    | ~120 req/s  | 410ms          |
| **Inyección Texto**  | ~75 req/s   | 650ms          |
| **Inyección Imagen** | ~55 req/s   | 850ms          |

_Pruebas realizadas utilizando el script `scripts/stress_test.py`._

## 📝 Ejemplo Rápido de Flujo

1. **Subir Template**: Envía tu `.pptx` con `{{nombre}}` y obtén un `template_id`.
2. **Crear Instancia**: Crea una nueva presentación a partir de ese template.
3. **Inyectar Datos**:
   - `POST /text` -> `variable_name: "nombre"`, `text: "Juan Pérez"`
   - `POST /image` -> `variable_name: "foto"`, `image: [archivo]`
4. **Descargar**: Obtén tu archivo terminado.

---

Meytrisk © 2026 - Herramienta de automatización PPTX
