# Guía de Estabilidad para Docker Desktop (Windows)

Si notás que Docker se vuelve inestable (se traba, se cierra solo o consume el 100% de tu CPU) al intentar construir la nueva versión del proyecto, seguí estos pasos:

## 1. Limpieza de Recursos (Paso de Oro)
A veces Docker tiene "restos" de instalaciones anteriores que bloquean la memoria. Ejecutá este comando en tu terminal de VS Code:

```bash
docker system prune -f
```
*(Esto borra capas de archivos que no se están usando, es seguro).*

## 2. Ajuste de Límites en `docker-compose.yml`
He actualizado tu archivo de configuración para "ponerle correa" a los procesos y que no consuman todo tu equipo:
- **n8n:** Limitado a 1GB de RAM.
- **Frontend UI:** Limitado a 512MB de RAM.
- **CPU:** Ambos componentes ahora comparten el procesador de forma más equitativa para no trabar Windows.

## 3. Reestablecimiento del Motor Docker
Si el icono de la ballena sigue en rojo o naranja:
1. Abrí **Docker Desktop**.
2. Tocá el icono del **Estetoscopio** (Troubleshoot) arriba a la derecha.
3. Tocá el botón **"Clean / Purge data"**. 
*(Ojo: Esto borrará tus imágenes actuales, pero se volverán a descargar solas y limpias).*
4. Tocá **"Restart"**.

## 4. Intento Limpio de Construcción
Una vez que el Docker esté "verdecito" y estable, ejecutá:
```bash
docker-compose up --build -d
```
