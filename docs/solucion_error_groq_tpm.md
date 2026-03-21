# Solución: Error de Límite de Tokens (TPM) en Groq

## Análisis del Error
El error que muestra tu captura de pantalla en el nodo `Basic LLM Chain` de n8n es:
> *"Request too large for model llama-3.3-70b-versatile... Limit 12000, Requested 24827"*

**¿Por qué ocurre esto?**
La transcripción que subiste es sumamente extensa. El texto representa **24.827 tokens**. Sin embargo, tu cuenta gratuita (*on_demand*) en la API de Groq tiene un límite estricto de **12.000 Tokens Por Minuto (TPM)** para el modelo `llama-3.3-70b-versatile`. Al enviar todo el bloque de texto de la reunión en una sola petición, el servidor de Groq rechaza la llamada por superar tu límite de cuota.

---

## Posibles Soluciones (Sin modificar código Python)

A continuación, presento 4 soluciones ordenadas según el impacto en tu flujo de n8n:

### Opción 1: Procesamiento por Bloques / Chunking (La Solución más Profesional)
En lugar de enviar un documento gigante de una sola vez, la mejor práctica en flujos de Inteligencia Artificial es dividirlo ("chunking").
*   **Acción en n8n**: En lugar de usar una `Basic LLM Chain` directa, debes usar un nodo **Summarization Chain** (o un nodo de ejecución por lotes) combinado con un parser como **Recursive Character Text Splitter**.
*   **Cómo funciona**: n8n dividirá tu reunión automáticamente en, por ejemplo, 3 o 4 partes más pequeñas. Procesará cada bloque poco a poco (respetando los límites de Groq) y luego la IA unirá todos los mini-resúmenes en una sola minuta final estructurada.

### Opción 2: Reemplazo por Ollama en Local (Sin límites de API)
Como sugeriste en una pregunta anterior, puedes evitar las APIs en la nube y correr el modelo localmente en tu PC.
*   **Ventaja**: Ollama corre en tu hardware, por lo que **no existe el límite de 12.000 TPM**. Puedes inyectar textos del tamaño que quieras sin que nadie rechace la petición (tu único límite será el hardware de tu computadora).
*   **Acción en n8n**: Borra el nodo con el ícono rojo de `Groq Chat Model`. En su lugar, arrastra el nodo `Ollama Chat Model` y conéctalo exactamente donde estaba el anterior. Solo debes asegurarte de configurar el parámetro de "Context Window" en Ollama para que acepte más de 25.000 tokens en memoria.

### Opción 3: Cambiar a un modelo "más ligero" en Groq
A veces, los proveedores de IA dan más margen de TPM a sus modelos más pequeños.
*   **Acción en n8n**: Abre la configuración del nodo `Groq Chat Model` y despliega la lista de "Models". Cambia el modelo pesado `llama-3.3-70b...` por uno más liviano que ofrece Groq (como `llama-3.1-8b-instant` o `gemma-2-9b-it`). 
*   *Nota:* Verifica primero en tu panel de desarrollador de Groq (pestaña Limits) si los modelos más pequeños tienen un límite superior a 25.000 TPM permitidos para tu cuenta.

### Opción 4: Actualizar el plan de Groq (La Solución Inmediata)
Si necesitas mantener la velocidad extrema de Groq y usar el poderoso modelo de 70 billones de parámetros (70b) enviando documentos súper largos en un solo golpe sin rediseñar tu flujo.
*   **Acción**: Entrar a la URL que indica el error (`console.groq.com/settings/billing`) y registrar una tarjeta para pasar a la capa "Developer" (Pay as you go). Esto elevará automáticamente tus límites TPM multiplicando su capacidad, permitiendo procesar reuniones enteras en 1 segundo.
