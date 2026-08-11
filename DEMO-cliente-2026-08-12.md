# Demo al cliente · miércoles 12-ago 10:00

> Plan para mostrar el sistema funcionando **sin WABA y sin tocar nada real**.
> Verificado el 11-ago: el pipeline nuevo *Ventas GALK* tiene **0 oportunidades**;
> las 3.722 reales viven en el pipeline viejo de Francisco. Por eso se puede publicar
> lo nuestro y demostrar en vivo sin riesgo.

---

## 1. El flujo nuevo — el que se propone al cliente

```
                    Meta / Instagram / TikTok
                              │
                   (autorrespuestas nativas APAGADAS)
                    mensaje con BOTÓN → WhatsApp
                              │
                              ▼
                        WhatsApp oficial
                              │
                     LS01 · captura atribución
                     UTMs, anuncio, crea oportunidad
                              │
                              ▼
                   BOT-00 · Secretaria (router)
                   saluda · pide nombre · detecta familia
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         BOT-01           BOT-02           BOT-03
        Talleres         Software         Gestión
              │               │               │
              └───────────────┼───────────────┘
                              │
                    P E R F I L A   3   D A T O S
                    ┌─────────────────────────┐
                    │  1. Curso               │
                    │  2. Modalidad           │
                    │  3. Sede                │
                    └─────────────────────────┘
                              │
                    WF-NORM-1..4 normalizan
                    los campos de texto → dropdowns
                              │
                              ▼
                    SP06 · CALIFICA Y ASIGNA
                    ├─ Calificado = Sí
                    ├─ Oportunidad → etapa Calificado
                    ├─ Round Robin entre las 6 asesoras
                    ├─ ESCRIBE EL ASESOR EN EL CONTACTO  ← el fix
                    ├─ ¿se asignó?
                    │    SÍ → etapa Asignado · notifica · silencia el bot
                    │    NO → avisa a Lucía · queda en Calificado · bot vivo
                    ▼
        ╔═══════════════════════════════════════════════╗
        ║   AQUÍ ENTRA EL VENDEDOR                      ║
        ║   Recibe el lead con el contexto ya resumido: ║
        ║   curso · modalidad · sede · de dónde vino    ║
        ║   Él da días, horarios, fechas y su flyer.    ║
        ╚═══════════════════════════════════════════════╝
                              │
                              ▼
                   SP09 · datos de pago (Yape)
                              │
                   SP10 · detecta el comprobante
                   crea tarea a Lucía para validar
                              │
                   SP10-B · Lucía marca validado
                              │
                   SP11 · Matriculado · GANADO
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        AP01 confirma   AP02 recuerda    AP03 grupo WA
                        T-48h y T-24h
                              │
                              ▼
                   PS01 encuesta · PS01-B reseña
                   PS02 venta cruzada · PS03 reintento 60d

    Si no cierra → SP12 · Perdido con razón obligatoria
```

### Qué cambia respecto al diseño anterior

| Antes | Ahora |
|---|---|
| El bot mandaba la ficha con horarios (SP05, 24 ramas) | **El vendedor da horarios, fechas y sedes** |
| 4 datos de calificación (+ horario) | **3 datos**: curso, modalidad, sede |
| Había que congelar 24 URLs de fichas en Fase 0 | Ese bloqueante **desaparece** |
| El bot dependía del panel, que tiene fechas vencidas | El bot no dice ninguna fecha, así que **no se desactualiza** |

---

## 2. Qué hay que tener listo antes de las 10

### A · Construir BOT-01 en la UI · ~40 min

Solo uno. Con uno alcanza para la demo y es el más representativo.

`Settings → AI Agents → nuevo agente`

| Paso | Qué |
|---|---|
| 1 | **Model** GPT 4.1 · **Business Name** Grupo GALK |
| 2 | **Prompt** — pegar el de la tarjeta `wdx6zequw1`, con **un cambio**: en `## Goal`, dejar 3 datos (curso, modalidad, sede) y quitar el horario. Agregar al final del Goal: *"Cuando tengas los tres, avisa que un asesor lo contacta con los horarios disponibles y te despides."* |
| 3 | **Knowledge Base** — subir `knowledge-base/KB-BOT-01-talleres.md` |
| 4 | **Actions → Contact Info** — 3 campos: `Curso de interés`, `Modalidad (bot)`, `Sede (bot)`. **Sin horario.** Config exacta en la tarjeta `wdx6zequvz` |
| 5 | **Actions → Trigger a Workflow** → `SP06`, cuándo ejecutar: *"cuando tengas guardados curso, modalidad y sede"* |
| 6 | **Actions → Human Handover** — mensaje de la tarjeta `wdx6zequw5` |
| 7 | **Timing & Pacing**: wait 2s · máx 25 · **sleep on Manual + Workflow ON** |
| 8 | **Response Behavior**: los 3 toggles en OFF |
| 9 | **Deploy**: NO conectar canal. Se demuestra con **"Probar tu agente"** |

