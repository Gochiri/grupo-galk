# Actualizaciones de ClickUp — BOT-02 y BOT-03

> **Por qué existe este archivo.** El 5-ago ClickUp devolvió `RATE_LIMIT_EXCEEDED`
> (`retryAfter` ≈ 23 h) a mitad de la tarea, así que estas descripciones no se pudieron
> escribir por API. Cada bloque de abajo es el **reemplazo completo** de la descripción de
> su tarjeta: copiar y pegar en el campo de descripción, o esperar a que se levante el
> límite y subirlas por API.

Es el mismo nivel de detalle que ya tiene BOT-01 (ejemplos de utterance → valor, mensajes
finales, avisos de WF-NORM y del tag `galk-bot-calificado`), adaptado a cada familia.

Las tarjetas de **Knowledge Base** de los dos bots (`wdx6zequwd`, `wdx6zequwp`) **ya quedaron
actualizadas** antes del corte — no están aquí.

---
---

# BOT-02 · Software y Diseño

---

## 🗂 `wdx6zequwc` — Action · Contact Info (Curso · Modalidad · Sede · Horario)

https://app.clickup.com/t/wdx6zequwc

```markdown
## ⚠️ Usar los campos de TEXTO, no los dropdown
Las acciones del bot **no pueden escribir en dropdowns**. Se escriben los gemelos `(bot)` y **WF-NORM** los normaliza.

**Actions → Añadir Información de contacto** → `+ Añadir nuevo campo` para los 4.

### Campo 1 — Curso de interés _(ya es TEXT, directo)_

| Panel | Valor |
|---|---|
| Nombre de la acción | `Capturar curso` |
| Campo a actualizar | `Curso de interés` |
| Qué actualizar en el campo | `El curso de software que quiere llevar. Escribe exactamente uno de estos: SketchUp, Revit BIM, Diseño de Mobiliario, AutoCAD.` |
| Pregunta a formular | `¿Cuál te interesa? 💻 SketchUp + Render, Revit BIM, Diseño de Mobiliario o AutoCAD` |
| Cuándo ejecutar | `Cuando la persona indica cuál de los cuatro cursos quiere. Si ya venía identificado del bot anterior, no vuelvas a preguntar.` |

**Ejemplos:**

```
"sketchup" → SketchUp
"el de render" → SketchUp
"quiero hacer renders" → SketchUp
"quiero revit" → Revit BIM
"el de bim" → Revit BIM
"el de muebles" → Diseño de Mobiliario
"diseño de mobiliario" → Diseño de Mobiliario
"despiece de muebles" → Diseño de Mobiliario
"autocad porfa" → AutoCAD
"planos en 2d" → AutoCAD
"quiero aprender 3d" → (no guardar, repreguntar: ¿SketchUp o Revit?)
```

### Campo 2 — **Modalidad (bot)** ← TEXTO

| Panel | Valor |
|---|---|
| Nombre de la acción | `Capturar modalidad` |
| Campo a actualizar | `Modalidad (bot)` |
| Qué actualizar en el campo | `Cómo quiere llevar el curso. Escribe SOLO una de estas palabras, sin nada más: Online o Presencial.` |
| Pregunta a formular | `¿Cómo prefieres llevarlo? 💻 Online en vivo por Zoom o 📍 Presencial en Surco` |
| Cuándo ejecutar | `Pregunta la modalidad SOLO si el curso es SketchUp o Revit BIM, que son los únicos con ambas opciones. Si el curso es Diseño de Mobiliario o AutoCAD, escribe Online de inmediato sin preguntar, porque solo existen online.` |

**Ejemplos:**

```
"online" → Online
"por zoom" → Online
"desde mi casa" → Online
"virtual" → Online
"prefiero presencial" → Presencial
"quiero ir al local" → Presencial
"en surco" → Presencial   (y la Sede queda Surco)
curso = AutoCAD → Online   (sin preguntar)
curso = Diseño de Mobiliario → Online   (sin preguntar)
"estoy en arequipa" → Online   (no hay presencial fuera de Surco; se le aclara en el chat)
"me da igual" → (no guardar, repreguntar: ¿online o presencial?)
```

> ⚠️ Una sola palabra: `Online` o `Presencial`. WF-NORM normaliza por coincidencia de texto;
> si el bot escribe una frase, el match se ensucia y el dato queda mal.

### Campo 3 — **Sede (bot)** ← TEXTO, automática

| Panel | Valor |
|---|---|
| Nombre de la acción | `Fijar sede` |
| Campo a actualizar | `Sede (bot)` |
| Qué actualizar en el campo | `Si la modalidad es Presencial, escribe SOLO: Surco. Si la modalidad es Online, escribe SOLO: No aplica. Surco es la única sede presencial de los cursos de software.` |
| Pregunta a formular | (dejar vacío — no se pregunta) |
| Cuándo ejecutar | `Apenas quede definida la modalidad. No preguntes por la sede: se deduce de la modalidad.` |

**Ejemplos:**

```
modalidad = Presencial → Surco
modalidad = Online → No aplica
"¿puedo ir a Los Olivos?" → Surco   (única sede de software; se le aclara en el chat)
"¿lo dictan en Arequipa?" → No aplica + modalidad Online   (Arequipa no dicta software)
```

### Campo 4 — Horario de interés _(ya es TEXT, directo)_

| Panel | Valor |
|---|---|
| Nombre de la acción | `Capturar horario` |
| Campo a actualizar | `Horario de interés` |
| Qué actualizar en el campo | `El horario que eligió la persona de la ficha de horarios que recibió. Guarda el día y el turno tal como lo dijo, en formato corto. Por ejemplo: "sábados mañana", "lunes y miércoles noche", "domingos tarde". No inventes horarios ni sugieras ninguno.` |
| Pregunta a formular | `¿Cuál de esos horarios te acomoda mejor? 🕐` |
| Cuándo ejecutar | `Solo DESPUÉS de que la persona recibió la ficha con los horarios. Nunca antes: los horarios cambian cada semana y tú no los conoces.` |

**Ejemplos:**

```
"los sábados en la mañana" → sábados mañana
"el sábado temprano" → sábados mañana
"prefiero de noche entre semana" → entre semana noche
"martes y jueves en la noche" → martes y jueves noche
"el domingo" → domingos
"domingos por la tarde" → domingos tarde
"el de las 7pm" → entre semana noche   (si la ficha ubica esa hora en ese bloque)
"cualquiera me sirve" → (no guardar, pedir que elija uno de la ficha)
```

## Recordatorios generales
*   Contact Info **solo rellena campos vacíos**, no sobrescribe.
*   Nombre / correo / teléfono NO van aquí (se piden en el prompt).
*   Los gemelos `(bot)` los normaliza **WF-NORM** (`e97e101e…`) a los dropdown reales.
*   Este bot **no tiene Pack x2**: el pack existe solo en talleres presenciales (BOT-01).
```

