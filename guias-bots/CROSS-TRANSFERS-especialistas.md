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

## ⚠️ Límite del panel: 10–500 caracteres

La **Condición de activación** no acepta más de 500 caracteres. Las de abajo están medidas y
entran todas (entre 337 y 417). Si las editas, cuenta antes.

Debajo de la condición hay un campo **Frases de Ejemplo**: son frases que **dispararían** la
transferencia. Sirven para descargar la condición de casuística — las de abajo ya vienen
elegidas. Ojo: van solo frases que **sí** deben transferir, nunca contraejemplos.

---

## ⚠️ Antes de configurar: el bloqueante

La acción **Contact Info solo rellena campos VACÍOS, no sobrescribe.**

Sin resolver eso, el cross-transfer nace roto: un lead le dice "melamina" a BOT-01, cambia a
AutoCAD, pasa a BOT-02, BOT-02 intenta escribir `Curso de interés = AutoCAD`, el campo **ya
dice "Melamina"** → se queda en Melamina → **SP05 le manda la ficha equivocada** y SP06 lo
califica con el curso de la otra familia.

Por eso existe **`WF-SWITCH | Limpiar interés al cambiar de familia`**
(`f72ee2f3-e29d-4894-883b-2aae4a7005a8`, draft, carpeta 01). Vacía los 10 campos de interés
—`Familia`, `Modalidad`, `Sede`, `Pack x2`, sus 4 gemelos `(bot)`, `Curso` y `Horario`— con la
acción **Borrar datos de campo**, para que el bot receptor arranque limpio. **No toca** nombre,
teléfono, correo ni la atribución de Meta.

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
lee "melamina" y lo devuelve a BOT-01, y así. Por eso las condiciones de ese par llevan un
`Ojo:` que separa por **intención** (¿hacerlo con sus manos o dirigir a otros?), nunca por la
palabra suelta.

---
---

# BOT-01 · Talleres Prácticos

**Actions → + Setup Your Actions → Transfer Bot** → `Nueva transferencia de bot` (dos veces).
`Enable Scenario` = **ON** en los dos.

## Escenario A — hacia Software

| Campo | Valor |
|---|---|
| Nombre de la acción | `Transfer a Software` |
| Seleccione el bot al que desea transferir | **BOT-02 Software GALK** |

**Condición de activación** · 337 car.
```
La persona deja los talleres y ahora quiere aprender un programa de diseño: SketchUp, renders, Revit, BIM, AutoCAD, planos 2D o diseño de mobiliario. Transfiere solo si abandona el interés anterior. Si solo lo menciona, compara o pregunta si existe, confírmale que sí y sigue con tu tema. No devuelvas a la persona al bot que te la pasó.
```

**Frases de Ejemplo**
```
mejor quiero aprender AutoCAD
cambié de opinión, me interesa Revit
ya no el taller, quiero el de SketchUp
quiero el curso de renders
```

## Escenario B — hacia Gestión

| Campo | Valor |
|---|---|
| Nombre de la acción | `Transfer a Gestión` |
| Seleccione el bot al que desea transferir | **BOT-03 Gestión GALK** |

**Condición de activación** · 417 car.
```
La persona deja el taller práctico y ahora quiere dirigir proyectos, no fabricar con sus manos: cocinas, obra interiorista, espacios comerciales o supervisión de melamina. Ojo: si quiere aprender a fabricar muebles de melamina, se queda contigo. Transfiere solo si abandona el interés anterior; si solo lo menciona o compara, confírmale que existe y sigue con tu tema. No devuelvas a la persona al bot que te la pasó.
```

**Frases de Ejemplo**
```
mejor quiero el de gestión de cocinas
ya no el taller, quiero supervisar proyectos
me interesa obra interiorista
quiero el curso de espacios comerciales
```

---

# BOT-02 · Software y Diseño

## Escenario A — hacia Talleres

| Campo | Valor |
|---|---|
| Nombre de la acción | `Transfer a Talleres` |
| Seleccione el bot al que desea transferir | **BOT-01 Talleres GALK** |

**Condición de activación** · 357 car.
```
La persona deja los cursos de software y ahora quiere un taller práctico presencial, con herramientas y materiales incluidos: melamina, drywall, electricidad o domótica. Transfiere solo si abandona el interés anterior. Si solo lo menciona, compara o pregunta si existe, confírmale que sí y sigue con tu tema. No devuelvas a la persona al bot que te la pasó.
```

