# Análisis de Precisión: Webhook vs Manual

Al comparar las ejecuciones manuales con las disparadas vía Webhook, hemos identificado por qué las minutas podrían ser menos "acertadas" cuando usás la interfaz de Python.

## 1. El Problema: Resultados del Nodo "Search en Google Drive"

En los logs de n8n, observamos que cuando el Webhook recibe la URL, se activa un nodo de **"Search files and folders"**. 
- **En la ejecución manual:** Seguramente seleccionás el archivo exacto.
- **En la ejecución vía Webhook:** Si el criterio de búsqueda (la URL que pegás en el frontend) es muy amplio o si el nodo de Google Drive no está filtrando por ID exacto, puede que n8n esté encontrando **varias versiones o archivos similares**.

Si el flujo procesa una lista de archivos en lugar de uno solo, el prompt que llega a la IA (Groq) se vuelve confuso o genérico, lo que baja la calidad del resumen.

## 2. Diferencia en el Prompt (Instrucciones)

Los logs muestran que el prompt que se le envía a Groq tiene una estructura muy específica:
`---MINUTA--- ... ---JSON---`
Si al correrlo manualmente usás una instrucción distinta (un prompt más largo o con más ejemplos), la IA se comportará de forma diferente.

## 3. Resolución: ¿Cómo mejorar la precisión?

Para que la ejecución vía Webhook sea tan buena como la manual, te recomendamos estos ajustes en tu flujo de n8n:

1.  **Filtro por ID:** En el nodo de Google Drive que busca el archivo, asegurate de que esté configurado para buscar por "File ID" si es posible, o que el filtro de búsqueda sea lo más estricto posible (`name = 'nombre exacto'`).
2.  **Verificar el Input:** En la pestaña de *Execution* de n8n, buscá una ejecución que haya venido de la UI (isManual: false) y compará el texto que bajó en el nodo "Download file" con el que tenés en la ejecución manual.
3.  **Configuración del LLM:** Asegurate de que el parámetro `temperature` en el nodo de Groq sea el mismo en ambos casos (recomendado 0.7 para minutas).

### Conclusión
Lo más probable es que el nodo de búsqueda esté devolviendo una **lista de archivos** (como la que me pasaste antes en el JSON largo) y la IA esté tratando de resumir "un poco de todo". Si logramos que n8n reciba un único archivo exacto, la precisión será idéntica a la manual.
