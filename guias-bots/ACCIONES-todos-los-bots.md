# Acciones de los 4 bots — todos los campos listos para copiar y pegar

> Cada acción de Conversation AI pide siempre lo mismo:
> **Nombre de la acción** · **Qué actualizar / a qué bot** · **Pregunta a formular** ·
> **Cuándo ejecutar (condición)** · **Ejemplos**.
> Aquí está todo relleno. Copia el texto de cada renglón tal cual.

---

## ⚠️ 3 reglas del panel que hay que tener presentes

1. **Contact Info solo rellena campos VACÍOS.** No sobrescribe. Si un campo ya trae valor
   (p. ej. `Curso de interés` que puso BOT-00), el bot especialista **no lo va a corregir**.
   Por eso BOT-00 captura lo mínimo y el resto lo capturan los especialistas.
2. **Nombre, correo y teléfono NO se capturan con Contact Info.** Lo dice el propio panel:
   se piden en el prompt y GHL los guarda solo. Contact Info es únicamente para campos custom.
3. **Los textos de "Cuándo ejecutar" y "Ejemplos" son lenguaje natural**, no fórmulas.
   El modelo los interpreta — por eso conviene usar las mismas palabras del prompt.

---
---

# BOT-00 · Secretaria (Router)

## Acción 1 — Contact Info · Familia de interés

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar familia de interés` |
| **Qué campo de contacto se actualizará** | `Familia de interés` |
| **Qué actualizar en el campo** | `La familia de cursos que le interesa a la persona. Guarda EXACTAMENTE una de estas tres palabras, sin ninguna otra: Talleres, Software, Gestion. Usa "Talleres" para melamina, drywall, electricidad o domótica. Usa "Software" para SketchUp, Revit, AutoCAD o diseño de mobiliario. Usa "Gestion" (sin tilde) para cocinas, obra interiorista, espacios comerciales o supervisión de melamina.` |
| **Pregunta a formular** | `¿Qué curso o tema te interesa? 😊` |
| **Cuándo ejecutar** | `Apenas quede claro a qué familia de cursos pertenece el interés de la persona, ya sea porque lo dijo directamente o porque eligió una de las tres opciones.` |

**Ejemplos** (uno por línea, si el panel los pide sueltos):
```
"quiero información del curso de melamina" → Talleres
"cuánto dura el taller de drywall" → Talleres
"me interesa electricidad y domótica" → Talleres
"quiero aprender sketchup" → Software
"el curso de autocad está disponible?" → Software
"quiero hacer renders en revit" → Software
"me interesa el curso de cocinas" → Gestion
"quiero llevar interiorismo" → Gestion
"el de supervisión de melamina" → Gestion
```

> ⚠️ El valor debe quedar exacto (`Talleres` / `Software` / `Gestion`) o los Transfer Bot no matchean.

## Acción 2 — Contact Info · Curso de interés (opcional)

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar curso puntual` |
| **Qué campo de contacto se actualizará** | `Curso de interés` |
| **Qué actualizar en el campo** | `El nombre del curso concreto que mencionó la persona, tal como se llama en GALK. Por ejemplo: Melamina Desde Cero, Drywall Avanzado, Electricidad y Domótica, SketchUp, Revit BIM, AutoCAD, Diseño de Mobiliario, Cocinas, Obra Interiorista, Espacios Comerciales, Supervisión de Melamina. Si la persona no nombró un curso específico, deja el campo vacío.` |
| **Pregunta a formular** | *(dejar vacío — no se pregunta, se deduce del mensaje)* |
| **Cuándo ejecutar** | `Solo cuando la persona menciona un curso específico por su nombre. Si únicamente habla del área general, no ejecutes esta acción.` |

**Ejemplos:**
```
"quiero el de melamina desde cero" → Melamina Desde Cero
"me interesa drywall avanzado" → Drywall Avanzado
"quiero llevar autocad" → AutoCAD
"quiero un curso de diseño" → (no ejecutar, es genérico)
```

