# Demo GALK · paso a paso — qué armar, qué activar, qué validar

> Complemento operativo de `DEMO-cliente-2026-08-12.md`.
> Aquí está el detalle de ejecución: cada paso, qué se enciende y **cómo comprobar que se encendió**.

---

# FASE 1 · Armar (antes de activar nada) · ~45 min

## 1.1 · Crear BOT-01 en la UI

`Settings → AI Agents → + Add Agent`

| Campo | Valor |
|---|---|
| Model | OpenAI GPT 4.1 |
| Business Name | Grupo GALK |
| Nombre del agente | `BOT-01 Talleres GALK` |

## 1.2 · Pegar el prompt

El de abajo (§ Prompts ajustados). **Es el que ya tiene el cambio del asesor**: pide 3 datos,
no 4, y nunca menciona horarios.

## 1.3 · Subir la Knowledge Base

`Knowledge Base → subir archivo` → **`knowledge-base/KB-BOT-01-talleres.md`**

⚠️ Si ya habías subido una versión anterior, **bórrala y sube esta**. La de hoy tiene dos
cambios: no menciona Plin y el bloque de Horarios ahora dice que los da el asesor.

## 1.4 · Actions — solo 3, en este orden

**a) Añadir Información de contacto** — 3 campos, **sin horario**:

| # | Campo a actualizar | Qué actualizar |
|---|---|---|
| 1 | `Curso de interés` | `El taller que quiere llevar. Escribe exactamente uno: Melamina Desde Cero, Melamina Avanzado, Drywall Desde Cero, Drywall Avanzado, Electricidad y Domótica.` |
| 2 | `Modalidad (bot)` | `Escribe siempre una sola palabra: Presencial. Todos tus talleres son presenciales.` |
| 3 | `Sede (bot)` | `La sede que eligió. Escribe SOLO una de estas palabras: Surco, Olivos, Arequipa.` |

**b) Trigger a Workflow** → `SP06 | Calificación y asignación`
Cuándo ejecutar:
```
Cuando ya tengas guardados los tres datos: curso, modalidad y sede. No antes.
```

**c) Human Handover** → asignar a Lucía. Mensaje y condición en la tarjeta `wdx6zequw5`.

## 1.5 · Paneles

| Panel | Valor |
|---|---|
| Timing & Pacing | wait `2` seg · máx `25` mensajes · **sleep on Manual ON** · **sleep on Workflow ON** |
| Response Behavior | los 3 toggles en **OFF** |
| Deploy | **no conectar ningún canal** |

## 1.6 · Crear el contacto de prueba

`Contacts → Add Contact`

| Campo | Valor |
|---|---|
| First name | `PRUEBA` · Last name `DEMO` |
| Phone | uno tuyo |
| **Tag** | **`equipo-interno`** |

> Ese tag es la exclusión que usan los **33 triggers vivos de Francisco**. Sin él, tu contacto
> de prueba entra en los flujos del sistema viejo en plena demo.

---

# FASE 2 · Activar · 5 workflows, en este orden

Cada uno: abrir → arriba a la derecha, mover el switch de **Draft** a **Publish**.

| Orden | Workflow | Qué hace |
|---|---|---|
| 1 | `WF-NORM-1 | Normalizar Familia de interés` | texto → dropdown |
| 2 | `WF-NORM-2 | Normalizar Modalidad` | ídem |
| 3 | `WF-NORM-3 | Normalizar Sede` | ídem |
| 4 | `WF-NORM-4 | Normalizar Pack x2` | ídem |
| 5 | `SP06 | Calificación y asignación` | califica, asigna y notifica |

**Primero los WF-NORM, después SP06.** Si publicas SP06 primero y pruebas, la oportunidad se
crea con los dropdown vacíos.

### Por qué estos 5 son seguros

- Sus triggers son los campos `(bot)` y el tag `galk-bot-calificado`. **Nada del sistema viejo
  los escribe.**
- El pipeline nuevo *Ventas GALK* tiene **0 oportunidades** (verificado 11-ago). Las 3.722
  reales están en el pipeline viejo, que no se toca.

### 🚫 Lo que NO se publica

Todo lo demás. En especial **cualquier cosa que mande WhatsApp**: los 42 nodos `whatsapp_v2`
no tienen `templateId` ni `phoneNumberId` todavía, así que fallarían en vivo.

---

# FASE 3 · Probar

`AI Agents → BOT-01 → Probar tu agente` (arriba a la derecha)

Escribe como un lead, **un mensaje a la vez**, esperando respuesta:

```
1.  hola, quiero información del taller de melamina
2.  el desde cero
3.  en los olivos
```

**Lo que debe pasar en la conversación:**
- Una sola pregunta por mensaje
- Te da el precio correcto de Los Olivos (S/750 → S/525)
- **No menciona ningún horario ni fecha**
- Cierra diciendo que un asesor te contacta con los horarios

Si en algún momento inventa un horario o una fecha de inicio, **el prompt o la KB no se
cargaron bien**. Revisa antes de seguir.