**Frases de Ejemplo**
```
mejor quiero el taller de melamina
ya no, prefiero algo presencial con herramientas
quiero aprender drywall
me interesa el de electricidad
```

## Escenario B — hacia Gestión

| Campo | Valor |
|---|---|
| Nombre de la acción | `Transfer a Gestión` |
| Seleccione el bot al que desea transferir | **BOT-03 Gestión GALK** |

**Condición de activación** · 337 car.
```
La persona deja el software y ahora quiere gestionar o dirigir proyectos: cocinas, obra interiorista, espacios comerciales o supervisión de melamina. Transfiere solo si abandona el interés anterior. Si solo lo menciona, compara o pregunta si existe, confírmale que sí y sigue con tu tema. No devuelvas a la persona al bot que te la pasó.
```

**Frases de Ejemplo**
```
mejor quiero el de gestión de cocinas
me interesa obra interiorista
quiero el de espacios comerciales
ya no el software, quiero supervisión de melamina
```

---

# BOT-03 · Gestión de Proyectos

## Escenario A — hacia Talleres

| Campo | Valor |
|---|---|
| Nombre de la acción | `Transfer a Talleres` |
| Seleccione el bot al que desea transferir | **BOT-01 Talleres GALK** |

**Condición de activación** · 411 car.
```
La persona deja los cursos de gestión y ahora quiere un taller práctico presencial, para trabajar con sus propias manos: melamina, drywall, electricidad o domótica. Ojo: si quiere dirigir el proyecto y supervisar a otros, se queda contigo. Transfiere solo si abandona el interés anterior; si solo lo menciona o compara, confírmale que existe y sigue con tu tema. No devuelvas a la persona al bot que te la pasó.
```

**Frases de Ejemplo**
```
mejor quiero el taller de melamina
quiero aprender a fabricar muebles con mis manos
me interesa drywall
quiero el de electricidad
```

## Escenario B — hacia Software

| Campo | Valor |
|---|---|
| Nombre de la acción | `Transfer a Software` |
| Seleccione el bot al que desea transferir | **BOT-02 Software GALK** |

**Condición de activación** · 346 car.
```
La persona deja los cursos de gestión y ahora quiere aprender un programa de diseño: SketchUp, renders, Revit, BIM, AutoCAD, planos 2D o diseño de mobiliario. Transfiere solo si abandona el interés anterior. Si solo lo menciona, compara o pregunta si existe, confírmale que sí y sigue con tu tema. No devuelvas a la persona al bot que te la pasó.
```

**Frases de Ejemplo**
```
mejor quiero aprender SketchUp
me interesa AutoCAD
quiero el de Revit
ya no gestión, quiero hacer renders
```

---
---

## La acción que acompaña — en los 3 bots

**Actions → + Setup Your Actions → Trigger a Workflow**

| Campo | Valor |
|---|---|
| Nombre de la acción | `Limpiar interés al cambiar de familia` |
| Workflow a disparar | `WF-SWITCH | Limpiar interés al cambiar de familia` |

**Cuándo ejecutar** · 250 car.
```
Justo antes de transferir a la persona a otro asesor especialista porque cambió de familia de curso. Ejecuta esto primero y transfiere después. No lo ejecutes si la persona sigue en el mismo tipo de curso, ni cuando la transfieres a un asesor humano.
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

Esto no tiene límite de caracteres — el prompt es texto libre. Por eso la casuística larga vive
aquí y la condición del transfer se queda corta.

---

## Orden de armado

1. Los 3 bots creados y con sus prompts (si no, el desplegable de *Seleccione el bot al que
   desea transferir* sale vacío).
2. `Trigger a Workflow → WF-SWITCH` en los 3.
3. Los 6 escenarios de Transfer Bot con sus frases de ejemplo.
4. QA de los 3 puntos de arriba, con foco en el ping-pong BOT-01 ↔ BOT-03.

> Las 3 condiciones de **BOT-00** ya estaban dentro del límite (109, 115 y 144 caracteres) —
> no hay que tocarlas. Pero conviene agregarles también sus Frases de Ejemplo.
