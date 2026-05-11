# 🛠️ IT Operations Runbook - Minutas-IA

Este documento es el **Manual Oficial de Operaciones** exclusivo para el equipo de Infraestructura, DevOps y SysAdmins. Contiene toda la información técnica necesaria para monitorizar, respaldar y mantener el entorno en producción.

## 1. Topología de Red y Puertos (Networking)

El stack se despliega bajo una red Docker tipo `bridge` denominada `minutas-net`. 

| Contenedor | Puerto Interno | Puerto Expuesto (Host) | Uso |
| :--- | :--- | :--- | :--- |
| `frontend_ui` | 8501 | **8051** | Interfaz de Usuario final (Acceso HTTP). |
| `n8n` | 5678 | **5678** | Interfaz de administración de flujos (Webhooks). |
| `ollama` | 11434 | **11434** | API del LLM Local. |

> **⚠️ Atención Firewall:** Asegúrese de abrir/permitir tráfico HTTP en el puerto `8051` hacia la IP del servidor para que los usuarios finales puedan acceder a la herramienta.

## 2. Persistencia de Datos y Backups (Volumes)

El sistema utiliza Volúmenes Nombrados (Named Volumes) gestionados por Docker. **Es crítico incluir estos volúmenes en la política de Backups del servidor.**

- `minutas_n8n_data` (Montado en `/home/node/.n8n`): Contiene la base de datos SQLite interna de n8n, las credenciales, historial de ejecuciones y los flujos lógicos (Workflows). **(Prioridad Alta de Backup)**.
- `minutas_ollama_data` (Montado en `/root/.ollama`): Contiene los pesos de los modelos de IA descargados. **(Prioridad Baja de Backup)**, ya que si se pierde, el modelo se puede volver a descargar, pero pesa varios Gigabytes.

## 3. Variables de Entorno Críticas (ENV)

El archivo `docker-compose.yml` pre-configura las variables críticas. Si necesita modificarlas en Portainer, tenga en cuenta:

- `N8N_BLOCK_SSRF_GET_ADDITIONAL_HOSTS=ollama`: Permite a n8n saltarse las protecciones de red internas para poder consultar a la IA directamente por su nombre de contenedor.
- `OLLAMA_KEEP_ALIVE=60m`: Mantiene el modelo de IA cargado en memoria RAM durante 60 minutos después de la última consulta. Esto previene tiempos de carga lentos entre reuniones seguidas. Si el servidor tiene mucha presión de RAM, puede reducirse a `5m`.
- `N8N_BASE_URL=http://n8n:5678` (En el contenedor de Streamlit): Determina hacia dónde envía los datos el frontend.

## 4. Comandos de Mantenimiento Comunes

### A. Ver Logs en Tiempo Real (Troubleshooting)
Si el frontend muestra errores de timeout, revise los logs del orquestador:
```bash
docker logs -f n8n
```
Si el modelo tarda mucho en responder, revise Ollama:
```bash
docker logs -f ollama
```

### B. Gestión del Modelo de IA (Liberar Espacio)
Si necesita liberar espacio en el disco duro o actualizar el modelo base (`qwen2.5:3b`):
```bash
# Entrar al contenedor de Ollama
docker exec -it ollama /bin/bash

# Listar modelos instalados y su peso
ollama list

# Eliminar un modelo
ollama rm qwen2.5:3b
```

## 5. Prevención de Out-Of-Memory (OOM) en el Host
El sistema procesa texto pesado de manera asíncrona mediante un bucle de *Batches* (Chunking) en n8n para no saturar la RAM de Ollama. Si nota que el Host Linux colapsa (Kernel OOM Killer), asigne límites estrictos en Portainer o Docker Compose:

```yaml
deploy:
  resources:
    limits:
      memory: 6G
```
*(Idealmente asigne un máximo de 6GB a Ollama si el servidor tiene 8GB totales).*
