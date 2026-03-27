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
* **[2026-03-19]**: Rediseño avanzado del frontend (UI/UX) incorporando efecto "Glassmorphism", tipografía Inter (Google Fonts), diseño oculto por pestañas (Tabs) y panel Dark Mode.
* **[2026-03-19]**: Creación de carpeta `Ejemplos/` con casos de prueba de transcripciones de reuniones de diversa complejidad (básica y stress-test).
* **[2026-03-19]**: Limpieza de logs redundantes de n8n (`n8nEventLog.log`) y configuración de `.gitignore` previo al primer commit para evitar trackear información transitoria.
* **[2026-03-20]**: Diseño e implementación de arquitectura "Chunking" (Map-Reduce) para evadir el límite de 12k TPM de la API de Groq en archivos extensos. Se crearon los documentos técnicos en `docs/` y el flujo paralelo `Minutas-VENG-Chunking` en n8n mediante la API MCP (dejando intacto el flujo original).
* **[2026-03-20]**: Verificación exitosa del estado activo del flujo de Chunking (`/webhook/minutas-chunking`) en el contenedor de n8n.
* **[2026-03-20]**: Parche en `app.py` para manejar excepciones de Timeout de red (`JSONDecodeError`) de n8n al procesar archivos de Chunking mayores a 2 minutos. Documentado en `docs/reparacion_timeout_chunking.md`.
* **[2026-03-20]**: Identificación y documentación del límite de Tokens por Día (TPD: 100k) de la capa gratuita de Groq. Se comprobó que el flujo responde con reintentos automáticos (Langchain backoff de 15 mins) tras agotar la cuota, explicando la demora asíncrona atrapada por el frontend.
* **[2026-03-26]**: Refactorización crítica de estabilidad en `app.py`: Se eliminó el uso de `st.rerun()` que ocultaba el mensaje de éxito en la UI, se implementó un `timeout=120` real en `requests.post()` para evitar el congelamiento infinito de Streamlit, y se corrigió el manejo de excepciones diferenciando correctamente un `requests.exceptions.Timeout` de red de un `json.JSONDecodeError`.
* **[2026-03-26]**: Corrección de desincronización y lógica en el flujo de Chunking (n8n): Se identificó que el webhook estaba devolviendo mensajes de texto asíncronos inmediatos causando un error temprano de "Respuesta no válida" en Streamlit. Se ajustó el nodo `Entrada Minuta Chunking` a "Using Respond to Webhook Node". En adición, se aumentó dinámicamente el timeout en `app.py` a 10 minutos (600s) cuando se selecciona el modo "Extenso". Por último, se corrigió el script JavaScript del `JS Parser Final` para extraer correctamente el texto del LLM desde `item.json.response.text`.
* **[2026-03-26]**: Optimización extrema de Tokens IA: Se implementó una función de pre-procesamiento en `app.py` que usa Expresiones Regulares para limpiar las transcripciones largas (borrado de marcas de tiempo como `[00:15:20]`, colapso de tabulaciones y reducción de saltos de línea continuos) antes de enviarlas a n8n. Esto busca reducir dramáticamente la cantidad de tokens utilizados en el modo Extenso, ayudando a mitigar el límite diario gratuito de la API de Groq.