---

## 🗂 `wdx6zequwf` — Action · Trigger a Workflow → SP05

https://app.clickup.com/t/wdx6zequwf

```markdown
## Acción en GHL
**Actions → Trigger a Workflow**

| Panel | Valor |
|---|---|
| Nombre de la acción | `Enviar ficha del curso` |
| Workflow a disparar | `SP05 | Envío de ficha (árbol 24 ramas)` |
| Cuándo ejecutar | `Cuando ya tengas guardados el curso Y la modalidad de la persona. Con esos dos datos la ficha que se envía es la correcta: el precio cambia bastante entre online y presencial.` |

**Ejemplos:**

```
curso "SketchUp" + modalidad "Online" → ejecutar   (ficha online 740→370)
curso "SketchUp" + modalidad "Presencial" → ejecutar   (ficha Surco 1100→550)
curso "SketchUp" sin modalidad → NO ejecutar todavía
curso "AutoCAD" → ejecutar   (la modalidad se autocompleta Online)
curso "Diseño de Mobiliario" → ejecutar   (ídem)
```

## Contexto
SP05 ya está construido (draft, `ae78625c-8f91-4af1-a7b0-3be0b2e4a667`): matchea curso+modalidad
en su árbol de 24 ramas y envía la ficha desde el Custom Value correspondiente — **sin URLs
hardcodeadas** (§6).

Si la combinación no matchea, la rama "None" de SP05 manda una notificación interna de
"ficha sin match".
```

---

## 🗂 `wdx6zequwg` — Action · Human Handover

