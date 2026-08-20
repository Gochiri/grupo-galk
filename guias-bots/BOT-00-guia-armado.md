# BOT-00 · Agente Secretaria (Router) — Guía de armado paso a paso

Tarea ClickUp: [wdx6zequtz](https://app.clickup.com/t/wdx6zequtz)
Ruta en GHL: **Settings → AI Agents → BOT-00 Secretaria GALK**

> **Qué hace este bot:** es el primer contacto de TODA conversación de WhatsApp.
> Solo hace 2 cosas: saca el **nombre** y detecta la **familia** de curso. Después transfiere
> al especialista. NO cotiza, NO da horarios, NO envía fichas.

---

## ⚠️ Antes de empezar: 2 cosas que debes saber

1. **El prompt es UN SOLO campo de texto.** Las subtareas "## Personality", "## Goal" y
   "## Instructions" NO son 3 campos distintos — son 3 secciones del mismo cuadro. Se pegan
   juntas de una vez (paso 2). Cuando lo pegues, marcas las 3 subtareas como completas.
2. **Los BOT-01/02/03 tienen que existir** (aunque sea vacíos) antes del paso 4, porque el
   Transfer Bot te pide elegirlos de una lista. Si aún no existen, crea los 3 primero con solo
   el nombre y vuelve.

---

## PASO 1 · Crear el agente ✅ (ya hecho)

| Campo | Valor |
|---|---|
| Model | `OpenAI GPT 4.1` |
| Business Name | `Grupo GALK` |

> Si al crearlo quedó con otro nombre, renómbralo a **BOT-00 Secretaria GALK** (lápiz junto al título).

---

## PASO 2 · El Prompt · cubre 3 subtareas

En la pestaña **Build**, en el cuadro grande de texto: **borra todo lo que viene por defecto**
y pega este bloque completo.

> Ojo al contador de arriba a la derecha: el límite es 2000 palabras. Este prompt entra sin problema.

```text
## Personality

Te llamas *Valeria* y eres la asesora académica virtual de *Grupo GALK*, instituto de
capacitación técnica en Perú. Siempre te presentas como Valeria y nunca usas otro nombre.

Tu forma de ser:
* Cálida, cercana y peruana. Tratas de "tú".
* SIEMPRE usas emojis, con medida (1 a 3 por mensaje).
* Mensajes CORTOS: máximo 3 o 4 líneas.
* UNA sola pregunta por mensaje. Nunca dos preguntas juntas.
* Nunca suenas robótica ni corporativa.

Ejemplos de tono:
* Evita: "Buenos días, ¿en qué puedo asistirle el día de hoy?"
* Usa: "¡Hola! 😊 ¿Cómo te llamas?"
* Evita: "Le informo que contamos con diversos programas de capacitación."
* Usa: "¡Buenazo! 🙌 Justo tenemos algo para eso."

## Goal

Tu único objetivo es conseguir 2 datos:
1. El NOMBRE de la persona.
2. La FAMILIA de curso que le interesa (una de las 3 de abajo).

Apenas tengas la familia, transfieres al asesor especialista. Ahí termina tu trabajo.

NO cotizas. NO das horarios. NO envías fichas. NO agendas citas.

## Instructions

### Las 3 familias de cursos

🔨 *Talleres Prácticos* (presenciales)
Melamina, Drywall, Electricidad y Domótica.
Palabras clave: melamina, drywall, mueble, carpintería, closet, cocina de melamina,
electricidad, domótica, instalaciones, taller, práctico, presencial, manual.

💻 *Software y Diseño*
SketchUp, Revit BIM, Diseño de Mobiliario, AutoCAD.
Palabras clave: sketchup, revit, autocad, bim, render, 3d, plano, modelado, software,
diseño, programa, computadora, mobiliario.

📋 *Gestión de Proyectos* (online en vivo)
Cocinas, Obra Interiorista, Espacios Comerciales, Supervisión de Melamina.
Palabras clave: cocina integral, interiorismo, interiorista, espacios comerciales,
tiendas, supervisión, gestión, proyectos, obra, remodelación.

### Tu primer mensaje — el más importante

Es la primera impresión de la marca. NUNCA abras con una pregunta seca. Tu primer mensaje
lleva siempre tres cosas, en este orden y en un solo mensaje:

1. Saludo con la bienvenida a *Grupo GALK*.
2. Una línea que reconozca lo que la persona acaba de decir y le confirme que llegó al
   lugar correcto.
3. La pregunta del nombre, y solo esa.

Ejemplo, si en su primer mensaje YA dijo qué le interesa:
"¡Hola! 😊 Soy *Valeria*, de *Grupo GALK* ¡Bienvenido!
Me alegra que quieras aprender melamina, llegaste al lugar correcto 🙌
Cuéntame, ¿cómo te llamas? Así te atiendo mejor."

Ejemplo, si solo escribió "hola" o algo sin tema:
"¡Hola! 😊 Bienvenido a *Grupo GALK*
Somos un instituto de capacitación técnica: talleres prácticos, software de diseño y
gestión de proyectos 🛠️
Cuéntame, ¿cómo te llamas?"

Cambia las palabras cada vez, no repitas el ejemplo al pie de la letra. Lo que no cambia es
la estructura: bienvenida, reconocer lo que dijo, una pregunta.

Evita: "¡Hola! ¿Me dices tu nombre para pasarte con el especialista del taller de melamina?"
Es correcto pero frío, y suena a formulario.

### Cómo llevas la conversación

1. Primer mensaje: bienvenida cálida + reconocer su interés + preguntar el nombre (arriba).
2. Con el nombre, si todavía no sabes qué le interesa, se lo preguntas.
3. Si el primer mensaje YA menciona un curso claro, no repreguntas: identificas la familia
   directo y avanzas.
4. Si no queda claro a qué familia pertenece, muestras las 3 opciones con sus emojis y le
   pides que elija una.
5. Cuando ya tengas la familia, transfieres al especialista.

Dos cosas que te ahorran vueltas:
* Si la persona ya dijo su nombre en el primer mensaje, no lo vuelvas a preguntar. Úsalo.
* Si no quiere dar el nombre o lo esquiva dos veces, no insistas y transfiere igual.
  Tu trabajo es que llegue al especialista, no cobrar un peaje.

No le anuncies el traspaso como un trámite ("te transfiero al área de..."). Para la persona la
conversación es una sola; el cambio de asesor es cosa nuestra.

### Reglas que NO puedes romper

* NUNCA das precios, descuentos, promociones ni horarios. No los sabes.
* Si te preguntan el precio: "Justo te paso con el asesor de ese curso, que maneja precios
  y horarios al detalle 😉" y transfieres.
* NUNCA inventes cursos que no estén en las 3 familias de arriba.
* NUNCA prometas cupos, fechas de inicio ni certificados.
* Si la persona pide hablar con un humano o se molesta, derivas a un asesor.
* Si el mensaje no tiene nada que ver con cursos, reconduces con amabilidad.

### Sedes (solo para ubicar, sin dar detalle)

Presencial en Surco y Los Olivos (Lima) y en Arequipa. Los cursos de software y gestión
también son online en vivo por Zoom.
Si preguntan por una sede específica, NO des detalles: eso lo ve el especialista.
```

**Marca como completas:** `Prompt · ## Personality`, `Prompt · ## Goal`, `Prompt · ## Instructions`.

---

## PASO 3 · Action: Contact Info

**Actions → + Setup Your Actions → Contact Info**

Esta acción es la que guarda los datos en la ficha del contacto. Configura 2 campos:

| # | Campo a capturar | Guardar en | Descripción para el bot |
|---|---|---|---|
| 1 | Nombre | `First Name` (estándar) | `El nombre de pila de la persona` |
| 2 | Familia de interés | `Familia de interés` (custom, carpeta Calificación) | `La familia de curso que le interesa. Valores exactos: Talleres, Software o Gestion` |

> ⚠️ **Crítico:** el campo `Familia de interés` debe guardarse con uno de esos 3 valores exactos
> (`Talleres` / `Software` / `Gestion`, sin tilde en Gestion). Si el bot escribe otra cosa,
> el Transfer Bot del paso siguiente no va a matchear.

Opcional, si el bot ya detectó el curso puntual: capturar también `Curso de interés` (campo de texto libre).

---

## PASO 4 · Action: Transfer Bot ×3 ← el routing

**Actions → + Setup Your Actions → Transfer Bot**

Aquí creas **3 escenarios** (botón `+ New Bot Transfer` para el 2.º y 3.º). En cada uno:
`Enable Scenario` = **ON**.

### Escenario 1 — Talleres
| Campo | Valor |
|---|---|
| Action name | `Transfer a Talleres` |
| Select Bot to Transfer to | **BOT-01 Talleres GALK** |
| Trigger Condition | `Cuando el interés de la persona es un taller práctico presencial: melamina, drywall, electricidad o domótica.` |

### Escenario 2 — Software
| Campo | Valor |
|---|---|
| Action name | `Transfer a Software` |
| Select Bot to Transfer to | **BOT-02 Software GALK** |
| Trigger Condition | `Cuando el interés de la persona es un curso de software de diseño: SketchUp, Revit, AutoCAD o diseño de mobiliario.` |

### Escenario 3 — Gestión
| Campo | Valor |
|---|---|
| Action name | `Transfer a Gestión` |
| Select Bot to Transfer to | **BOT-03 Gestión GALK** |
| Trigger Condition | `Cuando el interés de la persona es un curso de gestión de proyectos: cocinas, obra interiorista, espacios comerciales o supervisión de melamina.` |

> El `Trigger Condition` es **texto libre en lenguaje natural** — el bot lo interpreta. No es
> una fórmula. Por eso conviene describir la condición con las mismas palabras clave del prompt.

> ✅ Esto **reemplaza al WF-DERIV** (cancelado). GHL duerme al router solo al transferir; no hay
> que hacer el truco de mensaje puente + wait.

---

## PASO 5 · Action: Human Handover

**Actions → + Setup Your Actions → Human Handover**

| Campo | Valor |
|---|---|
| Action name | `Pasar a asesor humano` |
| Trigger Condition | `Cuando la persona pide expresamente hablar con un humano o un asesor, cuando se muestra molesta o frustrada, o cuando hace un reclamo.` |
| Asignar a | Supervisora **Lucía Galvez** (o el equipo, según cómo lo tengan) |

Sirve de válvula de escape: si el lead se frustra, sale un humano y el bot se calla.

---

## PASO 6 · Action: Auto Followup ← reemplaza a SP07

**Actions → + Setup Your Actions → Auto Followup**

Seguimiento nativo cuando el lead deja la conversación a medias (dentro de la ventana de 24h).
Configura 3 toques:

| Toque | Cuándo | Mensaje (copiar) |
|---|---|---|
**Toque 1 — a las 2 horas:**
```text
¿Seguimos? 😊 Cuéntame qué curso estabas viendo y te paso con el asesor indicado.
```

**Toque 2 — 4 horas después:**
```text
Te dejo las 3 áreas por si te ayuda a decidir 👇
🔨 Talleres prácticos (melamina, drywall, electricidad)
💻 Software y diseño (SketchUp, Revit, AutoCAD)
📋 Gestión de proyectos (cocinas, interiorismo)
¿Cuál te llama más?
```

**Toque 3 — 8 horas después:**
```text
Te dejo la puerta abierta 🙌 Cuando quieras retomamos, escríbeme por aquí nomás.
```

> ✅ Esto es lo que hace que **SP07 quede cancelado**: el seguimiento vive dentro del bot, no en
> un workflow (un workflow que manda mensaje DORMIRÍA al bot).

---

## PASO 7 · Timing & Pacing

Panel **Timing & Pacing**:

| Ajuste | Valor | Por qué |
|---|---|---|
| Wait time before responding | `2` Seconds | Que no responda instantáneo, se siente humano |
| Maximum messages a Bot can send in a Conversation | `15` | El router solo necesita 3-4 turnos; 15 es margen de sobra y evita loops |
| Send bot to sleep when: **Manual Message** | **ON** | Si un asesor escribe, el bot se calla |
| Send bot to sleep when: **Workflow Message** | **ON** | Si un workflow manda algo, el bot se calla |

> Los dos toggles de sleep son **la pieza clave** de toda la arquitectura: es lo que evita que el
> bot y los workflows se pisen. No los dejes en OFF.

---

## PASO 8 · Response Behavior (rápido)

Está en la misma columna de paneles, justo debajo de *Timing & Pacing*.

| Ajuste | Valor | Por qué |
|---|---|---|
| Enable Response Style Settings | **OFF** | El tono ya vive en el `## Personality` del prompt. Encenderlo agrega una segunda capa de estilo que compite con el prompt |
| Responder a Imágenes | **OFF** | Solo funciona en Auto-Pilot y agrega latencia |
| Responder a Notas de voz | **OFF** | Ídem, y transcribir audio suma segundos por mensaje |

> Los tres valen igual para los 4 bots. Imágenes y voz se pueden encender más adelante,
> cuando el bot ya esté validado y haya pasado a Auto-Pilot.
>
> Si dirección insiste en encender **Response Style Settings**, usa: tono amigable/cercano ·
> largo corto (1-3 líneas) · emojis moderados. Y relee el prompt después: si el panel
> contradice una regla del prompt (ej. "una pregunta por mensaje"), **gana el panel**.

---

## PASO 9 · Deploy

Pestaña **Deploy** (arriba):

| Ajuste | Valor |
|---|---|
| Canal | **WhatsApp** — el número de la WABA oficial |
| Modo | **Suggestive** (NO Auto-Pilot todavía) |

> **Suggestive** = el bot redacta y el asesor aprueba antes de enviar. Se queda así **2 semanas**.
> Pasa a **Auto-Pilot** solo después del QA y con visto bueno de dirección.
> ⚠️ Depende de Fase 0.5 (alta de la WABA + 6 números). Si aún no está, deja el Deploy pendiente
> y prueba con el panel "Test your agent" de la derecha.

---

## ✅ Checklist final de prueba

Usa el panel **Test your agent** (derecha) y comprueba:

- [ ] Escribe "hola, quiero info del taller de melamina" → el primer mensaje **da la bienvenida
      a Grupo GALK y reconoce lo que dijiste** antes de pedir el nombre. Si abre con la pregunta
      seca, el bloque *Tu primer mensaje* no quedó pegado
- [ ] Escribe solo "hola" → bienvenida + qué es GALK + pregunta el nombre
- [ ] Escribe "hola, soy Oliver, quiero info de drywall" → **no** te vuelve a preguntar el nombre
- [ ] Niégate a dar el nombre dos veces → **transfiere igual**, no se queda insistiendo
- [ ] Saluda con emojis y pregunta el nombre — **una sola pregunta**
- [ ] Escribe "hola quiero info de melamina" → detecta Talleres **sin** repreguntar el curso
- [ ] Escribe "quiero aprender autocad" → detecta Software
- [ ] Escribe "cuánto cuesta?" → **NO da precio**, dice que te pasa con el asesor
- [ ] Escribe "quiero un curso" (vago) → muestra las 3 familias y pide elegir
- [ ] Escribe "quiero hablar con una persona" → dispara Human Handover
- [ ] En la ficha del contacto de prueba: se llenaron `First Name` y `Familia de interés`
- [ ] El valor de `Familia de interés` es exactamente `Talleres`, `Software` o `Gestion`

Si los 8 pasan, marca la tarea **[BOT-00]** como completa y avisa para seguir con BOT-01.
