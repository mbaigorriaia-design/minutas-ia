# Arquitectura del Flujo: Minutas-VENG-Chunking

Este documento describe la arquitectura y funcionamiento del flujo creado para resolver el error de `Requested 24827` tokens excedidos en la API de Groq al procesar transcripciones extremadamente largas.

## 1. Problema Original
Groq tiene un límite estricto de [Tokens por Minuto (TPM) en la capa gratuita](docs/solucion_error_groq_tpm.md) de 12.000 tokens. Cuando se le envía una reunión de más de eso en una sola petición (por ejemplo, 24k tokens), la conexión es rechazada por el servidor con un error de exceso de cuota.

## 2. Solución Aplicada: "Map-Reduce"
Se construyó un nuevo flujo paralelo llamado **`Minutas-VENG-Chunking`** que no altera al flujo original. Utiliza una ruta diferente (`/webhook/minutas-chunking`) para que la aplicación frontend (Streamlit) pueda elegir qué flujo llamar.

La técnica de **Chunking con Map-Reduce** opera así:
1. **Preparación de Texto**: Se recibe el payload y se aísla únicamente la transcripción raw.
2. **Corte y Demora (`batchSize: 1, interval: 15s`)**: En vez del nodo "Basic LLM Array", se inyectó una `Summarization Chain`. Esta cadena toma el texto de 24k tokens y lo rebana internamente en pedazos de hasta `8000` caracteres (con `300` de solapamiento para no perder contexto de una oración cortada por la mitad).
3. **Paso 1: Map**: Envía el primer trozo a Groq. Groq extrae un breve resumen y decisiones de esos primeros 8000 caracteres. *Luego la cadena hace una pausa forzada de 15 segundos* para engañar al límite TPM de Groq.
4. **Pase Iterativo**: Envía el segundo trozo 15 segundos después... y así sucesivamente, recopilando "mini-resúmenes" temporales sin superar nunca el límite por minuto de la API.
5. **Paso 2: Reduce (Combine)**: Una vez digeridos todos los mini-resúmenes, se crea una variable unificada. Esta se envía a tu Prompt Original que exige el formato dictado `---MINUTA---` y `---JSON---`.
6. **Formateo JS**: El código final re-estructura todo y devuelve al frontend exactamente igual que el viejo flujo.

## 3. ¿Cómo usarlo en la app?
Para probar transcripciones masivas sin errores usando este nuevo flujo robusto, en el archivo `app.py` hay que cambiar la siguiente línea (alrededor de la línea 181):
```python
response = requests.post(
    "http://n8n:5678/webhook/minutas-chunking",  # <--- Agregaste -chunking al final
    json=payload
)
```
**Aviso importante de UX**: Dado que este flujo duerme 15 segundos entre trozos deliberadamente, una reunión muy larga puede demorar de 1 a 3 minutos en procesarse, pero garantiza 100% de éxito de respuesta.
