# Integración de la Interfaz con n8n

Esta pequeña guía documenta cómo se comunica el nuevo front-end de Streamlit con tu flujo del Generador de Minutas en n8n.

## 1. Punto de Entrada (Webhook) en n8n

El archivo `app.py` envía una solicitud HTTP para iniciar el flujo en n8n.
Asegúrate de que tu nodo **Webhook** inicial en tu flujo de n8n esté configurado de la siguiente manera:

- **Method**: `POST`
- **Path**: `minutas`
- **Respond**: Cambiar de *Immediately* a `Using 'Respond to Webhook' Node`. Esto es fundamental para poder retornar el texto generado a la app de Python y permitir su descarga posterior.

*(La URL del backend a la que envía la UI es `http://n8n:5678/webhook/minutas` gracias a que Streamlit y n8n están en la red de Docker Compose).*

## 2. El Payload Recibido (Input)

Cuando el usuario cliquea "Generar minutas", la app intenta extraer el ID exacto del documento y envía un payload JSON hacia n8n con el siguiente formato:

```json
{
  "document_url": "https://docs.google.com/document/d/AQUI_VA_EL_ID_DEL_DOC/edit",
  "document_id": "AQUI_VA_EL_ID_DEL_DOC"
}
```

### Recomendación para el flujo de n8n:
Para obtener la **máxima precisión**, no uses el nombre del archivo en tus nodos de búsqueda. Utilizá directamente el `document_id`:
-   En el nodo de **Google Drive (Download)**, seleccioná `File ID` e insertá el valor usando la expresión: `{{ $json.body.document_id }}`.
-   Esto garantiza que n8n procese exactamente el documento que pegaste en la interfaz, sin buscar versiones viejas o archivos similares.

## 3. Retornando el resultado (Nodo: Respond to Webhook)

Para que el flujo sea 100% interactivo y Streamlit active el botón de **"Descargar minutas"**, n8n debe enviar los resultados de vuelta a la UI mediante un nodo específico.

### Configuración Correcta (Sin errores de JSON):
En el nodo **"Respond to Webhook"**, configurá así:

1.  **Response Body:** `JSON`
2.  **Property to Send:** `minutas_texto`
3.  **Value:** Usá la expresión: `{{ $node["Groq Chat Model"].json.text }}`

> [!IMPORTANT]
> **No escribas las llaves `{ }` manualmente** en el campo de texto si estás usando el modo "JSON" de n8n. n8n arma el JSON por vos. Solo tenés que completar los campos "Property" y "Value".

Si el campo `Value` muestra un error de validación, asegurate de que el nodo de IA (`Groq Chat Model`) se haya ejecutado al menos una vez antes para que n8n pueda visualizar los datos.

### Comportamiento en la Interfaz:
-   **Si n8n devuelve `minutas_texto`:** Streamlit habilitará el botón de descarga y el archivo `.md` contendrá únicamente ese texto formateado.
-   **Si n8n devuelve otro formato:** La interfaz guardará la respuesta completa en formato JSON crudo para que no pierdas la información, pero no se verá como un documento de texto limpio.

> [!TIP]
> Asegúrate de que este sea el **último nodo** de tu flujo principal para que la interfaz no se quede esperando (timeout).

## 4. Iniciar la Interfaz (Docker)

Debido a la actualización de dependencias (`requirements.txt`), para que la interfaz sea estable y reconozca los cambios en los Webhooks, debés iniciar el entorno con el siguiente comando:

```bash
docker-compose up --build -d
```

Esto reconstruirá la imagen del frontend con `streamlit` y `requests` incluidos, evitando cierres inesperados.

## 5. Notas Adicionales y Resolución de Errores

- **El Webhook no está activo:** Recuerda que si el Webhook está inactivo (es decir, el workflow de n8n no está *Active*), deberías testear invocando la URL de test (cambiando `webhook/minutas` por `webhook-test/minutas` en el script Python temporalmente durante tu desarrollo).
- **Error Network / Connection Refused:** Verifica con `docker-compose ps` que tanto n8n como la UI estén operativos en la misma red.