## Acción 3 — Transfer Bot · Talleres

| Campo del panel | Qué poner |
|---|---|
| **Enable Scenario** | ON |
| **Nombre de la acción** | `Transferir a Talleres` |
| **Select Bot to Transfer to** | `BOT-01 Talleres GALK` |
| **Trigger Condition / Cuándo ejecutar** | `Cuando el interés de la persona es un taller práctico presencial: melamina, drywall, electricidad o domótica. Transfiere apenas tengas identificada la familia, sin dar precios ni horarios.` |

**Ejemplos:**
```
"quiero el taller de melamina"
"cuánto cuesta drywall" (transfiere, no cotices)
"hacen cursos de electricidad?"
"quiero aprender a hacer muebles"
```

## Acción 4 — Transfer Bot · Software

| Campo del panel | Qué poner |
|---|---|
| **Enable Scenario** | ON |
| **Nombre de la acción** | `Transferir a Software` |
| **Select Bot to Transfer to** | `BOT-02 Software GALK` |
| **Trigger Condition / Cuándo ejecutar** | `Cuando el interés de la persona es un curso de software de diseño: SketchUp, Revit BIM, AutoCAD o diseño de mobiliario. Transfiere apenas tengas identificada la familia.` |

**Ejemplos:**
```
"quiero aprender sketchup"
"tienen curso de autocad?"
"quiero hacer planos en 3d"
"el curso de revit es online?"
```

## Acción 5 — Transfer Bot · Gestión

| Campo del panel | Qué poner |
|---|---|
| **Enable Scenario** | ON |
| **Nombre de la acción** | `Transferir a Gestión` |
| **Select Bot to Transfer to** | `BOT-03 Gestión GALK` |
| **Trigger Condition / Cuándo ejecutar** | `Cuando el interés de la persona es un curso de gestión de proyectos: cocinas, obra interiorista, espacios comerciales o supervisión de melamina. Transfiere apenas tengas identificada la familia.` |

**Ejemplos:**
```
"quiero el curso de cocinas"
"me interesa interiorismo"
"tienen algo de espacios comerciales?"
"quiero aprender a supervisar obras"
```

## Acción 6 — Human Handover

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Pasar a asesor humano` |
| **Trigger Condition / Cuándo ejecutar** | `Cuando la persona pide expresamente hablar con un humano o un asesor, cuando se muestra molesta o frustrada, cuando hace un reclamo, o cuando pregunta algo que no sabes responder y no corresponde a ninguna de las tres familias de cursos.` |
| **Asignar a** | Supervisora **Lucía Galvez** |

**Ejemplos:**
```
"quiero hablar con una persona"
"me puedes pasar con un asesor?"
"esto es un robot? necesito ayuda real"
"ya les escribí y nadie me responde"
"quiero un reembolso"
```

## Acción 7 — Auto Followup

| Toque | Espera | Mensaje |
|---|---|---|
| 1 | 2 horas | `¿Seguimos? 😊 Cuéntame qué curso estabas viendo y te paso con el asesor indicado.` |
| 2 | +4 horas | *(ver bloque abajo)* |
| 3 | +8 horas | `Te dejo la puerta abierta 🙌 Cuando quieras retomamos, escríbeme por aquí nomás.` |

Toque 2:
```
Te dejo las 3 áreas por si te ayuda a decidir 👇
🔨 Talleres prácticos (melamina, drywall, electricidad)
💻 Software y diseño (SketchUp, Revit, AutoCAD)
📋 Gestión de proyectos (cocinas, interiorismo)
¿Cuál te llama más?
```

**Cuándo ejecutar:** `Cuando la persona deja de responder y todavía no se ha identificado su familia de curso ni ha sido transferida a un especialista.`

---
---

# BOT-01 · Talleres Prácticos

## Acción 1 — Contact Info · Curso de interés

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar curso` |
| **Qué campo de contacto se actualizará** | `Curso de interés` |
| **Qué actualizar en el campo** | `El taller que quiere llevar la persona. Guarda exactamente uno de estos: Melamina Desde Cero, Melamina Avanzado, Drywall Desde Cero, Drywall Avanzado, Electricidad y Domótica.` |
| **Pregunta a formular** | `¿Cuál de nuestros talleres te interesa? 🔨\n1️⃣ Melamina (desde cero o avanzado)\n2️⃣ Drywall (desde cero o avanzado)\n3️⃣ Electricidad y Domótica` |
| **Cuándo ejecutar** | `Cuando la persona indica cuál de los talleres quiere llevar. Si ya venía identificado desde el bot anterior, no vuelvas a preguntar.` |

