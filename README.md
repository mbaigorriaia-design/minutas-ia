<div align="center">
  <h1>⚡ Minutas-IA</h1>
  <p><strong>Un generador automatizado de minutas de reunión 100% On-Premise, seguro y potenciado por IA Local.</strong></p>
</div>

---

## 🎯 ¿Qué es Minutas-IA?
Minutas-IA es una aplicación de grado empresarial diseñada para transformar transcripciones de reuniones, audios y documentos largos en **minutas estructuradas, accionables y precisas**. Todo esto procesado de forma local (LLM On-Premise), garantizando **Privacidad Zero-Trust**. ¡Ningún dato sensible abandona tu servidor!

## ✨ Características Principales
- 🔒 **Privacidad Total**: Inferencia local con Ollama. Cero llamadas a APIs externas comerciales.
- ⚡ **Dos Modos Inteligentes**:
  - **Modo Rápido**: Para reuniones cortas. Procesamiento ágil con resultados directos.
  - **Modo Extenso (Anti-OOM)**: Algoritmo de *Chunking* avanzado y *Split-in-Batches* gestionado por n8n para documentos colosales, evitando colapsos de memoria RAM.
- 🧹 **Sanitización de Texto**: Motor de expresiones regulares (RegEx) optimizado en Python para eliminar marcas de tiempo innecesarias y ruidos de transcripción antes del procesamiento.
- 🎨 **Renderizado Inteligente y Resiliente**: Fallback estructurado en el frontend que garantiza una **Vista Previa Markdown** impecable (agrupando fechas y ocultando etiquetas de sistema) aunque la IA genere formatos inesperados.
- 📥 **Exportación Profesional**: Visualización limpia y descarga directa de la minuta en formato `.json` estructurado para una fácil integración con bases de datos o sistemas de tickets.

## 🛠️ Stack Tecnológico
- **Frontend**: `Streamlit` (Python 3.11) - Interfaz de usuario reactiva, moderna y con estilo *glassmorphism*.
- **Orquestador**: `n8n` (Node.js) - Gestión de flujos lógicos, enrutamiento y división de texto (Batches).
- **Motor de IA**: `Ollama` - Inferencia local para modelos LLM avanzados (como Llama 3 o Qwen).
- **Infraestructura**: `Docker` & `Docker Compose` - Contenedores aislados sobre una red interna segura (Bridge).

## 🚀 Arquitectura a Alto Nivel
1. El usuario carga la transcripción cruda en la **UI de Streamlit**.
2. Streamlit aplica limpieza semántica al texto y envía el *Payload HTTP* a **n8n**.
3. **n8n** enruta la petición según la longitud del documento y consulta a **Ollama** de forma segura vía red interna (`http://ollama:11434`).
4. **Ollama** analiza el contexto, extrae Decisiones, Acciones y Responsables, y le devuelve la data estructurada a **n8n**.
5. **n8n** retorna un JSON al **Frontend**, el cual utiliza un formateador heurístico para renderizar la Vista Previa perfecta sin ruido visual.

## 📦 Instalación y Despliegue
El proyecto está completamente contenerizado y listo para ejecutarse en entornos Linux de producción.

```bash
# 1. Clonar el repositorio
git clone https://github.com/mbaigorriaia-design/minutas-ia.git
cd minutas-ia

# 2. Levantar los servicios en background
docker compose up -d --build
```

*Desarrollado con ❤️ para llevar la automatización corporativa al siguiente nivel.*