https://app.clickup.com/t/wdx6zequwg

```markdown
## Acción en GHL
**Actions → Human Handover**

| Panel | Valor |
|---|---|
| Nombre de la acción | `Pasar a asesor humano` |
| Cuándo ejecutar | `Cuando la persona pide hablar con un humano, se muestra molesta, hace un reclamo, pide una excepción de precio o descuento que no está en tu información, pregunta por los requisitos técnicos de su computadora, o pregunta algo que no puedes responder con tu base de conocimiento.` |
| Asignar a | Supervisora **Lucía Galvez** |

## 💬 Mensaje final (el que envía el bot antes de callarse)

```
¡Por supuesto! 🙌 Le paso tu caso a un asesor del equipo de software y diseño para que lo vea a detalle.
Te escriben por aquí mismo en un rato 😊
```

> Menciona **"del equipo de software y diseño"** para que el lead sepa que va con alguien que
> conoce su curso, no a un buzón genérico. Y avisa que responden por el mismo canal.
> No promete tiempos exactos a propósito.

**Ejemplos que disparan la acción:**

```
"me pueden hacer un descuento especial?"
"quiero hablar con alguien"
"puedo pagar en cuotas?"
"necesito factura a nombre de mi empresa"
"cuál es el temario completo de Revit?"
"mi laptop aguanta SketchUp?"
"las clases quedan grabadas?"
```

> Ojo: este handoff es distinto del de SP06. Aquel ocurre cuando el lead **sí se calificó**
> (4/4 datos). Este es la válvula de escape cuando la conversación se traba antes.
```

---

## 🗂 `wdx6zequwh` — Action · Trigger a Workflow → SP06

https://app.clickup.com/t/wdx6zequwh

```markdown
## Acción en GHL
**Actions → Trigger a Workflow**

| Panel | Valor |
|---|---|
| Nombre de la acción | `Marcar lead calificado` |
| Workflow a disparar | `SP06 | Calificación y asignación` |
| Cuándo ejecutar | `Solo cuando los CUATRO datos estén guardados: curso, modalidad, sede y horario de interés. Si falta alguno, no ejecutes: sigue conversando hasta completarlos.` |

**Ejemplos:**

```
curso ✅ modalidad ✅ sede ✅ horario ✅ → ejecutar
curso "Revit BIM" ✅ modalidad ✅ sede ✅ pero sin horario → NO ejecutar
curso "AutoCAD" ✅ (modalidad y sede automáticas) + horario ✅ → ejecutar
```

## ⚠️ Si usas tag en vez de disparar el workflow
El tag correcto es **`galk-bot-calificado`** — NO `lead-calificado`.

**Motivo (hallazgo 2026-07-23):** el workflow **"WF1 | IA Califica el Lead" de Francisco está
PUBLICADO y vivo**, y usa `lead-calificado`. Si SP06 escuchara ese tag, se dispararía con leads
reales del sistema viejo: movería oportunidades reales al pipeline nuevo y asignaría asesores.
El trigger de SP06 ya fue cambiado a `galk-bot-calificado`, exclusivo del sistema nuevo.

## Contexto
SP06 (draft `84811c16-30d8-4c08-a05d-0c12fa46567d`): Calificado → round robin 6 asesores →
**escribe el asesor EN EL CONTACTO** → Asignado a asesor → notifica → tag `bot-silenciado`.
```

---

## 🗂 `wdx6zequwj` — Timing & Pacing (+ Response Behavior)

https://app.clickup.com/t/wdx6zequwj

```markdown
## Acción en GHL
Panel **Timing & Pacing**:

| Ajuste | Valor | Por qué |
|---|---|---|
| Wait time before responding | `2` Seconds | Que no responda instantáneo, se siente humano |
| Maximum messages a Bot can send in a Conversation | `25` | El especialista conversa más que el router (curso → modalidad → ficha → horario) |
| Sleep when **Manual Message** | **ON** | Si un asesor escribe, el bot se calla |
| Sleep when **Workflow Message** | **ON** | Si SP05/SP06 mandan algo, el bot se calla |

⚠️ Los 2 toggles de sleep son la pieza clave de la arquitectura: son la razón de que
**WF-DERIV y SP07 estén cancelados**, y el respaldo del handoff cuando SP06 asigna el lead.

## Panel vecino · Response Behavior

Está justo debajo, en la misma columna.

| Toggle | Valor | Por qué |
|---|---|---|
| Enable Response Style Settings | **OFF** | El tono ya vive en el `## Personality` del prompt. Encenderlo agrega una segunda capa de estilo que compite con el prompt |
| Responder a Imágenes | **OFF** | Solo funciona en Auto-Pilot y agrega latencia |
| Responder a Notas de voz | **OFF** | Ídem, y transcribir audio suma segundos por mensaje |