**Ejemplos:**
```
"quiero melamina desde cero" → Melamina Desde Cero
"el avanzado de melamina" → Melamina Avanzado
"drywall básico" → Drywall Desde Cero
"quiero el de electricidad" → Electricidad y Domótica
```

## Acción 2 — Contact Info · Sede

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar sede` |
| **Qué campo de contacto se actualizará** | `Sede` |
| **Qué actualizar en el campo** | `La sede donde quiere llevar el taller. Guarda exactamente una de estas: Surco, Los Olivos, Arequipa.` |
| **Pregunta a formular** | `📍 ¿Qué sede te queda mejor?\n🔴 Lima: Surco o Los Olivos\n🔴 Arequipa` |
| **Cuándo ejecutar** | `Después de saber qué taller quiere y antes de enviarle la ficha.` |

**Ejemplos:**
```
"en surco" → Surco
"me queda mejor los olivos" → Los Olivos
"estoy en arequipa" → Arequipa
"en lima" → (repreguntar: ¿Surco o Los Olivos?)
```

## Acción 3 — Contact Info · Modalidad

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Fijar modalidad presencial` |
| **Qué campo de contacto se actualizará** | `Modalidad` |
| **Qué actualizar en el campo** | `Siempre guarda el valor: Presencial. Todos los talleres prácticos de esta área son presenciales.` |
| **Pregunta a formular** | *(vacío — no se pregunta)* |
| **Cuándo ejecutar** | `Apenas se confirme que el interés es un taller práctico. No preguntes, guarda Presencial directamente.` |

## Acción 4 — Contact Info · Horario de interés

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar horario` |
| **Qué campo de contacto se actualizará** | `Horario de interés` |
| **Qué actualizar en el campo** | `El horario o turno que eligió la persona de la ficha de horarios que recibió. Guarda el día y el turno tal como lo dijo, por ejemplo: "sábados mañana", "lunes y miércoles noche", "domingos tarde".` |
| **Pregunta a formular** | `¿Cuál de esos horarios te acomoda mejor? 🕐` |
| **Cuándo ejecutar** | `Solo DESPUÉS de que la persona recibió la ficha con los horarios. Nunca antes, porque los horarios cambian cada semana y no los conoces.` |

**Ejemplos:**
```
"los sábados en la mañana" → sábados mañana
"prefiero de noche entre semana" → entre semana noche
"el domingo" → domingos
```

## Acción 5 — Contact Info · Pack x2

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar interés en Pack x2` |
| **Qué campo de contacto se actualizará** | `Pack x2` |
| **Qué actualizar en el campo** | `Si la persona aceptó o mostró interés en llevar el pack de dos niveles (Desde Cero + Avanzado), guarda: Sí. Si lo rechazó, guarda: No.` |
| **Pregunta a formular** | `🎁 Tenemos un pack: Desde Cero + Avanzado del mismo taller por S/890 (reservas con S/200). ¿Te interesa?` |
| **Cuándo ejecutar** | `Solo si la sede es Surco o Los Olivos (Lima) Y el curso tiene versión avanzada (melamina o drywall). NUNCA lo ofrezcas si la sede es Arequipa: ahí no existe el pack.` |