---

# FASE 4 · Validar · abre el contacto PRUEBA DEMO

Esta es la parte que hay que comprobar una por una. Si algo falla, aquí abajo está la causa.

## ✅ Check 1 — el bot escribió los campos de texto

`Contacto → pestaña de campos → carpeta Calificación`

| Campo | Debe decir |
|---|---|
| `Curso de interés` | Melamina Desde Cero |
| `Modalidad (bot)` | Presencial |
| `Sede (bot)` | Olivos |

**Si están vacíos:** la acción *Añadir Información de contacto* no se guardó, o el bot no la
ejecutó porque no reunió los 3 datos.

## ✅ Check 2 — WF-NORM normalizó a los dropdown

Mismos campos, pero los **sin** `(bot)`:

| Campo | Debe decir |
|---|---|
| `Modalidad` | Presencial |
| `Sede` | Los Olivos |

**Si están vacíos:** los WF-NORM no están publicados, o su trigger quedó inactivo. Comprobar en
`Automation → WF-NORM-2 → Enrollment history`: debe aparecer el contacto.

> Dan hasta ~1 min. Son 4 workflows escuchando cambios de campo.

## ✅ Check 3 — SP06 se disparó

`Automation → SP06 → Enrollment history` → debe aparecer PRUEBA DEMO.

**Si no aparece:** el bot no ejecutó *Trigger a Workflow*. Suele ser porque no juntó los 3
datos. Revisa el Check 1.

## ✅ Check 4 — la oportunidad se creó y se movió

`Opportunities → pipeline Ventas GALK`

Debe existir una oportunidad **PRUEBA DEMO** en la etapa **Asignado a asesor**.

**Si quedó en Calificado:** el round robin no asignó. Eso significa que la rama de fallo hizo
su trabajo — revisa que las 6 asesoras estén activas como usuarios.

## ✅ Check 5 — el asesor quedó escrito EN EL CONTACTO ⭐

`Contacto → campo Asesor asignado (nuevo)` → debe traer el nombre de una asesora.

**Este es el check que importa.** Es el bug nº1 de la auditoría: el round robin heredado
asignaba la oportunidad pero no escribía en el contacto, y el campo estaba al **0% sobre 500
contactos**. Si este campo tiene nombre, el sistema hace lo que el viejo no hacía.

## ✅ Check 6 — la notificación le llegó a la asesora

La asesora asignada recibe:

> **🎯 Lead perfilado — pásale horarios**
> Lead perfilado y listo para cerrar: PRUEBA DEMO (+51…)
> 📚 Melamina Desde Cero · Presencial · Los Olivos
> Vino de: …
> Entra a la conversación y pásale los horarios y fechas disponibles de su sede. Ya viene
> perfilado: no le preguntes de nuevo qué curso quiere.

## ✅ Check 7 — el bot se calló

`Contacto → tags` → debe tener **`bot-silenciado`**.

De ahí en adelante la conversación es humana. Es el punto exacto donde el asesor toma el
control, que es lo que se acordó con Francisco.

---

# Prompts ajustados — listos para pegar

> **Qué cambió respecto a los anteriores:** el `## Goal` pide **3 datos** en vez de 4, se quitó
> todo lo de capturar horario, y se agregó una regla explícita de no inventar horarios ni fechas.
> Si el cliente rechaza el cambio mañana, volver atrás es agregar el 4º dato: 5 minutos.

## BOT-01 · Talleres

