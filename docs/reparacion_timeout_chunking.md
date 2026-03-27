# Solución: Desconexión de Webhook (Timeout) en Flujo Chunking

## 1. Análisis del Problema Reportado
El usuario reportó un comportamiento confuso: la interfaz web en Streamlit arrojaba un error de tipo:
`Error de conexión: Expecting value: line 1 column 1 (char 0)`
Sin embargo, al ver el backend, en el entorno de n8n se observaba claramente que el flujo "Minutas-VENG-Chunking" **seguía ejecutándose** ("Running in 3m 32s").

### La Causa Raíz
Cuando se utiliza la estrategia de Chunking, la arquitectura incluye intencionalmente demoras forzadas (hasta 15 o más segundos entre fragmentos) para evitar el límite restrictivo de TPM de la API de Groq en la nube. 
Esto significa que procesar una reunión muy larga toma entre 1 a 5 minutos.
El problema está en que el servidor web interno Express/NodeJS de n8n tiene un tiempo de espera preestablecido para las peticiones HTTP (generalmente alrededor de 80 a 120 segundos). Cuando n8n está esperando a que su último nodo asíncrono termine (`responseMode: responseNode`), pero este límite se cumple, el servidor **cierra la conexión enviando una respuesta vacía con código `200 OK`**.
La aplicación `app.py` al recibir el `200`, invocaba el método `.json()` sobre una cadena vacía de texto, lo cual rompía el código base de Python al intentar parsearlo como JSON (`json.JSONDecodeError`).

## 2. Modificaciones Aplicadas

Para solucionar esto sin desestabilizar la red interna pidiendo conexiones mantenidas irrestrictamente, se optó por un enfoque centrado en UX y control de fallos en el Frontend.

Se ha modificado el archivo `frontend_ui/app.py` (Línea 233):
**Código Anterior:**
```python
except Exception as e:
    st.error(f"Error de conexión: {str(e)}")
```

**Código Actualizado:**
```python
except json.JSONDecodeError as je:
    st.error(f"⚠️ **Timeout del servidor n8n**: El archivo es demasiado extenso y demoró más del tiempo máximo de red (120 segundos). La IA sigue procesando tu minuta en el fondo y se guardará como ejecución exitosa en n8n, pero Streamlit no pudo esperar la respuesta.")
except Exception as e:
    st.error(f"Error de conexión: {type(e).__name__} - {str(e)}")
```

- **Impacto**: A partir de ahora el usuario comprenderá la razón del fallo, y más importante, **entenderá que su información no se perdió, sino que la minuta terminará de generarse de manera exitosa directo en la base de datos o almacenamiento de n8n**, gracias al flujo programado.