**Ejemplos:**
```
"sí me interesa el pack" → Sí
"cuánto sale llevando los dos?" → Sí
"no, solo el básico" → No
```

## Acción 6 — Trigger a Workflow · SP05 (enviar ficha)

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Enviar ficha del curso` |
| **Workflow a disparar** | `SP05 | Envío de ficha (árbol 24 ramas)` |
| **Cuándo ejecutar** | `Cuando ya tengas guardados el curso Y la sede de la persona. Dispara este workflow para que le llegue la ficha con la información y los horarios del curso en su sede.` |

**Ejemplos:**
```
Ya sé que quiere "Melamina Desde Cero" en "Surco" → ejecutar
Sé el curso pero no la sede → NO ejecutar todavía
```

## Acción 7 — Trigger a Workflow · SP06 (calificado)

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Marcar lead calificado` |
| **Workflow a disparar** | `SP06 | Calificación y asignación` |
| **Cuándo ejecutar** | `Solo cuando los CUATRO datos estén guardados: curso, modalidad, sede y horario de interés. Si falta alguno, no ejecutes: sigue conversando hasta completarlos.` |

**Ejemplos:**
```
curso ✅ modalidad ✅ sede ✅ horario ✅ → ejecutar
curso ✅ sede ✅ pero sin horario → NO ejecutar
```

## Acción 8 — Human Handover

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Pasar a asesor humano` |
| **Trigger Condition / Cuándo ejecutar** | `Cuando la persona pide hablar con un humano, se muestra molesta, hace un reclamo, pide una excepción de precio o descuento que no está en tu información, o pregunta algo que no puedes responder con tu base de conocimiento.` |

**Ejemplos:**
```
"me pueden hacer un descuento especial?"
"quiero hablar con alguien"
"puedo pagar en cuotas?"
"necesito factura a nombre de mi empresa"
```

## Acción 9 — Auto Followup

| Toque | Espera | Mensaje |
|---|---|---|
| 1 | 2 horas | `¿Seguimos? 😊 ¿Te ayudo a elegir la sede o el horario del taller?` |
| 2 | +4 horas | `Los cupos de los talleres se llenan rápido 🔨 ¿Te reservo un lugar para conversarlo con un asesor?` |
| 3 | +8 horas | `Te dejo la info a la mano 🙌 Cuando quieras retomamos, escríbeme por aquí.` |

**Cuándo ejecutar:** `Cuando la persona deja de responder antes de completar los cuatro datos de calificación.`

---
---

# BOT-02 · Software y Diseño

## Acción 1 — Contact Info · Curso de interés

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar curso` |
| **Qué campo de contacto se actualizará** | `Curso de interés` |
| **Qué actualizar en el campo** | `El curso de software que quiere llevar. Guarda exactamente uno de estos: SketchUp, Revit BIM, Diseño de Mobiliario, AutoCAD.` |
| **Pregunta a formular** | `¿Cuál te interesa? 💻\n🏠 SketchUp + Render\n🏗️ Revit BIM\n🪑 Diseño de Mobiliario\n📐 AutoCAD` |
| **Cuándo ejecutar** | `Cuando la persona indica cuál de los cuatro cursos quiere. Si ya venía identificado del bot anterior, no repreguntes.` |

**Ejemplos:**
```
"sketchup" → SketchUp
"quiero revit" → Revit BIM
"el de muebles" → Diseño de Mobiliario
"autocad porfa" → AutoCAD
```

