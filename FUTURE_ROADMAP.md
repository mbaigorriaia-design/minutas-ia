# 🚀 Roadmap & Trabajo Futuro (Performance)

Este documento enumera las oportunidades arquitectónicas recomendadas para el equipo de desarrollo entrante. El objetivo de estas implementaciones es reducir drásticamente los tiempos de procesamiento (como el *timeout* de 40 minutos en documentos inmensos) y escalar el sistema de manera eficiente.

## 1. Aceleración por Hardware (GPU / vRAM)
Actualmente, el contenedor de Ollama procesa los prompts consumiendo la CPU y los 32GB de memoria RAM (DDR).
- **Propuesta:** Adquirir una GPU dedicada (incluso tarjetas de gama de entrada como una NVIDIA RTX 3060 de 12GB o RTX 4060 Ti de 16GB) e integrarla en el servidor Linux.
- **Implementación:** Modificar el `docker-compose.yml` para habilitar el *NVIDIA Container Toolkit*:
  ```yaml
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
  ```
- **Impacto:** Los documentos de Word que actualmente tardan 40 minutos en procesarse, pasarían a resolverse en **3 a 5 minutos** gracias al procesamiento matricial paralelo de la GPU.

## 2. Procesamiento de Texto en Paralelo (Map-Reduce)
Actualmente, cuando un documento de Word tiene más de 40 páginas, el sistema divide el texto en *Chunks* y los envía a Ollama uno por uno (de forma secuencial).
- **Propuesta:** Implementar un patrón de arquitectura **Map-Reduce**.
- **Implementación:** 
  1. Enviar múltiples Chunks a Ollama simultáneamente utilizando llamadas asíncronas (`asyncio` en Python o múltiples hilos en el *Split-in-Batches* de n8n).
  2. Tener un prompt de "Reduce" final que consolide los resúmenes parciales en la Minuta JSON definitiva.
- **Impacto:** Reducción lineal del tiempo de procesamiento equivalente al número de hilos paralelos permitidos por el procesador del servidor.

## 3. Implementación de RAG (Retrieval-Augmented Generation)
En lugar de forzar a Ollama a "leer" 40 páginas de corrido para armar una minuta, el sistema podría ser más inteligente.
- **Propuesta:** Integrar una base de datos vectorial ultraligera (como **ChromaDB** o **Qdrant**).
- **Implementación:** Al subir el archivo de Word, el texto se convierte en *Embeddings* matemáticos y se guarda en la base de datos. Luego, el motor de IA solo extrae y lee los párrafos que contienen decisiones, fechas clave o tareas, ignorando el "texto basura".
- **Impacto:** Ahorro masivo de contexto (tokens), previniendo cualquier tipo de OOM y mejorando la precisión de la minuta generada.

## 4. Caché de Peticiones Repetidas
- **Propuesta:** Integrar **Redis** o utilizar la caché interna de Streamlit/FastAPI.
- **Implementación:** Si un usuario sube el mismo documento de Word exacto (mismo hash/checksum) que otro usuario ya procesó ayer, el sistema debería devolver instantáneamente el JSON cacheado en lugar de despertar a Ollama para que vuelva a pensar durante 40 minutos.