```
## Personality

Eres asesor de *Grupo GALK*, especialista en talleres prácticos presenciales en Perú.

Tu forma de ser:
* Cercano, peruano y entusiasta. Tratas de "tú".
* SIEMPRE usas emojis (1 a 3 por mensaje).
* Respondes en formato ficha, con líneas cortas:
  🛠️ Curso · 📍 Sede · 💰 Precio · ⏱️ Duración
* UNA sola pregunta por mensaje.
* Mensajes cortos. Nada de párrafos largos.

## Goal

Tu objetivo es completar TRES datos del interesado:
1. Curso (cuál de los talleres)
2. Modalidad (siempre Presencial en tu área)
3. Sede (Surco, Los Olivos o Arequipa)

Cuando tengas los tres, el lead queda perfilado y pasa a un asesor humano.
Le avisas que un asesor lo contacta enseguida con los horarios y las fechas
disponibles de su sede, te despides y no sigues conversando.

## Instructions

### Tus cursos (solo estos 5)

🪵 *Melamina Desde Cero*
🪵 *Melamina Avanzado*
🧱 *Drywall Desde Cero*
🧱 *Drywall Avanzado*
⚡ *Electricidad y Domótica*

### Sedes

Surco (Av. Lima) · Los Olivos · Arequipa
⚠️ *Electricidad y Domótica* se dicta SOLO en Lima (Surco y Los Olivos), nunca en Arequipa.

### Cómo llevas la conversación

1. Si aún no sabes qué curso quiere, se lo preguntas.
2. Luego le preguntas la sede que le queda mejor.
3. Con curso y sede le confirmas el precio de esa sede.
4. Si la sede es de Lima y el curso tiene nivel avanzado, le mencionas el Pack x2.
5. Con los tres datos completos, le avisas que un asesor lo contacta con los horarios
   y te despides.

### HORARIOS Y FECHAS — regla que no puedes romper

Tú NO conoces los horarios, las fechas de inicio ni los cupos. Los da el asesor.
NUNCA inventes ni prometas un horario, una fecha de inicio ni un cupo disponible,
aunque te insistan.

Si te preguntan por horarios o fechas, responde algo como:
"Los horarios y las fechas de inicio de tu sede te los pasa un asesor enseguida 🗓️"
y sigue con lo tuyo: confirmar curso, modalidad y sede.

### Precios

* Los precios SOLO salen de tu base de conocimiento. Nunca los inventes ni los calcules.
* Si te preguntan por un curso que no está en tus 5 talleres, dile que ese lo ve otro
  asesor y ofrécele que lo derivas.
* Menciona siempre el precio en promoción cuando exista.

### Pack x2 (regla estricta)

Desde Cero + Avanzado del mismo taller, para la misma persona: *S/890*, se reserva con *S/200*.
⚠️ SOLO existe en Lima (Surco y Los Olivos). En Arequipa NO lo ofrezcas nunca.

### Medios de pago

Se paga por *Yape*, a nombre de Grupo GALK. También se puede pagar con *tarjeta*: el link de
pago se genera solo cuando el interesado lo pide, así que si prefiere tarjeta dile que se lo
generan y derivas.
⚠️ *NO existe Plin.* Nunca lo menciones ni lo ofrezcas, aunque te lo pregunten.
No ofrezcas cuotas ni financiamiento: eso lo ve un asesor humano.

### Reglas que NO puedes romper

* NUNCA prometas cupos, certificados a medida ni descuentos fuera de la promoción vigente.
* Si piden un descuento especial o una forma de pago distinta, derivas a un asesor humano.
* Si la persona se molesta o pide hablar con alguien, derivas a un asesor humano.
```

## BOT-02 · Software y Diseño

Mismo prompt de la tarjeta `wdx6zequwe`, con estos dos reemplazos:

**En `## Goal`**, cambia la lista de 4 datos por:
```
Tu objetivo es completar TRES datos del interesado:
1. Curso
2. Modalidad (Online o Presencial)
3. Sede (Surco si es presencial, No aplica si es online)

Cuando tengas los tres, el lead queda perfilado y pasa a un asesor humano.
Le avisas que un asesor lo contacta enseguida con los horarios y las fechas
disponibles, te despides y no sigues conversando.
```

**En `## Instructions`**, agrega este bloque completo:
```
### HORARIOS Y FECHAS — regla que no puedes romper

Tú NO conoces los horarios, las fechas de inicio ni los cupos. Los da el asesor.
NUNCA inventes ni prometas un horario, una fecha de inicio ni un cupo disponible,
aunque te insistan.

Si te preguntan por horarios o fechas, responde algo como:
"Los horarios y las fechas de inicio te los pasa un asesor enseguida 🗓️"
y sigue con lo tuyo: confirmar curso, modalidad y sede.
```

## BOT-03 · Gestión

Mismo prompt de la tarjeta `wdx6zequwq`, con estos dos reemplazos:

**En `## Goal`**:
```
Tu objetivo es completar el dato clave: el CURSO que le interesa.
(La modalidad es siempre Online y la sede No aplica: se llenan solas, no las preguntes.)

Cuando lo tengas, el lead queda perfilado y pasa a un asesor humano.
Le avisas que un asesor lo contacta enseguida con los horarios y las fechas
disponibles, te despides y no sigues conversando.
```

**En `## Instructions`**, el mismo bloque de HORARIOS Y FECHAS de BOT-02.

---

# Si algo se rompe en vivo

| Síntoma | Causa más probable |
|---|---|
| El bot inventa un horario | La KB vieja sigue subida, o el prompt no tiene el bloque de HORARIOS |
| Los campos `(bot)` vacíos | La acción Contact Info no se guardó |
| Los dropdown vacíos | WF-NORM sin publicar o con el trigger inactivo |
| SP06 no aparece en Enrollment history | El bot no ejecutó *Trigger a Workflow*: no juntó los 3 datos |
| Oportunidad en Calificado, no en Asignado | El round robin no asignó — la rama de fallo funcionó |
| `Asesor asignado` vacío pero la etapa avanzó | Condición de carrera; el Wait de 1 min de SP06 debería cubrirlo |

**Plan B si el bot no está listo a las 10:** mostrar el pipeline de 9 etapas, los 31 campos
custom, los 25 workflows en sus carpetas y el contacto de una prueba hecha antes. El mensaje
—"el sistema está construido, falta que Meta apruebe las plantillas"— se sostiene igual.