## Acción 2 — Contact Info · Modalidad

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar modalidad` |
| **Qué campo de contacto se actualizará** | `Modalidad` |
| **Qué actualizar en el campo** | `Cómo quiere llevar el curso. Guarda exactamente: Online o Presencial.` |
| **Pregunta a formular** | `¿Cómo prefieres llevarlo?\n💻 Online en vivo por Zoom\n📍 Presencial en Surco` |
| **Cuándo ejecutar** | `Pregunta la modalidad SOLO si el curso es SketchUp o Revit BIM, que son los únicos que tienen ambas opciones. Si el curso es Diseño de Mobiliario o AutoCAD, guarda Online directamente sin preguntar, porque solo existen online.` |

**Ejemplos:**
```
"online" → Online
"prefiero presencial" → Presencial
curso = AutoCAD → Online (sin preguntar)
curso = Diseño de Mobiliario → Online (sin preguntar)
```

## Acción 3 — Contact Info · Sede

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Fijar sede` |
| **Qué campo de contacto se actualizará** | `Sede` |
| **Qué actualizar en el campo** | `Si la modalidad es Presencial, guarda: Surco (es la única sede para cursos de software). Si la modalidad es Online, guarda: No aplica.` |
| **Pregunta a formular** | *(vacío — no se pregunta)* |
| **Cuándo ejecutar** | `Apenas quede definida la modalidad. No preguntes por la sede: se deduce de la modalidad.` |

## Acción 4 — Contact Info · Horario de interés

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar horario` |
| **Qué campo de contacto se actualizará** | `Horario de interés` |
| **Qué actualizar en el campo** | `El horario o turno que eligió la persona de la ficha que recibió. Guarda día y turno tal como lo dijo.` |
| **Pregunta a formular** | `¿Cuál de esos horarios te acomoda mejor? 🕐` |
| **Cuándo ejecutar** | `Solo DESPUÉS de que la persona recibió la ficha con los horarios.` |

## Acción 5 — Trigger a Workflow · SP05 (enviar ficha)

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Enviar ficha del curso` |
| **Workflow a disparar** | `SP05 | Envío de ficha (árbol 24 ramas)` |
| **Cuándo ejecutar** | `Cuando ya tengas guardados el curso Y la modalidad. Con esos dos datos la ficha que se envía es la correcta (el precio cambia entre online y presencial).` |

## Acción 6 — Trigger a Workflow · SP06 (calificado)

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Marcar lead calificado` |
| **Workflow a disparar** | `SP06 | Calificación y asignación` |
| **Cuándo ejecutar** | `Solo cuando los cuatro datos estén guardados: curso, modalidad, sede y horario de interés.` |

## Acción 7 — Human Handover

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Pasar a asesor humano` |
| **Trigger Condition / Cuándo ejecutar** | `Cuando la persona pide hablar con un humano, se muestra molesta, hace un reclamo, pide un descuento o forma de pago especial, o pregunta detalles técnicos que no están en tu base de conocimiento.` |

**Ejemplos:**
```
"puedo pagar en partes?"
"necesito el temario completo del curso"
"quiero hablar con un asesor"
"mi laptop aguanta el programa?"
```

## Acción 8 — Auto Followup

| Toque | Espera | Mensaje |
|---|---|---|
| 1 | 2 horas | `¿Seguimos? 😊 ¿Te cuento más del curso o prefieres ver los horarios?` |
| 2 | +4 horas | `Recuerda que el precio de preventa es por tiempo limitado 💻 ¿Te interesa asegurar tu cupo?` |
| 3 | +8 horas | `Te dejo la info a la mano 🙌 Cuando quieras retomamos.` |

---
---

# BOT-03 · Gestión de Proyectos

## Acción 1 — Contact Info · Curso de interés

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar curso` |
| **Qué campo de contacto se actualizará** | `Curso de interés` |
| **Qué actualizar en el campo** | `El curso de gestión que quiere llevar. Guarda exactamente uno de estos: Cocinas, Obra Interiorista, Espacios Comerciales, Supervisión de Melamina.` |
| **Pregunta a formular** | `¿Cuál te interesa? 📋\n🍳 Cocinas\n🏡 Obra Interiorista\n🏬 Espacios Comerciales\n📊 Supervisión de Melamina` |
| **Cuándo ejecutar** | `Cuando la persona indica cuál de los cuatro cursos quiere. Si ya venía identificado del bot anterior, no repreguntes.` |

**Ejemplos:**
```
"cocinas" → Cocinas
"el de interiorismo" → Obra Interiorista
"espacios comerciales" → Espacios Comerciales
"supervisión" → Supervisión de Melamina
```

## Acción 2 — Contact Info · Modalidad y Sede (automáticas)

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Fijar modalidad online` |
| **Qué campo de contacto se actualizará** | `Modalidad` |
| **Qué actualizar en el campo** | `Siempre guarda: Online. Todos los cursos de gestión son online en vivo por Zoom.` |
| **Pregunta a formular** | *(vacío)* |
| **Cuándo ejecutar** | `Apenas se confirme que el interés es un curso de gestión. No preguntes.` |