> Si dirección insiste en encender **Response Style Settings**: tono amigable/cercano · largo
> corto (1-3 líneas) · emojis moderados. Y relee el prompt después: si el panel contradice una
> regla del prompt (ej. "una pregunta por mensaje"), **gana el panel** y rompe la calificación.
>
> Imágenes y voz se revisitan tras las 2 semanas en Suggestive, al pasar a Auto-Pilot.
```

---

## 🗂 `wdx6zerppy` — Action · Auto Followup (reemplaza SP07)

https://app.clickup.com/t/wdx6zerppy

```markdown
## Acción en GHL
**Actions → Auto Followup** — 3 toques dentro de la ventana de 24h.

**Cuándo ejecutar:** `Cuando la persona deja de responder antes de completar los cuatro datos de calificación.`

### Toque 1 — 2 horas

```
¿Seguimos? 😊 ¿Te ayudo a elegir la modalidad o el horario del curso?
```

### Toque 2 — +4 horas

```
Los precios de preventa son por tiempo limitado 💻 ¿Te paso con un asesor para que te dé los detalles?
```

### Toque 3 — +8 horas

```
Te dejo la info a la mano 🙌 Cuando quieras retomamos, escríbeme por aquí.
```

## ✅ Reemplaza a SP07
SP07 quedó cancelado: un workflow que manda mensajes **dormiría al bot** (ver Timing & Pacing →
sleep on Workflow Message). Fuera de la ventana de 24h sí actúa un workflow: **SP08** con
plantilla Meta.
```

---

## 🗂 `wdx6zerppz` — Deploy · WhatsApp + Suggestive

https://app.clickup.com/t/wdx6zerppz

```markdown
## Acción en GHL
Pestaña **Deploy**

| Ajuste | Valor |
|---|---|
| Canal | WhatsApp — número de la WABA oficial |
| Modo | Suggestive (NO Auto-Pilot todavía) |

**Suggestive** = el bot redacta, el asesor aprueba antes de enviar. 2 semanas mínimo.
Auto-Pilot solo tras QA punta a punta.

⚠️ Depende de **Fase 0.5** (WABA + 6 números). Mientras tanto, probar con **"Test your agent"**.
Nunca conectar a un número de GoGHL (§5.1).
```

---
---

# BOT-03 · Gestión de Proyectos

---

## 🗂 `wdx6zequwr` — Action · Contact Info (Curso · Horario + Modalidad/Sede automáticas)

https://app.clickup.com/t/wdx6zequwr

```markdown
## ⚠️ Usar los campos de TEXTO, no los dropdown
Las acciones del bot **no pueden escribir en dropdowns**. Se escriben los gemelos `(bot)` y **WF-NORM** los normaliza.

**Actions → Añadir Información de contacto** → `+ Añadir nuevo campo` para los 4.

### Campo 1 — Curso de interés _(ya es TEXT, directo)_

| Panel | Valor |
|---|---|
| Nombre de la acción | `Capturar curso` |
| Campo a actualizar | `Curso de interés` |
| Qué actualizar en el campo | `El curso de gestión que quiere llevar. Escribe exactamente uno de estos: Cocinas, Obra Interiorista, Espacios Comerciales, Supervisión de Melamina.` |
| Pregunta a formular | `¿Cuál te interesa? 📋 Cocinas, Obra Interiorista, Espacios Comerciales o Supervisión de Melamina` |
| Cuándo ejecutar | `Cuando la persona indica cuál de los cuatro cursos quiere. Si ya venía identificado del bot anterior, no vuelvas a preguntar.` |

**Ejemplos:**