### B · Publicar solo estos 5 workflows

Son los únicos que hacen falta para la demo, y los únicos que se pueden publicar sin riesgo:

```
WF-NORM-1  Normalizar Familia de interés
WF-NORM-2  Normalizar Modalidad
WF-NORM-3  Normalizar Sede
WF-NORM-4  Normalizar Pack x2
SP06       Calificación y asignación
```

**Por qué son seguros:** sus triggers son los campos `(bot)` y el tag `galk-bot-calificado`.
Nada del sistema viejo los escribe, y el pipeline nuevo está vacío.

⚠️ **NO publicar nada que mande WhatsApp.** Los 42 nodos `whatsapp_v2` no tienen `templateId`
ni `phoneNumberId` todavía (falta que Meta apruebe las plantillas), así que fallarían en vivo.

### C · Crear el contacto de prueba

| Campo | Valor |
|---|---|
| Nombre | `PRUEBA DEMO` |
| Teléfono | uno tuyo |
| **Tag** | **`equipo-interno`** ← imprescindible |

El tag `equipo-interno` es el que usan los **33 triggers `customer_reply` vivos de Francisco**
como exclusión. Sin él, el contacto de prueba entra en los flujos del sistema viejo en medio
de la demo.

---

## 3. El guion de la demo · ~12 min

**1 · El problema, con sus propios números** (2 min)
Abrir el pipeline viejo: **3.722 oportunidades, todas abiertas**. Ninguna ganada, ninguna
perdida. Y el campo "Asesor asignado" al 0% sobre 500 contactos revisados: el round robin
asignaba la oportunidad pero no escribía en el contacto, así que **nadie sabía de quién era
cada lead**.

**2 · La conversación** (4 min)
Abrir BOT-01 → *Probar tu agente*. Escribir como un lead real:

```
hola, quiero info del taller de melamina
desde cero
en los olivos
```

Que vean: una pregunta por mensaje, tono peruano, precios correctos desde la KB, y que
**nunca inventa un horario**.

**3 · Lo que pasó por detrás** (4 min) — esto es lo que vende
Abrir el contacto y mostrar, en este orden:
- Los campos `(bot)` que escribió el bot
- Los dropdown ya normalizados por WF-NORM
- La oportunidad **creada y movida** a *Asignado a asesor* en el pipeline nuevo
- **El asesor escrito en el contacto** ← decir explícitamente que este era el bug nº1
- La notificación que le llegó a esa asesora

**4 · Dónde entra el vendedor** (2 min)
"El bot llega hasta acá y se apaga solo. La asesora entra y ve la conversación completa: sabe
que quiere Melamina Desde Cero en Los Olivos. No pregunta de nuevo — arranca dando los
horarios de esa sede."

---

## 4. Cómo plantearle el cambio a Lucía

Ella dijo que lo que quieren es *"recibir mensajes para vender"*. El argumento se le da vuelta
a favor:

> "El bot no les quita la venta, se las entrega lista. Hoy sus asesoras abren 600 mensajes
> diarios sin saber cuáles son curiosos. Con esto solo les llega el que ya dijo qué curso, qué
> modalidad y qué sede quiere. **Los horarios y las fechas los siguen dando ustedes**, porque
> son quienes los conocen al día — el bot ni los menciona, así que nunca va a mandar una fecha
> vencida."

Ese último punto es fuerte y es real: el panel tiene fechas ya pasadas. Un bot que promete
fechas se equivoca; uno que no las toca, no.

---

## 5. Qué NO prometer mañana

- **Fecha de salida a producción.** Depende de que Meta apruebe las plantillas de WhatsApp,
  que es trámite externo. La WABA ya está verificada, falta eso.
- **Mensajes automáticos funcionando.** Ninguno puede enviar todavía por lo mismo.
- **Llamadas por WhatsApp.** Se puede, ~USD 0,0127/min en Perú, pero se factura a Francisco.
  Es decisión comercial de ellos.

---

## 6. Después de la reunión

Si el cliente confirma el flujo nuevo, la adaptación son ~2 horas:

1. Reescribir la notificación de SP06 sin el horario, con el resumen que el asesor necesita
2. Quitar `Horario de interés` de las 3 acciones de Contact Info
3. Ajustar el bloque *Horarios* de las 3 KB: de *"vienen en la ficha"* a *"te los da tu asesor"*
4. Archivar **SP05** y sus 24 custom values de fichas
5. Actualizar las tarjetas de ClickUp afectadas

Si lo rechaza, volver a 4/4 es agregar un campo a Contact Info y reactivar SP05. También ~2 horas.
