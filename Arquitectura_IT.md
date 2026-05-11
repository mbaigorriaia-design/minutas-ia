# Presentación de Arquitectura: Minutas-IA

## 1. Diagrama de Infraestructura y Red (Mermaid)

Este diagrama detalla cómo se comunican los contenedores de forma aislada y segura en el servidor, sin depender de redes externas.

```mermaid
graph TD
    %% Estilos de Infraestructura
    classDef client fill:#ffffff,stroke:#333,stroke-width:2px;
    classDef container fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#000;
    classDef network fill:#f5f5f5,stroke:#9e9e9e,stroke-width:2px,stroke-dasharray: 5 5;
    classDef storage fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#000;

    Client[💻 Cliente Web / Browser]:::client

    subgraph "Docker Host Server (Linux)"
        direction TB
        
        subgraph "Red Interna: minutas-ia_default (Bridge)"
            
            UI[📦 Contenedor: Streamlit<br/>Puerto Expuesto: 8501<br/>Python 3.11]:::container
            N8N[📦 Contenedor: n8n<br/>Puerto Expuesto: 5678<br/>Node.js]:::container
            OLLAMA[📦 Contenedor: Ollama<br/>Puerto Interno: 11434<br/>Inferencia Local]:::container
            
            UI -- "Llamada HTTP/REST\n(Payload JSON)" --> N8N
            N8N -- "API Call Interna\n(Resolución por DNS Docker)" --> OLLAMA
            OLLAMA -- "Respuesta JSON" --> N8N
            N8N -- "Respuesta 200 OK" --> UI
        end
        
        V_N8N[(Volumen: n8n_data)]:::storage
        V_OLLAMA[(Volumen: ollama_data)]:::storage
        
        N8N -. "Persistencia de flujos" .-> V_N8N
        OLLAMA -. "Caché de Modelos" .-> V_OLLAMA
    end

    Client -- "Acceso UI (HTTP:8501)" --> UI
    
    %% Nota de Privacidad
    classDef security fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    SecNote>🔒 100% On-Premise. Zero External API Calls]:::security
    OLLAMA -.- SecNote
```

## 2. Argumentos Técnicos para Infraestructura / Seguridad

**1. Privacidad de Datos Total (Zero-Trust Compliant):**
El pipeline completo de IA se ejecuta de forma *On-Premise* dentro de la red local. A diferencia de soluciones comerciales como ChatGPT o Claude, **ningún documento sensible, grabación o minuta abandona los servidores de la empresa**. 

**2. Arquitectura Contenerizada Aislada:**
La solución está empaquetada mediante `docker-compose.yml` utilizando una red de tipo *Bridge* aislada. Ollama no expone sus puertos al exterior; Streamlit y n8n se comunican con él estrictamente mediante la resolución DNS interna de Docker (`http://ollama:11434`), minimizando drásticamente la superficie de ataque.

**3. Prevención de OOM (Out Of Memory) y Estabilidad:**
Se ha diseñado un middleware en **n8n** con un patrón avanzado de *Split-in-Batches* (Chunking). Esto previene que audios o reuniones extremadamente largas colapsen la memoria RAM del contenedor del orquestador, dividiendo la carga de procesamiento del LLM en paquetes manejables en lugar de saturar el contexto del modelo.

**4. Resiliencia de Interfaz (Graceful Fallback):**
El sistema se rige bajo un contrato de datos estricto (JSON). Si por algún motivo de alta concurrencia el motor de IA falla en generar el renderizado Markdown estandarizado, la aplicación central en Python intercepta el JSON crudo y renderiza visualmente la estructura a prueba de fallos. Esto garantiza que el usuario final nunca experimente pantallas de error o fallos catastróficos en la UI.