```
"cocinas" → Cocinas
"diseño de cocinas" → Cocinas
"el de interiorismo" → Obra Interiorista
"obra interiorista" → Obra Interiorista
"gestión de obra" → Obra Interiorista
"espacios comerciales" → Espacios Comerciales
"el de tiendas" → Espacios Comerciales
"supervisión" → Supervisión de Melamina
"el G2" → Supervisión de Melamina
"quiero aprender a hacer muebles de melamina" → (no guardar — eso es el TALLER práctico, va con BOT-01)
```

> ⚠️ El caso de arriba es el error clásico de este bot: **Supervisión de Melamina (G2) es de
> gestión**, no enseña a fabricar muebles. Si el lead quiere trabajar con sus manos, deriva.

### Campo 2 — **Modalidad (bot)** ← TEXTO, automática

| Panel | Valor |
|---|---|
| Nombre de la acción | `Fijar modalidad online` |
| Campo a actualizar | `Modalidad (bot)` |
| Qué actualizar en el campo | `Escribe SIEMPRE la palabra Online, sin nada más. Todos los cursos de gestión son online en vivo por Zoom, sin excepción. No preguntes la modalidad y no escribas ningún otro valor aunque el lead diga otra cosa.` |
| Pregunta a formular | (dejar vacío — no se pregunta) |
| Cuándo ejecutar | `Apenas se confirme que el interés es un curso de gestión. Escribe Online de inmediato, sin preguntar.` |

**Ejemplos:**

```
el lead eligió "Cocinas" → Online
el lead eligió "Espacios Comerciales" → Online
"¿hay presencial?" → Online   (el campo igual se llena; en el chat le explicas que son solo online)
"prefiero ir a la sede" → Online   (no existe presencial en gestión; se le aclara)
"vivo en Trujillo, ¿puedo?" → Online   (sí, justamente por ser online)
```

> El valor **nunca cambia**. Los ejemplos existen solo para que el modelo no se confunda cuando
> el lead menciona "presencial" o "sede" — el campo se llena igual con `Online`.

### Campo 3 — **Sede (bot)** ← TEXTO, automática

| Panel | Valor |
|---|---|
| Nombre de la acción | `Fijar sede no aplica` |
| Campo a actualizar | `Sede (bot)` |
| Qué actualizar en el campo | `Escribe SIEMPRE: No aplica. Estos cursos no tienen sede física porque son 100% online.` |
| Pregunta a formular | (dejar vacío — no se pregunta) |
| Cuándo ejecutar | `Junto con la modalidad, sin preguntar.` |

**Ejemplos:**

```
cualquier curso de gestión → No aplica
"¿dónde queda el local?" → No aplica   (y en el chat le explicas que es por Zoom)
"estoy en Arequipa" → No aplica   (da igual la ciudad, es online)
```

### Campo 4 — Horario de interés _(ya es TEXT, directo)_

| Panel | Valor |
|---|---|
| Nombre de la acción | `Capturar horario` |
| Campo a actualizar | `Horario de interés` |
| Qué actualizar en el campo | `El horario que eligió la persona de la ficha de horarios que recibió. Guarda el día y el turno tal como lo dijo, en formato corto. Por ejemplo: "sábados mañana", "lunes y miércoles noche", "domingos tarde". No inventes horarios ni sugieras ninguno.` |
| Pregunta a formular | `¿Cuál de esos horarios te acomoda mejor? 🕐` |
| Cuándo ejecutar | `Solo DESPUÉS de que la persona recibió la ficha con los horarios. Nunca antes: los horarios cambian cada semana y tú no los conoces.` |

**Ejemplos:**

```
"los sábados en la mañana" → sábados mañana
"el sábado temprano" → sábados mañana
"prefiero de noche entre semana" → entre semana noche
"martes y jueves en la noche" → martes y jueves noche
"el domingo" → domingos
"domingos por la tarde" → domingos tarde
"el de las 7pm" → entre semana noche   (si la ficha ubica esa hora en ese bloque)
"cualquiera me sirve" → (no guardar, pedir que elija uno de la ficha)
```

## Recordatorios generales
*   Contact Info **solo rellena campos vacíos**, no sobrescribe.
*   Nombre / correo / teléfono NO van aquí (se piden en el prompt).
*   Autocompletar modalidad y sede permite llegar a **4/4 campos con solo 2 preguntas reales** —
    es el bot más rápido de calificar de los tres.
