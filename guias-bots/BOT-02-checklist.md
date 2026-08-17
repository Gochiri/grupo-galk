# BOT-02 · Software y Diseño — qué falta para dejarlo como talleres

> Talleres quedó cerrado el 17-ago. Esta es la misma lista, adaptada. El orden importa:
> el paso 1 es bloqueante y sin él nada de lo demás se nota.

---

## 1. Publicar **WF-SEDE** ← bloqueante, empieza por aquí

`WF-SEDE | Sede No aplica cuando es online` · `35977571-c05a-40a8-a1a5-391f114e4d5e`
Está en **draft**, en la carpeta *01 Setup y Normalización*.

**Por qué existe.** La guarda de SP06 exige los tres campos: Curso, Modalidad y Sede. En talleres
siempre hay sede porque son presenciales — por eso talleres funcionó. Pero en **software online y
en todo gestión no hay sede que capturar**: el lead nunca va a decir "no aplica", *Contact Info*
no tiene nada que extraer y `Sede` se queda vacía para siempre.

Sin esto, **ningún lead de software online ni de gestión llega jamás al asesor**. SP06 los corta
en la guarda, en silencio. Es el mismo agujero que tenía `Modalidad` antes de WF-MOD.

Lo que hace: si `Modalidad` = Online y `Sede` está vacía → escribe **No aplica**. La condición de
"vacía" evita pisar una sede real si alguien cambia de presencial a online.

⚠️ Al publicarlo, **activa también su trigger** (`Modalidad definida`). Se creó inactivo a
propósito, porque mandar `active: true` por API publica el workflow sin querer.

La cadena queda así:

```
Curso de interés  →  WF-MOD   →  Modalidad = Online
                             →  WF-SEDE  →  Sede = No aplica
                                         →  SP06 ya tiene los tres → califica
```

---

## 2. Las DOS acciones que NO se crean ← esto es lo que borraste en BOT-01

Las anoto porque es exactamente lo que preguntaste. En BOT-01 existían y las quitamos:

| Acción | Apuntaba a | Por qué se quitó |
|---|---|---|
| **Marcar lead calificado** | *Trigger a Workflow* → SP06 | El bot la disparaba en el mismo turno en que se extraían los datos, así que llegaba antes de que el campo se escribiera. SP06 entraba, la guarda cortaba y nadie reintentaba: **el lead se perdía**. |
| **Enviar ficha del curso** | *Trigger a Workflow* → SP05 | Lo mismo, con la ficha. |

**En BOT-02 no las crees.** SP05 y SP06 ya entran solos por los tres campos canónicos
(`Curso de interés`, `Modalidad`, `Sede`), que es lo que arregló todo en talleres: entra por los
datos, no por la opinión del bot.

Si BOT-02 ya las tiene creadas de antes, **bórralas**.

---

## 3. Prompt

`guias-bots/PROMPTS-bots-v3.md`, bloque **BOT-02** — 666 palabras, tope 2000.
Se pega completo en **Build**, borrando lo que haya.

Lleva la compuerta de cierre, el "tú eres el especialista", los precios embebidos y la regla de
duración (POR CONFIRMAR en los 4 cursos, nunca inventar horas ni sesiones).

---

## 4. Action **Contact Info** — 3 campos

Los mismos tres de talleres. Las descripciones van en *Qué actualizar en el campo*, y las tres
entran de sobra en el tope de 500:

**`Curso de interés`** — 258 caracteres
```
El curso de software que quiere la persona. Escribe exactamente uno de estos cuatro: SketchUp + Render, Revit BIM, Diseño de Mobiliario, AutoCAD. No lo abrevies ni escribas solo una parte del nombre. Si todavía no está claro cuál quiere, deja el campo vacío.
```

**`Modalidad (bot)`** — 256 caracteres
```
Escribe exactamente Online o Presencial. Solo SketchUp + Render y Revit BIM tienen presencial, y únicamente en Surco. Diseño de Mobiliario y AutoCAD son siempre Online. Si el curso tiene las dos opciones y la persona todavía no eligió, deja el campo vacío.
```

**`Sede (bot)`** — 212 caracteres
```
Escribe exactamente Surco si la persona eligió presencial. Si eligió online, deja el campo vacío: el sistema lo completa solo. La única sede presencial de software es Surco; nunca escribas Los Olivos ni Arequipa.
```

> Ojo con `Sede (bot)`: **para online se deja vacío a propósito.** Quien pone el "No aplica" es
> WF-SEDE, sobre el campo canónico. Si el bot escribiera "No aplica" en el gemelo de texto,
> dependeríamos de que WF-NORM-3 tenga una rama para ese valor — y así no hace falta.

---

## 5. Transfer Bot — los 2 cruces de BOT-02

De `guias-bots/CROSS-TRANSFERS-especialistas.md`: **BOT-02 → BOT-01** y **BOT-02 → BOT-03**.
Recuerda el tope de **10–500 caracteres** en la *Condición de activación*; la casuística larga va
en *Frases de Ejemplo*.

---

## 6. Lo demás, igual que BOT-01

- **Human Handover** con su condición de escape.
- **Timing & Pacing**: los dos toggles de *sleep* (Manual Message y Workflow Message) en **ON**.
  Son la pieza que evita que el bot y los workflows se pisen.
- **Response Behavior**: los tres en OFF.
- **Subir `knowledge-base/KB-BOT-02-software.md`**.

---

## 7. La prueba — dos casos, no uno

Contacto **nuevo**, usuario asignado a mano (lo pide el plugin de SMS) y tag `equipo-interno`.

### Caso A · AutoCAD — es el que estrena WF-SEDE

```
hola, quiero info del curso de autocad
```
El bot debe presentar el curso, confirmar que es online sin preguntar la modalidad, y dar el
precio de preventa después de presentar. Al final, en el contacto:

```
Curso de interés = AutoCAD
Modalidad        = Online       ← lo pone WF-MOD
Sede             = No aplica    ← lo pone WF-SEDE
Calificado       = Sí
tags: ficha-enviada · bot-silenciado
```

### Caso B · SketchUp presencial

```
hola, quiero info de sketchup   →   presencial
```
Debe preguntar la modalidad (porque SketchUp tiene las dos) y dar S/1100 / preventa S/550, no el
precio de online. Al final:

```
Curso de interés = SketchUp + Render
Modalidad        = Presencial
Sede             = Surco
```

### Prueba de esquive, en cualquiera de los dos

Contesta solo con preguntas y no le des nunca la modalidad. **No se debe despedir** ni decir que
un asesor te va a contactar. Si lo hace, la compuerta de cierre no quedó pegada.

### Y lo que no prueba la pantalla

Los tres campos y los tags se verifican **por API**, no en el panel. Que el asesor reciba la
notificación tampoco prueba que fuera SP06: WF3 de Francisco avisa por su cuenta.

---

## 8. Lo que NO se puede cerrar todavía

La presentación de producto que pidió Lucía exige contar qué se aprende, y de los 4 cursos de
software la Knowledge Base tiene **una línea por curso y la duración en POR CONFIRMAR**. El prompt
está blindado para que no invente temario y derive si se lo piden, pero **la presentación va a
salir pobre comparada con la de talleres**. Falta el contenido real (ver `ACUERDOS §P3`).

Eso no bloquea la prueba técnica: los campos, los workflows y el cierre se validan igual.
