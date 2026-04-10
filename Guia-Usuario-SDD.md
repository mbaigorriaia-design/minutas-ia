# 🚀 Guía Rápida: Operando el Motor SDD (Agent Teams Lite)

Al tener el orquestador **SDD (Spec-Driven Development)** instalado en tu repositorio, ya no "hablas" con una IA para que programe al azar. Ahora **delegas tareas** a través de un ciclo de vida ordenado.

Esta guía sirve como tu hoja de trucos (Cheat Sheet) de escritorio.

---

## 🛠️ El Ciclo de Vida Exigido (El Camino Feliz)

Para asegurar la calidad extrema, el orquestador te obliga (o te recomienda fuertemente) seguir este flujo ordenado:

1. **`/sdd-init`**: 🔌 Enciende los motores y revisa las reglas.
2. **`/sdd-explore`**: 🔍 Analiza el problema y busca información.
3. **`/sdd-propose`**: 💡 Presenta una idea de solución.
4. **`/sdd-spec`**: 📝 Redacta los requerimientos funcionales técnicos.
5. **`/sdd-design`**: 📐 Crea la arquitectura del software.
6. **`/sdd-tasks`**: ✅ Divide el trabajo en un "Checklist" de Pasos.
7. **`/sdd-apply`**: 👨‍💻 Escribe el código o crea los nodos en el servidor.
8. **`/sdd-verify`**: 🛡️ Realiza pruebas de QA contra el código.
9. **`/sdd-archive`**: 💾 Consolida la memoria (Engram) y finaliza con el `context-logger`.

---

## 🐍 Ejemplo 1: Desarrollo en Python
*Imagina que quieres crear un script que limpie datos de un Excel.*

### 1. Inicializar
> **Tú escribes:** `/sdd-init`
*(El orquestador despierta, lee tus reglas de PEP 8 y se prepara).*

### 2. Explorar y Proponer
> **Tú escribes:** `/sdd-explore Necesito crear un script Python que lea un CSV de ventas, quite nulos, y lo guarde procesado.`
*(El agente busca en tus carpetas, revisa librerías como Pandas y te pregunta detalles).*

### 3. Especificar y Diseñar (Bypass opcional)
*Consejo: Si la tarea es chica, puedes decirle al orquestador que junte pasos:*
> **Tú escribes:** `/sdd-spec y /sdd-tasks para el limpiador de ventas.`
*(El agente crea las pruebas esperadas y te arma la lista de tareas).*

### 4. Implementar
> **Tú escribes:** `/sdd-apply ejecuta las tareas del limpiador de ventas.`
*(El sub-agente Ejecutor crea `limpiador_ventas.py`. Sabe que debe usar **PEP 8**, `snake_case` y `Docstrings` porque leyó las reglas de LIDR).*

### 5. Verificar y Cerrar
> **Tú escribes:** `/sdd-verify revisa si el código cumple todo y luego /sdd-archive`
*(El inspector revisa que no haya errores, valida el PEP 8. El archivero guarda los recuerdos y el **context-logger** escribe en `context-log.md` que hoy creaste el limpiador).*

---

## ⚙️ Ejemplo 2: Automatización con n8n
*Imagina que quieres un Bot de Telegram que guarde mensajes en Google Sheets.*

### 1. Inicializar
> **Tú escribes:** `/sdd-init arranquemos un nuevo flujo de n8n`

### 2. Exploración Inteligente
> **Tú escribes:** `/sdd-explore busca templates o nodos para Telegram a Google Sheets en n8n.`
*(El orquestador usa la herramienta `search_templates` de tu n8n-mcp, lee el manual de `n8n-workflow-patterns` y te sugiere la mejor arquitectura RAG o simple).*

### 3. Tareas
> **Tú escribes:** `/sdd-tasks divide la instalación en pasos.`
*(Te genera una tarea para Telegram Node, otra para Data Transformation, y otra para Sheets).*

### 4. Magia Pura (La Implementación)
> **Tú escribes:** `/sdd-apply construye el workflow del bot de Telegram en mi n8n.`
*(En vez de darte código suelto, el Agente lee las **n8n-skills**, conecta sus herramientas **n8n-mcp**, crea el workflow directamente en tu Localhost usando `n8n_create_workflow` y conecta todos los nodos).*

### 5. Verificación (Quality Assurance)
> **Tú escribes:** `/sdd-verify valida si el workflow creado en n8n tiene errores o le faltan credenciales.`
*(Usa `n8n_validate_workflow`, arregla si olvidó un parámetro y finalmente el `context-logger` deja rastro en tu `context-log.md`).*

---

## ⚡ Comandos Rápidos "Hacks"

Si tienes prisa y la tarea es muy sencilla (ej. Corregir una variable), no precisas hacer los 9 pasos. Puedes usar "Atajos Autorizados":

*   **Implementación Directa:** `/sdd-explore y /sdd-apply Cambia la url de la base de datos en config.py`
*   **Inspección Rápida:** `/sdd-verify Valida que el workflow 15 no tenga errores de sintaxis en sus expresiones {{ }}`

> **NOTA VITAL:** Nunca olvides usar el comando **`/sdd-init`** cada vez que reabras el IDE al día siguiente o tras un cierre, es la llave inglesa que enciende el motor.
