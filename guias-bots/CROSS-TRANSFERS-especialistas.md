# Cross-transfers entre bots especialistas

> **Qué resuelve.** Hoy solo BOT-00 sabe derivar. Si un lead ya está en BOT-01 Talleres y
> pregunta por AutoCAD, se queda ahí y le contestan mal o lo mandan a un humano.
> Faltan **6 escenarios de Transfer Bot**: 2 en cada especialista, hacia los otros dos.

```
                    BOT-00 Secretaria (router)
                     │        │        │
          ┌──────────┘        │        └──────────┐
          ▼                   ▼                   ▼
   BOT-01 Talleres  ◄────► BOT-02 Software ◄────► BOT-03 Gestión
          ▲                                          ▲
          └──────────────────────────────────────────┘
              los 6 cross-transfers que faltan
```

---

## ⚠️ Antes de configurar: el bloqueante

La acción **Contact Info solo rellena campos VACÍOS, no sobrescribe.**

Sin resolver eso, el cross-transfer nace roto: un lead le dice "melamina" a BOT-01, cambia a
AutoCAD, pasa a BOT-02, BOT-02 intenta escribir `Curso de interés = AutoCAD`, el campo **ya
dice "Melamina"** → se queda en Melamina → **SP05 le manda la ficha equivocada** y SP06 lo
califica con el curso de la otra familia.

Por eso existe **`WF-SWITCH | Limpiar interés al cambiar de familia`**
(`f72ee2f3-e29d-4894-883b-2aae4a7005a8`, draft, carpeta 01). Vacía los 10 campos de interés
—`Familia`, `Modalidad`, `Sede`, `Pack x2`, sus 4 gemelos `(bot)`, `Curso` y `Horario`— para que
el bot receptor arranque limpio. **No toca** nombre, teléfono, correo ni la atribución de Meta.

Los dropdown se vacían **antes** que los `(bot)`: si fuera al revés, WF-NORM vería cambiar el
campo `(bot)` y volvería a escribir el dropdown que acabamos de limpiar.

### Los 3 puntos a validar en QA (no los doy por hechos)

1. **Que Contact Info efectivamente no sobrescriba.** Es la premisa de todo esto. Prueba: contacto
   con `Curso de interés` ya lleno, que el bot intente escribir otro. Si sí sobrescribe,
   WF-SWITCH sobra y se quita.
2. **El orden de las acciones.** Necesitamos que el bot ejecute *Trigger a Workflow (WF-SWITCH)*
   **antes** del *Transfer Bot*. Las dos condiciones están redactadas para eso, pero quien decide
   el orden es el modelo. Si en la prueba transfiere primero y limpia después, el plan B es mover
   el `Trigger a Workflow` al bot **receptor**, como su primera acción.
3. **Que no haya ping-pong** entre BOT-01 y BOT-03 (ver la trampa de la melamina, abajo).

---

## La trampa de la melamina 🚨

Es el par de mayor riesgo de bucle:

| Curso | Qué es | Bot |
|---|---|---|
| **Taller de Melamina** | práctico, presencial, fabricar muebles con las manos | BOT-01 |
| **Gestión y Supervisión de Melamina (G2)** | online, gestionar proyectos y equipos | BOT-03 |

Los dos dicen "melamina". Si las condiciones no lo distinguen, BOT-01 manda a BOT-03, BOT-03
lee "melamina" y lo devuelve a BOT-01, y así. Por eso las condiciones de ese par están
redactadas por **intención** (¿quiere hacerlo con sus manos o quiere dirigir a otros?), nunca
por la palabra suelta.

---

## Regla anti-bucle (va en los 6 escenarios)

Cada `Trigger Condition` termina con esta frase. Cópiala tal cual:

```
Transfiere SOLO si la persona abandona el interés anterior y quiere otra cosa. Si solo lo
menciona de paso, compara dos cursos, o pregunta si existen otros, respóndele que sí existen
y sigue tú con el tema original. Si ya te transfirieron a ti en esta conversación, no
devuelvas a la persona al bot que te la pasó.
```

---
---

# BOT-01 · Talleres Prácticos

**Actions → + Setup Your Actions → Transfer Bot** → `+ New Bot Transfer` (dos veces).
`Enable Scenario` = **ON** en los dos.

## Escenario A — hacia Software

| Campo | Valor |
|---|---|
| Action name | `Transfer a Software` |
| Select Bot to Transfer to | **BOT-02 Software GALK** |

**Trigger Condition:**
```
Cuando la persona deja de interesarse por los talleres presenciales y lo que quiere es aprender
un programa de diseño en computadora: SketchUp, renders, Revit, BIM, AutoCAD, planos en 2D o
diseño de mobiliario para fabricación. Transfiere SOLO si la persona abandona el interés
anterior y quiere otra cosa. Si solo lo menciona de paso, compara dos cursos, o pregunta si
existen otros, respóndele que sí existen y sigue tú con el tema original. Si ya te transfirieron
a ti en esta conversación, no devuelvas a la persona al bot que te la pasó.
```

## Escenario B — hacia Gestión

| Campo | Valor |
|---|---|
| Action name | `Transfer a Gestión` |
| Select Bot to Transfer to | **BOT-03 Gestión GALK** |

