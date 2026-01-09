# Guía de Despliegue por Repositorio (PAAS)

Esta guía te ayudará a desplegar la PPTX API en plataformas como **Dokploy, Coolify, Easypanel, CapRover** o similares, conectando directamente tu repositorio de GitHub/GitLab.

## 1. Conexión del Repositorio
1.  En tu panel de PAAS, crea una nueva aplicación.
2.  Selecciona **GitHub** (o tu proveedor) y elige este repositorio.
3.  La plataforma detectará automáticamente el `Dockerfile`.

## 2. Configuración de Variables de Entorno (Opcional)
Puedes configurar las siguientes variables en el panel de tu PAAS:

| Variable | Descripción | Valor por Defecto |
| :--- | :--- | :--- |
| `CORS_ORIGINS` | Dominios permitidos (separados por coma) | `*` |
| `API_TITLE` | Título de tu instancia de la API | `PPTX API` |

> [!IMPORTANT]
> Si deseas restringir el acceso, configura `CORS_ORIGINS` con la URL de tu frontend (ej: `https://mi-app.com`).

## 3. Configuración de Almacenamiento (VITAL)
Para que no pierdas tus plantillas ni las presentaciones generadas al reiniciar el servidor o actualizar el código, **DEBES** configurar volúmenes persistentes.

En el panel de tu PAAS (Sección Storage/Volumes), crea dos volúmenes:

1.  **Volumen de Subidas**:
    *   **Ruta en el contenedor**: `/app/uploads`
2.  **Volumen de Salidas**:
    *   **Ruta en el contenedor**: `/app/outputs`

## 4. Puerto
*   La aplicación corre en el puerto **8000**.
*   Asegúrate de mapear el dominio/puerto público al puerto 8000 del contenedor.

## 5. Health Check
Si tu plataforma pide una URL de salud para saber si la app está lista:
*   **Path**: `/health`
*   **Puerto**: `8000`
