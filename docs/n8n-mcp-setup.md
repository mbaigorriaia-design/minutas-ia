# Guía de Conexión n8n-MCP (Modo Docker) para Antigravity

Esta guía detalla el proceso paso a paso para conectar un entorno local de **n8n corriendo en Docker** con el asistente de IA **Antigravity** utilizando el servidor **n8n-mcp**.

---

## 📋 Requisitos Previos

1.  **Docker Desktop** (o Docker Engine) instalado y funcionando. 
    *   [Descargar Docker Desktop](https://www.docker.com/products/docker-desktop/)
2.  **Instancia de n8n** corriendo en un contenedor (normalmente en `http://localhost:5678`).
3.  **Antigravity** instalado y funcionando como IDE o chat de IA.

---

## 🚀 Paso 1: Descargar la Imagen del Servidor MCP

Dado que trabajamos con Docker, no es necesario instalar Node.js en tu máquina local. Vamos a descargar la imagen oficial que contiene toda la lógica del servidor MCP.

1.  Abre una terminal (PowerShell o CMD en Windows).
2.  Ejecuta el siguiente comando:
    ```bash
    docker pull ghcr.io/czlonkowski/n8n-mcp:latest
    ```
    *   **¿Dónde encontrar esto?**: Es la imagen oficial del repositorio [czlonkowski/n8n-mcp](https://github.com/czlonkowski/n8n-mcp).

---

## 🔑 Paso 2: Obtener las Credenciales de n8n

Para que la IA pueda "hablar" con tu n8n, necesita una llave (API Key).

1.  Entra en tu instancia de n8n: `http://localhost:5678`.
2.  Ve al menú lateral izquierdo y haz clic en **Settings** (Ajustes).
3.  Selecciona la pestaña **Personal API Keys**.
4.  Haz clic en **Create a new API Key**.
5.  **Copia y guarda** la clave en un lugar seguro. ¡No la compartas!
    *   **Instrucción**: Si no ves esta opción, asegúrate de estar usando una versión reciente de n8n (v1.0+).

---

## 🛠️ Paso 3: Configurar Antigravity (mcp_config.json)

Ahora debemos decirle a Antigravity que use Docker para ejecutar el servidor MCP.

1.  En Antigravity, haz clic en los **tres puntos `...`** (arriba a la derecha).
2.  Selecciona **MCP Servers**.
3.  Haz clic en **Manage MCP Servers**. Esto abrirá tu explorador de archivos en la carpeta de configuración.
4.  Busca y abre el archivo llamado `mcp_config.json`.
    *   **Ruta típica en Windows**: `C:\Users\<TU_USUARIO>\.gemini\antigravity\mcp_config.json`.
5.  Pega el siguiente bloque de configuración dentro del objeto `"mcpServers"`. 

> [!IMPORTANT]
> Debes reemplazar `TU_API_KEY_AQUI` con la clave que copiaste en el Paso 2.

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--init",
        "-e", "MCP_MODE=stdio",
        "-e", "LOG_LEVEL=error",
        "-e", "DISABLE_CONSOLE_OUTPUT=true",
        "-e", "N8N_MCP_TELEMETRY_DISABLED=true",
        "-e", "N8N_API_URL=http://host.docker.internal:5678",
        "-e", "N8N_API_KEY=TU_API_KEY_AQUI",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
```

### Notas sobre la configuración:
*   **`host.docker.internal`**: NO uses `localhost`. Como el MCP corre *dentro* de un contenedor de Docker, necesita esta dirección especial para poder ver a tu n8n que también está en Docker/Windows.
*   **`N8N_MCP_TELEMETRY_DISABLED=true`**: Esta línea asegura que no se envíen datos de uso anónimos fuera de tu red, garantizando máxima privacidad.

---

## 🔄 Paso 4: Reiniciar y Validar

1.  Guarda el archivo `mcp_config.json`.
2.  Vuelve a Antigravity (menú **Manage MCP Servers**).
3.  Haz clic en el botón de **Refresh** (icono de flechas circulares) para que cargue la nueva configuración.
4.  Deberías ver que `n8n-mcp` aparece con el estado **Enabled** o con una lista de herramientas.

---

## ✅ Paso 5: Prueba de Fuego

Para comprobar que todo está bien, escribe esto en el chat de Antigravity:

> *"¿Cuáles son mis flujos actuales en n8n?"*

Si la IA te responde con una lista de tus workflows (IDs y nombres), **¡felicidades!** Ya tienes el poder de n8n integrado en tu asistente de código.

---

## 📄 Recursos Adicionales
*   [Repositorio n8n-mcp (GitHub)](https://github.com/czlonkowski/n8n-mcp)
*   [Documentación de Antigravity](https://github.com/czlonkowski/n8n-mcp/blob/main/docs/ANTIGRAVITY_SETUP.md)