**Trigger Condition:**
```
Cuando la persona deja de interesarse por el taller práctico y lo que quiere es gestionar o
dirigir proyectos, no fabricar con sus manos: diseño y gestión de cocinas, obra interiorista,
espacios comerciales o supervisión de proyectos de melamina. Ojo con la melamina: el taller de
melamina es práctico y lo llevas tú; el curso de supervisión de melamina es de gestión, es
online y va con el otro asesor. Si la persona quiere aprender a fabricar los muebles, se queda
contigo. Transfiere SOLO si la persona abandona el interés anterior y quiere otra cosa. Si solo
lo menciona de paso, compara dos cursos, o pregunta si existen otros, respóndele que sí existen
y sigue tú con el tema original. Si ya te transfirieron a ti en esta conversación, no devuelvas
a la persona al bot que te la pasó.
```

---

# BOT-02 · Software y Diseño

## Escenario A — hacia Talleres

| Campo | Valor |
|---|---|
| Action name | `Transfer a Talleres` |
| Select Bot to Transfer to | **BOT-01 Talleres GALK** |

**Trigger Condition:**
```
Cuando la persona deja de interesarse por los cursos de software y lo que quiere es un taller
práctico presencial, trabajando con herramientas y materiales: melamina, drywall, electricidad
o domótica. Transfiere SOLO si la persona abandona el interés anterior y quiere otra cosa. Si
solo lo menciona de paso, compara dos cursos, o pregunta si existen otros, respóndele que sí
existen y sigue tú con el tema original. Si ya te transfirieron a ti en esta conversación, no
devuelvas a la persona al bot que te la pasó.
```

## Escenario B — hacia Gestión

| Campo | Valor |
|---|---|
| Action name | `Transfer a Gestión` |
| Select Bot to Transfer to | **BOT-03 Gestión GALK** |

**Trigger Condition:**
```
Cuando la persona deja de interesarse por aprender un programa de diseño y lo que quiere es
gestionar o dirigir proyectos: diseño y gestión de cocinas, obra interiorista, espacios
comerciales o supervisión de proyectos de melamina. Transfiere SOLO si la persona abandona el
interés anterior y quiere otra cosa. Si solo lo menciona de paso, compara dos cursos, o pregunta
si existen otros, respóndele que sí existen y sigue tú con el tema original. Si ya te
transfirieron a ti en esta conversación, no devuelvas a la persona al bot que te la pasó.
```

---

# BOT-03 · Gestión de Proyectos

## Escenario A — hacia Talleres

| Campo | Valor |
|---|---|
| Action name | `Transfer a Talleres` |
| Select Bot to Transfer to | **BOT-01 Talleres GALK** |

**Trigger Condition:**
```
Cuando la persona deja de interesarse por los cursos de gestión y lo que quiere es un taller
práctico presencial para trabajar con sus propias manos, con herramientas y materiales:
melamina, drywall, electricidad o domótica. Ojo con la melamina: si la persona quiere aprender
a fabricar muebles, ese es el taller práctico y va con el otro asesor; si quiere dirigir el
proyecto y supervisar a otros, se queda contigo. Transfiere SOLO si la persona abandona el
interés anterior y quiere otra cosa. Si solo lo menciona de paso, compara dos cursos, o pregunta
si existen otros, respóndele que sí existen y sigue tú con el tema original. Si ya te
transfirieron a ti en esta conversación, no devuelvas a la persona al bot que te la pasó.
```

## Escenario B — hacia Software

| Campo | Valor |
|---|---|
| Action name | `Transfer a Software` |
| Select Bot to Transfer to | **BOT-02 Software GALK** |

**Trigger Condition:**
```
Cuando la persona deja de interesarse por los cursos de gestión y lo que quiere es aprender a
usar un programa de diseño en computadora: SketchUp, renders, Revit, BIM, AutoCAD, planos en 2D
o diseño de mobiliario para fabricación. Transfiere SOLO si la persona abandona el interés
anterior y quiere otra cosa. Si solo lo menciona de paso, compara dos cursos, o pregunta si
existen otros, respóndele que sí existen y sigue tú con el tema original. Si ya te transfirieron
a ti en esta conversación, no devuelvas a la persona al bot que te la pasó.
```

---
---

## La acción que acompaña — en los 3 bots

**Actions → + Setup Your Actions → Trigger a Workflow**

| Campo | Valor |
|---|---|
| Action name | `Limpiar interés al cambiar de familia` |
| Workflow a disparar | `WF-SWITCH | Limpiar interés al cambiar de familia` |

**Cuándo ejecutar:**
```
Justo antes de transferir a la persona a otro asesor especialista porque cambió de familia de
curso. Ejecuta esto primero y transfiere después. No lo ejecutes si la persona sigue en el mismo
tipo de curso, ni cuando la transfieres a un asesor humano.
```

---

## Qué agregar al prompt de cada bot

En el bloque `## Instructions`, al final:

```
Si la persona cambia de tema hacia un curso que no es de los tuyos, no improvises ni le des
precios de esos cursos. Dile en una frase que sí lo tienen y que le pasas con el asesor que lo
maneja, y transfiere. Si solo lo menciona de paso o está comparando, confírmale que existe y
retoma tu tema.
```

---

## Orden de armado

1. Los 3 bots creados y con sus prompts (si no, el desplegable de *Select Bot to Transfer to*
   sale vacío).
2. `Trigger a Workflow → WF-SWITCH` en los 3.
3. Los 6 escenarios de Transfer Bot.
4. QA de los 3 puntos de arriba, con foco en el ping-pong BOT-01 ↔ BOT-03.