*   Los gemelos `(bot)` los normaliza **WF-NORM** (`e97e101e…`) a los dropdown reales.
*   Este bot **no tiene Pack x2**: el pack existe solo en talleres presenciales (BOT-01).
```

---

## 🗂 `wdx6zequwt` — Action · Trigger a Workflow → SP05

https://app.clickup.com/t/wdx6zequwt

```markdown
## Acción en GHL
**Actions → Trigger a Workflow**

| Panel | Valor |
|---|---|
| Nombre de la acción | `Enviar ficha del curso` |
| Workflow a disparar | `SP05 | Envío de ficha (árbol 24 ramas)` |
| Cuándo ejecutar | `Apenas tengas guardado el curso. En esta área no hace falta esperar nada más: la modalidad es siempre Online y no hay sede, así que con el curso ya queda determinada la ficha.` |

**Ejemplos:**

```
curso "Cocinas" → ejecutar
curso "Obra Interiorista" → ejecutar
curso "Espacios Comerciales" → ejecutar
curso "Supervisión de Melamina" → ejecutar
todavía no sé qué curso quiere → NO ejecutar
```

> Es el único bot que dispara SP05 con **un solo dato**. BOT-01 necesita curso+sede y BOT-02
> curso+modalidad; aquí la modalidad y la sede son constantes.

## Contexto
SP05 ya está construido (draft, `ae78625c-8f91-4af1-a7b0-3be0b2e4a667`): matchea el curso en su
árbol de 24 ramas y envía la ficha desde el Custom Value correspondiente — **sin URLs
hardcodeadas** (§6).

Si la combinación no matchea, la rama "None" de SP05 manda una notificación interna de
"ficha sin match".
```

---

## 🗂 `wdx6zequwu` — Action · Trigger a Workflow → SP06

https://app.clickup.com/t/wdx6zequwu

```markdown
## Acción en GHL
**Actions → Trigger a Workflow**

| Panel | Valor |
|---|---|
| Nombre de la acción | `Marcar lead calificado` |
| Workflow a disparar | `SP06 | Calificación y asignación` |
| Cuándo ejecutar | `Solo cuando los CUATRO datos estén guardados: curso, modalidad, sede y horario de interés. Modalidad y sede se autocompletan, así que en la práctica basta con tener el curso y el horario. Si falta alguno, no ejecutes: sigue conversando hasta completarlos.` |

**Ejemplos:**

```
curso ✅ (modalidad Online y sede No aplica automáticas) + horario ✅ → ejecutar
curso "Cocinas" ✅ pero sin horario → NO ejecutar
horario ✅ pero sin curso → NO ejecutar
```

## ⚠️ Si usas tag en vez de disparar el workflow
El tag correcto es **`galk-bot-calificado`** — NO `lead-calificado`.

**Motivo (hallazgo 2026-07-23):** el workflow **"WF1 | IA Califica el Lead" de Francisco está
PUBLICADO y vivo**, y usa `lead-calificado`. Si SP06 escuchara ese tag, se dispararía con leads
reales del sistema viejo: movería oportunidades reales al pipeline nuevo y asignaría asesores.
El trigger de SP06 ya fue cambiado a `galk-bot-calificado`, exclusivo del sistema nuevo.

## Contexto
SP06 (draft `84811c16-30d8-4c08-a05d-0c12fa46567d`): Calificado → round robin 6 asesores →
**escribe el asesor EN EL CONTACTO** → Asignado a asesor → notifica → tag `bot-silenciado`.
```

---

## 🗂 `wdx6zequwv` — Action · Human Handover

https://app.clickup.com/t/wdx6zequwv

```markdown
## Acción en GHL
**Actions → Human Handover**

| Panel | Valor |
|---|---|
| Nombre de la acción | `Pasar a asesor humano` |
| Cuándo ejecutar | `Cuando la persona pide hablar con un humano, se muestra molesta, hace un reclamo, pide una excepción de precio o descuento que no está en tu información, pregunta por el temario completo o el detalle de la certificación, o pregunta algo que no puedes responder con tu base de conocimiento.` |
| Asignar a | Supervisora **Lucía Galvez** |

