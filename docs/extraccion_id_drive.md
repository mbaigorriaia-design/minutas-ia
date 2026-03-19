# Documentación: Extracción de ID de Google Drive

Este documento describe la mejora implementada para garantizar que n8n reciba el archivo exacto desde la interfaz de usuario, eliminando errores de precisión causados por búsquedas ambiguas.

## 1. El Problema Original
La interfaz enviaba una URL completa a n8n. n8n utilizaba nodos de búsqueda que podían devolver múltiples resultados (versiones antiguas, archivos con nombres similares, etc.), lo que confundía a la IA y generaba minutas poco precisas.

## 2. La Solución: Extracción de ID por Regex
Se implementó una función de extracción en el frontend (`app.py`) que utiliza expresiones regulares para obtener el ID único de Google Drive de cualquier link pegado.

**Patrón Regex utilizado:** `[-\w]{25,}`

### Comportamiento:
1.  **Input:** El usuario pega un link de Drive (ej. `https://docs.google.com/document/d/1A2B3C4D.../edit`).
2.  **Procesamiento:** La aplicación detecta el ID (`1A2B3C4D...`).
3.  **Visualización:** Se muestra un aviso informativo en la UI confirmando el ID detectado.
4.  **Envío a n8n:** El payload JSON ahora incluye un campo extra: `"document_id": "1A2B3C4D..."`.

## 3. Integración en n8n
Para aprovechar este cambio, el flujo de n8n debe configurarse para usar el `document_id`:

-   **Nodo de Entrada:** Recibe la clave `document_id`.
*   **Nodo de Google Drive (Download):** 
    -   **File:** Seleccionar `By ID`.
    -   **File ID:** Usar la expresión `{{ $json.body.document_id }}`.

## 4. Beneficios
-   **Precisión Total:** n8n descarga siempre el archivo exacto.
-   **Velocidad:** Se elimina el paso intermedio de búsqueda ("Search files").
-   **Robustez:** La interfaz funciona igual si el usuario pega el link completo o solo el ID del archivo.