Añade un **segundo campo** con `+ Añadir nuevo campo`:

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Fijar sede no aplica` |
| **Qué campo de contacto se actualizará** | `Sede` |
| **Qué actualizar en el campo** | `Siempre guarda: No aplica. Estos cursos no tienen sede física.` |
| **Cuándo ejecutar** | `Junto con la modalidad, sin preguntar.` |

## Acción 3 — Contact Info · Horario de interés

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Capturar horario` |
| **Qué campo de contacto se actualizará** | `Horario de interés` |
| **Qué actualizar en el campo** | `El horario o turno que eligió la persona de la ficha que recibió. Guarda día y turno tal como lo dijo.` |
| **Pregunta a formular** | `¿Cuál de esos horarios te acomoda mejor? 🕐` |
| **Cuándo ejecutar** | `Solo DESPUÉS de que la persona recibió la ficha con los horarios.` |

## Acción 4 — Trigger a Workflow · SP05 (enviar ficha)

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Enviar ficha del curso` |
| **Workflow a disparar** | `SP05 | Envío de ficha (árbol 24 ramas)` |
| **Cuándo ejecutar** | `Apenas tengas guardado el curso. Como todos son online, no necesitas más datos para saber qué ficha enviar.` |

## Acción 5 — Trigger a Workflow · SP06 (calificado)

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Marcar lead calificado` |
| **Workflow a disparar** | `SP06 | Calificación y asignación` |
| **Cuándo ejecutar** | `Cuando estén guardados el curso y el horario de interés (modalidad y sede se llenan solas).` |

## Acción 6 — Human Handover

| Campo del panel | Qué poner |
|---|---|
| **Nombre de la acción** | `Pasar a asesor humano` |
| **Trigger Condition / Cuándo ejecutar** | `Cuando la persona pide hablar con un humano, se muestra molesta, hace un reclamo, pide descuento o forma de pago especial, o pregunta por el temario o la certificación en detalle.` |

## Acción 7 — Auto Followup

| Toque | Espera | Mensaje |
|---|---|---|
| 1 | 2 horas | `¿Seguimos? 😊 ¿Te muestro los horarios del curso?` |
| 2 | +4 horas | `Las clases son online en vivo, así que puedes llevarlas desde donde estés 📋 ¿Te interesa?` |
| 3 | +8 horas | `Te dejo la info a la mano 🙌 Cuando quieras retomamos.` |

---
---

## Tabla resumen — quién captura qué

| Campo | BOT-00 | BOT-01 Talleres | BOT-02 Software | BOT-03 Gestión |
|---|---|---|---|---|
| Nombre | *en el prompt* | — | — | — |
| Familia de interés | ✅ | — | — | — |
| Curso de interés | opcional | ✅ | ✅ | ✅ |
| Modalidad | — | auto `Presencial` | ✅ pregunta (G1/G4) | auto `Online` |
| Sede | — | ✅ pregunta | auto (Surco/No aplica) | auto `No aplica` |
| Horario de interés | — | ✅ | ✅ | ✅ |
| Pack x2 | — | ✅ solo Lima | — | — |

> Recuerda: **Contact Info solo llena campos vacíos**. Si BOT-00 ya guardó `Curso de interés`,
> el especialista no lo va a poder corregir — por eso BOT-00 solo lo guarda cuando la persona
> nombró el curso de forma explícita.
