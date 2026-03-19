# Contexto del Proyecto: Generador de Minutas IA

Este proyecto consiste en una aplicación de Python (Streamlit) integrada con flujos de trabajo en n8n para la generación automatizada de minutas de reunión a partir de documentos en Google Drive.

## Arquitectura Actual
- **Frontend**: Streamlit (Python) corriendo en Docker (`frontend_ui`).
- **Backend Automático**: n8n corriendo en Docker (`n8n`).
- **IA**: Groq (LLMa 3.x) configurada en n8n mediante LangChain.
- **Entorno**: Docker Compose gestionando ambos servicios.

## Componentes Clave
- `frontend_ui/app.py`: Interfaz de usuario para pegar URLs de Drive y descargar minutas.
- `n8n_data/`: Almacenamiento persistente de configuraciones y base de datos de n8n.
- `docs/`: Documentación técnica detallada (Instalación, Integración, Estabilidad).

## Log de Avances y Seguimiento de Tareas
* **[2026-03-16]**: Creación inicial del proyecto y configuración de Docker Compose para n8n.
* **[2026-03-17]**: Desarrollo de la interfaz Streamlit (`app.py`) y conexión básica por Webhook.
* **[2026-03-18]**: Corrección de dependencias de Docker para estabilidad del frontend.
* **[2026-03-18]**: Implementación de extracción de File ID mediante Regex para búsqueda exacta en Google Drive.
* **[2026-03-18]**: Instalación y configuración de **n8n-mcp** permitiendo que Antigravity interactúe con el backend.
* **[2026-03-18]**: Documentación de precisión y errores de JSON en n8n.
* **[2026-03-18]**: Se reconstruyó quirúrgicamente el flujo `Minutas-VENG` en n8n para corregir errores de sintaxis JSON y IDs de archivo hardcodeados, habilitando el procesamiento exacto por `document_id`.
* **[2026-03-18]**: Migración total de los nodos de lógica de Python a JavaScript nativo de n8n para eliminar la dependencia de "runners" y asegurar compatibilidad universal del flujo.
* **[2026-03-18]**: Transición de Google Drive a carga local de archivos. Se implementó procesamiento de `.docx` y `.txt` directamente en el frontend (Streamlit) y se simplificó el flujo n8n a solo 5 nodos esenciales.
* **[2026-03-18]**: Corrección final de robustez en el flujo `Minutas-VENG`. Se implementó limpieza automática de markdown en el parser de JSON y se corrigió la expresión del nodo de respuesta final, eliminando errores de "No data found".
* [2026-03-18]: Sincronización de Docker con `app.py`. Se añadió un volumen de montaje en `docker-compose.yml` para el frontend, permitiendo hot-reload y asegurando que los cambios de código (como la descarga en `.json`) se reflejen de inmediato sin reconstruir.
* **[2026-03-19]**: Rediseño premium "marketinero" y dark mode del frontend (app.py y config.toml) incorporando branding e imagen de VENG.
