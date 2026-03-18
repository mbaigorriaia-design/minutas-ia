# Arquitectura del Proyecto n8n

El contenedor de **n8n** se encuentra **en ejecución y funcionando correctamente** en tu máquina (Estado: Up) exponiendo el puerto `5678`.

## Componentes y Arquitectura a Nivel Sistema

El proyecto está orquestado utilizando **Docker Compose** y consta de dos servicios principales conectados entre sí:

### 1. Servicio `n8n` (Backend / Orquestador de flujos)
- **Imagen Docker:** `n8nio/n8n:latest`
- **Puerto expuesto:** `5678` (Accesible en `http://localhost:5678/`)
- **Variable de Entorno (`WEBHOOK_URL`):** `http://localhost:5678/` que indica la URL base a utilizar para recibir webhooks.
- **Descripción:** Es el motor principal que ejecuta y diseña los flujos de automatización o integración de IA.
- **Persistencia de Datos (Volumen `n8n_data`):**
  El directorio local `./n8n_data` está mapeado a `/home/node/.n8n` dentro del contenedor. Todo el estado de la aplicación se guarda aquí de forma persistente para que no se pierda al reiniciar el contenedor. Contiene:
  - **`database.sqlite`:** Base de datos relacional (SQLite) donde n8n almacena la estructura de todos los workflows, las ejecuciones, configuraciones y credenciales registradas.
  - **`binaryData/`:** Carpeta utilizada para almacenar archivos temporales generados o procesados durante la ejecución de los workflows, liberando carga de memoria y base de datos.
  - **`config`:** Archivo que contiene la llave de encriptación (`encryptionKey`) que asegura (encripta) las credenciales y accesos guardados en la base de datos de n8n.
  - **`nodes/` con `package.json`:** Funciona como un sandbox para nodos desarrollados a medida instalados desde la comunidad (NPM). Actualmente, se encuentra libre de dependencias extras (`"dependencies": {}`).
  - **`git/`:** Soporte de integración con Git preparado, permitiendo la sincronización o respaldo del código (como workflows y credentials en formato JSON) fuera del sistema.
  - **Logs Principales (`*.log` / `crash.journal`):** Archivos donde el contenedor n8n registra eventos de sistema, ejecuciones y depuración de errores que hayan ocurrido.

### 2. Servicio `frontend_ui` (Interfaz de Usuario)
- **Contexto de compilación:** Directorio `./frontend_ui` (donde se sitúa el script `app.py`).
- **Contenedor:** `frontend_ui`
- **Puerto expuesto:** `8501` (Puerto estándar utilizado por Streamlit, accesible en `http://localhost:8501/`)
- **Relación con n8n:** Este servicio depende directamente del de n8n (`depends_on: - n8n`). Esto significa que Docker se asegurará de que n8n esté operativo antes de levantar el frontend. Esta arquitectura implica fuertemente que `frontend_ui` actúa como aplicación visual y dispara automatizaciones llamando al Webhook de n8n, mostrando luego los resultados a los usuarios finales.

## Conclusión de Verificación
1. **Los volúmenes y persistencia** están correctos: Tus credenciales, claves de encriptación y base de datos están bajo la carpeta `n8n_data` segura y aislada.
2. **El estado de docker** denota que está corriendo fluidamente hace más de 24 hs.
3. El frontend de Python y Streamlit está **separado y depende** del orquestador, lo cual es una excelente práctica.

Podemos continuar sin problemas con el siguiente paso.
