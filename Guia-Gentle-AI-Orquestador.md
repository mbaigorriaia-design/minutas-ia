# Guía de Uso Eficiente: Gentle AI + Antigravity (Gemini CLI)

Gentle AI transforma a este asistente en un **Orquestador de Equipos (Tech Lead)**, aplicando la metodología **Spec-Driven Development (SDD)**. En lugar de lanzar código desorganizado, el orquestador delega tareas a sub-agentes para asegurar calidad, persistencia arquitectónica y menor pérdida de contexto.

Como regla dorada, toda petición importante y estructural debe manejarse a través del orquestador utilizando comandos específicos de SDD para planificar antes de programar.

## 🚀 1. Inicialización y Configuración

Después de que termine la instalación (que está ejecutándose en segundo plano), debes abrir una nueva terminal y ejecutar `gentle-ai`. La interfaz te pedirá seleccionar tu agente (elige `Gemini CLI`). Con esto, mi sistema `antigravity` heredará las capacidades del orquestador.

En cada nuevo gran requerimiento o refactorización que vayas a realizar en tus proyectos, comienza la sesión "despertando" el estado persistente.

**Comando en el chat:**
```text
/sdd-init
```
> [!NOTE]
> Esto inicializa el contexto SDD. El agente escaneará tu entorno, cargará las memorias persistentes y se preparará para comenzar el ciclo de vida del desarrollo.

---

## 🏗️ 2. Flujo de Trabajo (Spec-Driven Development)

Para desarrollar una nueva funcionalidad abstracta (por ejemplo, "Crear un nuevo pipeline PEP 8 en Python para procesamiento de datos espaciales"), en vez de pedir el código de golpe, usa el ciclo SDD:

### Fase A: Exploración y Propuesta
Pide al agente que explore la viabilidad teórica y el estado actual del repositorio, y te presente una propuesta estructurada. No creará código aún.

**Comando en el chat:**
```text
/sdd-explore Agregar módulo de cálculo de trayectoria alineado con poliastro
```

> [!TIP]
> Si la tarea es amplia, una vez discutida y explorada, puedes iniciar el ciclo completo automatizado ejecutando:
> `/sdd-new [nombre-del-feature]`

### Fase B: Especificaciones y Diseño
El agente creará documentos analíticos o propuestas de dependencias y arquitectura. Si todo se alinea con las reglas obligatorias de tu proyecto (como **PEP 8, docstrings detallados, y variables snake_case para Python**), procederá a subdividir la implementación global en micro-tareas (*Task Breakdown*).

### Fase C: Implementación (`/sdd-apply`)
Una vez tengas la tabla con las tareas o la especificación lista, llega el turno de codificar. En esta fase el Agente ejecutará los sub-agentes en el fondo para editar el código directamente.

**Comando en el chat:**
```text
/sdd-apply
```
> [!IMPORTANT]
> A diferencia de una sugerencia rápida de código, este comando obliga a la IA revisora a apegarse 100% al documento maestro de diseño que se generó y a las pautas de estilo de tu entorno global de trabajo (indentación de 4 espacios, máximo 79 caracteres por línea, etc.).

### Fase D: Verificación (`/sdd-verify`)
Nunca des por terminada una implementación grande sin auditar. Sub-agentes especializados realizarán testing de las modificaciones efectuadas y constatarán que no existan regresiones o faltas respecto al estándar.

**Comando en el chat:**
```text
/sdd-verify
```

### Fase E: Archivando y Creando Memoria (`/sdd-archive`)
Las versiones de los LLMs tienen "amnesia" entre múltiples pláticas (hilos o conversaciones). Gentle-AI permite almacenar conocimiento trans-sesión.

**Comando en el chat:**
```text
/sdd-archive
```
> [!TIP]
> Esto consolida lo que se aprendió, las decisiones de arquitectura (ej: si usamos una librería en concreto, si aplicamos un patrón Observer) y el porqué, guardando tu esfuerzo estructural en tu repositorio. Cuando abras un hilo nuevo en el futuro y ejecutes `/sdd-init`, tu memoria tecnológica seguirá intacta.

---

## 🧠 3. Mejores Prácticas Generales para Proyectos con Gentle AI

1. **Evita el Desarrollo Desorganizado ("No inline work")**: Acostúmbrate a no pedirme la solución en código directo de problemas gigantes simplemente en un mensaje de chat; acostúmbrate a las fases de escalación del `/sdd-explore`. Mantén nuestro hilo conversacional enfocado a decisiones lógicas o directrices a los sub-agentes, y todo el código y análisis lo harán de fondo.
2. **Aplicando tu rigor estricto Python (PEP 8)**: Durante la planificación en la Fase A, recuérdame adherirme al documento matriz de estándares y estilo que poseas, o las guías de PEP 8; así, la tabla de tareas generadas ya incluirá como requerimiento absoluto que los módulos presenten validaciones rigurosas, uso coherente de mayúsculas en constantes, tipeos e imperativas descripciones de unidades físicas en funciones, sin excepciones.
3. **Escalación Controlada**: Si tienes una duda de Python puntual "cómo declaro esto", hazlo ordinariamente sin SDD y recibirás una respuesta inmediata. SDD brilla enormemente en la integración de n8n, manejo de bases de datos persistentes y arquitectura lógica.

### Resumen Rápido de Comandos SDD:

| Comando | Propósito | ¿Modifica Archivos de Código? |
| :--- | :--- | :--- |
| `/sdd-init` | Carga contexto y memorias activas del proyecto. | No |
| `/sdd-new <tema>` | Delega la planificación profunda de un requerimiento abstracto. | No |
| `/sdd-explore <tema>` | Investiga enfoques asumiendo contexto amplio. | No |
| `/sdd-apply` | Un sub-agente ejecuta de lleno la implementación pendiente. | **Sí** |
| `/sdd-verify` | Audita y evalúa el código implementado contra el plan original. | No |
| `/sdd-archive` | Cierra y guarda permanentemente el estado de esa nueva función. | No |

¡Empleando Gentle AI, `antigravity` funcionará como un Tech Lead en un entorno empresarial y mantendrá limpia la abstracción de tus programas espaciales y flujos de n8n!