## 💬 Mensaje final (el que envía el bot antes de callarse)

```
¡Por supuesto! 🙌 Le paso tu caso a un asesor del equipo de gestión de proyectos para que lo vea a detalle.
Te escriben por aquí mismo en un rato 😊
```

> Menciona **"del equipo de gestión de proyectos"** para que el lead sepa que va con alguien que
> conoce su curso, no a un buzón genérico. Y avisa que responden por el mismo canal.
> No promete tiempos exactos a propósito.

**Ejemplos que disparan la acción:**

```
"me pueden hacer un descuento especial?"
"quiero hablar con alguien"
"puedo pagar en cuotas?"
"necesito factura a nombre de mi empresa"
"cuál es el temario completo?"
"las clases quedan grabadas?"
"qué tipo de certificado dan exactamente?"
```

> Ojo: este handoff es distinto del de SP06. Aquel ocurre cuando el lead **sí se calificó**
> (4/4 datos). Este es la válvula de escape cuando la conversación se traba antes.
```

---

## 🗂 `wdx6zerpq9` — Timing & Pacing + Auto Followup (+ Response Behavior)

https://app.clickup.com/t/wdx6zerpq9

```markdown
## A · Timing & Pacing

| Ajuste | Valor | Por qué |
|---|---|---|
| Wait time before responding | `2` Seconds | Que no responda instantáneo, se siente humano |
| Maximum messages a Bot can send in a Conversation | `20` | Es el flujo más corto de los tres (curso → ficha → horario) |
| Sleep when **Manual Message** | **ON** | Si un asesor escribe, el bot se calla |
| Sleep when **Workflow Message** | **ON** | Si SP05/SP06 mandan algo, el bot se calla |

⚠️ Los 2 toggles de sleep son la pieza clave de la arquitectura: son la razón de que
**WF-DERIV y SP07 estén cancelados**, y el respaldo del handoff cuando SP06 asigna el lead.

## B · Auto Followup (reemplaza SP07)

**Actions → Auto Followup** — 3 toques dentro de la ventana de 24h.

**Cuándo ejecutar:** `Cuando la persona deja de responder antes de completar los cuatro datos de calificación.`

### Toque 1 — 2 horas

```
¿Seguimos? 😊 ¿Te paso los horarios del curso?
```

### Toque 2 — +4 horas

```
Las clases son online en vivo, así que puedes llevarlas desde donde estés 📋 ¿Te paso con un asesor?
```

### Toque 3 — +8 horas

```
Te dejo la info a la mano 🙌 Cuando quieras retomamos, escríbeme por aquí.
```

> SP07 quedó cancelado: un workflow que manda mensajes **dormiría al bot**. Fuera de la ventana
> de 24h sí actúa un workflow: **SP08** con plantilla Meta.

## C · Response Behavior

| Toggle | Valor | Por qué |
|---|---|---|
| Enable Response Style Settings | **OFF** | El tono ya vive en el `## Personality` del prompt. Encenderlo agrega una segunda capa de estilo que compite con el prompt |
| Responder a Imágenes | **OFF** | Solo funciona en Auto-Pilot y agrega latencia |
| Responder a Notas de voz | **OFF** | Ídem, y transcribir audio suma segundos por mensaje |

> Si dirección insiste en encender **Response Style Settings**: tono amigable/cercano · largo
> corto (1-3 líneas) · emojis moderados. Y relee el prompt después: si el panel contradice una
> regla del prompt (ej. "una pregunta por mensaje"), **gana el panel** y rompe la calificación.
```

---

## 🗂 `wdx6zerpqa` — Deploy · WhatsApp + Suggestive

https://app.clickup.com/t/wdx6zerpqa

```markdown
## Acción en GHL
Pestaña **Deploy**

| Ajuste | Valor |
|---|---|
| Canal | WhatsApp — número de la WABA oficial |
| Modo | Suggestive (NO Auto-Pilot todavía) |

**Suggestive** = el bot redacta, el asesor aprueba antes de enviar. 2 semanas mínimo.
Auto-Pilot solo tras QA punta a punta.

⚠️ Depende de **Fase 0.5** (WABA + 6 números). Mientras tanto, probar con **"Test your agent"**.
Nunca conectar a un número de GoGHL (§5.1).
```
