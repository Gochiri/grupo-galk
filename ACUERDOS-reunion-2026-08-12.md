# Reunión con Lucía Gálvez (Grupo GALK) — 12-ago-2026

Asistentes: Lucía Gálvez (cliente) · Francisco Rodríguez (agencia) · Henry, Oliver, Germán (Profit).
Se probó **solo BOT-01 Talleres** en el canal SMS de prueba, con el contacto `pruebas demo`.

Veredicto: la estructura le gustó. Lo que pidió cambiar es **el contenido y el orden de la
conversación**, no la arquitectura. Nada de lo construido se tira.

---

## 1. Decisiones cerradas

### D1 · Los horarios y las fechas los da el asesor — CONFIRMADO

> Lucía (14:59): *"lo que es horarios sí sería bueno que obviamente lo maneje el vendedor,
> porque nosotros cambiamos horarios una vez a la semana"*.

El modo demo deja de ser provisional. **`ROLLBACK-flujo-ficha.md` queda archivado: no hay rollback.**

Consecuencia pendiente: BOT-02 y BOT-03 **siguen con el flujo viejo de 4 datos + ficha**. Hay que
pasarlos al mismo esquema de 3 datos que BOT-01. (Era la condición que puso Oliver al abrir la
reunión: *"si les gusta esta forma, modificamos los otros"* — les gustó.)

Matiz importante que dio Lucía y que no teníamos:

> *"Lo único que se mueve son las fechas de inicio, más no los días ni los horarios."*

O sea, los horarios en sí son fijos; lo que rota semana a semana es la **fecha de inicio**. Aun así
la decisión es la misma: el bot no da ninguno de los dos.

### D2 · El bot presenta el producto ANTES de hablar de precio

El reclamo más fuerte de la reunión:

> Lucía (13:23): *"si tú le das en un segundo el costo, como que le va a decir: pucha, no, es
> demasiado. Pero si no le presentas bien el producto, si no eres claro con qué es lo que va a
> lograr, qué es lo que va a aprender, cuántas son las promociones que manejamos, no va a procesar
> bien. Y el trabajo del vendedor sería el doble."*

> Lucía (15:38): *"cuando pregunte yo melamina, que me explique exactamente qué va a ser el curso:
> A, B, C, D. La primera parte de la información me la dé completa."*

El precio **no desaparece** — se dice después de la presentación, y siempre con la promoción.
Lo que cambia es el orden: valor primero, cifra después.

### D3 · Imágenes: 1 o 2, nunca el "chorrero"

> Francisco (32:43): *"como han vendido así con el chorrero de fotos, piensan que así está bien.
> Yo le he explicado que por eso tienen bloqueo."*
> Henry (33:29): *"se pueden enviar una o dos fotos, pero no el chorrero."*

Reglas acordadas:
- Se disparan **cuando el bot ya detectó el curso**, no en el saludo genérico.
- Máximo **2 imágenes**.
- La imagen **no lleva fechas ni duración** — solo el contenido de lo que se aprende
  (Henry 34:55: *"la imagen no tiene que decir ni fechas ni duración"*).
- Francisco las sube a un Drive. **Ya llegaron** (confirmado por Oliver el 15-ago).

### D4 · Datos que el bot dijo mal en vivo

| Lo que dijo el bot | Realidad | Causa |
|---|---|---|
| "S/490" | Melamina Desde Cero promo = **S/525** (Surco / Los Olivos) | inventado; la KB dice 525 |
| "cuatro semanas" | son **16 horas**; se reparten en 1½ semanas, 2 semanas o un mes según el horario | el bot tradujo "4 días" a "4 semanas" |

Arreglo aplicado (ver §3): la duración deja de expresarse en calendario y **los precios se meten
también en el prompt**, no solo en la Knowledge Base — la KB se consulta por similitud y puede
fallar; el prompt siempre está en contexto.

### D5 · Fuera de alcance de esta fase

- **Encuestas de satisfacción por docente** (Lucía 27:20). Lo nuestro es la encuesta de
  satisfacción del alumno → reseña en Google. Lo de evaluar docentes se puede hacer después.
- **Snippets / plantillas de respuesta rápida**: ya existen en la subcuenta, los maneja el equipo
  de GALK. Francisco los capacita, nosotros no los construimos.

---

## 2. Lo que quedó pendiente de definir con el cliente

### P1 · Matriculados — cómo entran al CRM

Es la duda que Francisco marcó al inicio (1:39) y que Lucía retomó (24:21). Hoy ella matricula en
una planilla aparte. Lo que pidió:

> *"que se cargue como normalmente lo cargamos y adicional lo coloquemos también aquí, para que
> salga la data de todos los inscritos del mes: cuántos alumnos, cuáles solo dieron un adelanto,
> cuáles ya no continuaron."*

Sin esto **AP01–AP04 no arrancan**: los recordatorios de 48 h y 24 h antes del inicio dependen de
que exista una fecha de inicio en el contacto. Falta decidir:

1. ¿La matrícula entra moviendo la oportunidad a *Matriculado* en el CRM, o por importación desde
   su planilla?
2. ¿Quién escribe la **fecha de inicio del grupo** en el contacto? Es el ancla de los recordatorios.
3. "Adelanto" no existe hoy como estado. ¿Se agrega una etapa o un campo?

### P2 · Dos precios que faltan y una duración sin fuente

**Decidido el 15-ago:** el bot **sí da precios**, con la promoción, después de presentar el
producto. Las actualizaciones mensuales de promociones las gestiona Francisco; nosotros
entregamos la estructura y el contenido se mueve dentro de ella. No se vuelve a abrir el tema.

Con eso cerrado, quedan tres datos por conseguir. Auditados contra los 3 catálogos el 15-ago:

**Precios — 12 de 14 cursos completos.** Faltan:

| Curso | Falta |
|---|---|
| Melamina Avanzado (G16) | precio regular y promo, las 3 sedes |
| Drywall Avanzado | precio regular y promo, las 3 sedes |

Son justo los dos donde el bot tiene más chance de inventar, porque tiene alrededor todo para
deducirlos: Melamina Desde Cero promo = S/525 y Pack x2 (desde cero + avanzado) = S/890. Restar y
contestar "S/365" es exactamente lo que un modelo hace con confianza. Por eso el prompt v3 los
nombra explícitamente como POR CONFIRMAR en vez de omitirlos, y prohíbe calcular: un hueco
silencioso se rellena, uno nombrado no.

**Duración — sin fuente.** La KB dice 16 horas (melamina y drywall) y 20 horas (electricidad),
pero los 3 catálogos dicen `por confirmar` en los 14 cursos. Ese 16 fue de donde salió el "cuatro
semanas" que Lucía corrigió en vivo; ella rechazó las semanas pero nunca confirmó las horas.
Si el número no es firme, lo más limpio es que el bot tampoco dé duración y la mande al asesor,
igual que los horarios.

### P3 · Contenido real de los cursos de BOT-02 y BOT-03

La presentación de producto que pidió Lucía (D2) se puede escribir bien para talleres, porque la
KB tiene el detalle de qué se aprende. Para **software y gestión la KB está casi vacía**: duración
"POR CONFIRMAR" en los 8 cursos y una línea de descripción cada uno. Si le pedimos a esos bots
"explica A, B, C, D", van a inventar. Hace falta el temario real.

### P4 · Asesores de lunes a sábado, bot 24/7

Lucía (17:43) confirmó que los domingos no trabaja nadie. El bot sí califica y el round-robin sí
asigna. Un lead calificado un domingo se le asigna a alguien que no está y el anti-fuga corre igual.
Decidir si se congela la asignación fuera de horario o se deja así.

---

## 3. Backlog de implementación

Prioridad para la próxima demo (Francisco prueba primero, luego Lucía).

| # | Qué | Dónde | Estado |
|---|---|---|---|
| 1 | Duración sin calendario + precios embebidos en prompt | KB ×3 + prompts ×3 | ✅ hecho |
| 2 | Bloque de presentación de producto por curso | `KB-BOT-01` | ✅ hecho |
| 3 | Prompts v3 con el nuevo orden de conversación | `guias-bots/PROMPTS-bots-v3.md` | ✅ hecho — **los pega Oliver en la UI** |
| 4 | Subir las 3 KB actualizadas a los bots | UI de GHL | ⬜ Oliver |
| 5 | Publicar **WF-MOD** y validar que `Modalidad` se llena | GHL | ⬜ bloquea SP06 |
| 6 | Workflow de envío de 1–2 imágenes por curso | GHL | ⬜ falta subir las imágenes a la media library |
| 7 | BOT-02 y BOT-03 al esquema de 3 datos | UI + KB | ⬜ |
| 8 | Presentación de producto de software y gestión | — | 🔒 bloqueado por P3 |
| 9 | AP01–AP04 (recordatorios 48 h / 24 h) | GHL | 🔒 bloqueado por P1 |

---

## 4. El bug interno que sigue abierto

**`Modalidad` no se llena y por eso SP06 no dispara.**

La acción *Contact Info* de Conversation AI **extrae** datos de lo que dice el lead. En talleres la
modalidad es siempre "Presencial", así que el lead nunca la dice y la acción nunca se activa. No es
un problema de redacción del prompt: no hay nada que extraer.

Verificado el 11-ago leyendo el contacto por API: `Curso de interés` ✅ y `Sede` ✅ sí se llenan.
El único hueco es `Modalidad`.

Solución ya construida: **`WF-MOD | Modalidad automática por curso`**
(`8e19ee3b-5cfe-4c38-a501-12cfdc16a0ea`, 9 ramas) deduce la modalidad del curso y la escribe
directamente en el dropdown — los workflows sí pueden escribir dropdowns, los bots no.

Sigue en **draft**. Para probarlo: publicarlo, usar un contacto **nuevo** (Contact Info solo llena
campos vacíos) y etiquetarlo `equipo-interno` — no `pruebas demo`, que no filtra nada y deja que
corran encima los 33 triggers vivos de Francisco.

---

## 5. SP06 se disparaba con los campos vacíos (arreglado el 15-ago)

En la prueba del 15-ago el evento *Flujo de trabajo activado → SP06* apareció en la conversación
aunque los tres campos estaban vacíos. La causa no es SP06: es **quién lo llama**.

BOT-01 tiene una acción *Trigger a Workflow* llamada "Marcar lead calificado" con esta condición
de inicio escrita a mano:

> *"Cuando ya tengas guardados los tres datos: curso, modalidad y sede. No antes. Si falta alguno,
> no ejecutes: sigue conversando hasta completarlos."*

Esa frase **no es una validación, es texto que interpreta el modelo**. El bot creyó tener los datos
porque él mismo los había dicho en su mensaje — pero *Contact Info* extrae de lo que dice la
persona, no de lo que escribe el bot. Y la acción usa `add_to_workflow`, así que entra por la
puerta de atrás: se salta el trigger propio de SP06 (`Tag Added: galk-bot-calificado`).

**No hubo daño de pura casualidad.** SP06 arrancaba con un if/else que corta si el contacto ya
tiene asesor, y WF2 de Francisco ya le había asignado uno a las 10:09. Se cumplió esa rama y SP06
murió ahí. La prueba es que `Calificado` quedó vacío, y ese es el primer nodo de la rama buena.

En un contacto limpio (`equipo-interno`, sin los workflows viejos encima) esa guarda no se cumple
y SP06 corre entero: `Calificado = Sí`, oportunidad creada y movida a Asignado, notificación al
asesor y **bot silenciado**. Un lead sin curso, sin sede y sin modalidad en la bandeja de un
vendedor, y el bot mudo para arreglarlo.

### El primer intento de guarda no servía

La v1 metió los tres campos en el if/else de entrada, que ya traía `assigned_to has_value`. Pero
ese if/else **ya no cortaba**: tenía colgado un nodo `Go to` que salta a "Calificado = Sí + Fecha",
o sea a la misma cadena que la rama else. Las dos ramas terminaban en el mismo sitio.

Y el `Go to` estaba bien puesto, por una razón real: el plugin de pruebas que conecta WhatsApp por
SMS **solo funciona si el contacto tiene un usuario asignado** — si no, da error al responder. En
pruebas *todos* los contactos tienen asesor, así que `assigned_to has_value` se cumplía siempre y
SP06 moría antes de empezar. El `Go to` era el parche. Se quita solo cuando se conecte la API
oficial de WhatsApp.

### El arreglo bueno (v2)

La guarda mezclaba dos cosas distintas:

* **"faltan datos"** → tiene que cortar SIEMPRE, sin excepción
* **"ya tiene asesor"** → anti-reproceso, pero choca de frente con el plugin

Así que se cambia el marcador de anti-reproceso: en vez de `assigned_to` —que el plugin llena de
entrada— se usa **`Calificado`**, que es lo primero que escribe SP06 cuando de verdad procesa un
lead. El plugin no lo toca, así que el `Go to` deja de hacer falta y se eliminó.

**Aplicado** (`scripts_ghl/guardia_sp06.py`, SP06 sigue publicado, de 19 a 18 nodos):

```
NO calificar si:  Calificado ya tiene valor      (ya se procesó)
              O   Curso de interés está vacío
              O   Modalidad está vacía
              O   Sede está vacía
```

Un solo nodo de condición, sin anidar nada, y la rama vuelve a ser un callejón sin salida. Se
comprueban los campos **canónicos**, no los gemelos de texto del bot, así que la guarda verifica
de paso que WF-NORM y WF-MOD ya corrieron antes de dar el lead por bueno.

**Pendiente conocido:** WF-SWITCH limpia los 10 campos de interés al cambiar de familia pero no
limpia `Calificado`, así que un lead ya calificado que cambia de familia no se puede recalificar.
No es una regresión — con `assigned_to` pasaba lo mismo y peor, porque el dueño no se limpia
nunca. Se decide aparte: recalificar implica mover la oportunidad hacia atrás y volver a pasar por
el round robin.

---

## 6. La cadena completa funcionó — 15-ago, contacto `6qYKCW0WI79XLV245V17`

Con WF-MOD publicado y el prompt v3 endurecido pegado, el flujo corrió entero por primera vez.
Verificado por API, no por la UI:

```
Familia de interés (bot)  = Talleres
Curso de interés          = Melamina Desde Cero    ✅
Modalidad (bot)           = Presencial
Modalidad                 = Presencial             ✅
Sede (bot)                = Surco
Sede                      = Surco                  ✅
Calificado                = Sí
Asesor asignado (nuevo)   = Oliver Guerrero
tags: … bot-silenciado, asesor-notificado
Oportunidad: Nuevo Lead → Calificado → Asignado a asesor
```

Y el bot se comportó: presentó antes del precio, **preguntó el nivel**, dijo S/525, contestó
16 horas sin traducirlas a semanas, mandó las fechas al asesor sin cerrar, y solo se despidió
cuando ya tenía nivel y sede. Los tres bloques nuevos del prompt hicieron su trabajo.

### 6.1 · `Familia de interés` (el canónico) sigue vacío

`Familia de interés (bot)` = Talleres, pero el dropdown `Familia de interés` quedó en blanco.
Pasó igual en el contacto anterior, así que es sistemático, no casualidad.

WF-NORM-1 está bien por dentro: publicado, trigger `Familia de interés (bot) has-changed`, rama
`contain 'taller'` → escribe `Familia de interés = Talleres`. Sus hermanos con la misma estructura
sí funcionaron (`Modalidad` y `Sede` quedaron normalizadas). La diferencia es **cuándo** se dispara:
NORM-1 depende de un campo que escribe BOT-00 en el primer segundo de vida del contacto, mientras
que NORM-2 y NORM-3 dependen de campos que escribe BOT-01 más tarde.

*Historial de inscripciones* de WF-NORM-1: **"No se han encontrado inscripciones"**. Ningún
contacto entró nunca. Y no es que el bot no escribiera el campo — `Familia de interés (bot)` dice
`Talleres`, leído por API.

**Causa encontrada — y afectaba a 5 workflows, no a uno.** Cada trigger guarda un
`targetActionId`: el nodo por el que el contacto entra. Los triggers viven en un endpoint aparte
y **el PUT del workflow no los toca**, así que cada vez que un script reconstruyó los nodos —y
todos generan IDs nuevos— el trigger se quedó apuntando al nodo viejo. Dispara, no encuentra por
dónde entrar, y no pasa nada. Sin error, sin inscripción, sin rastro en *Registros de ejecución*.

| Workflow | Estado | Qué implicaba |
|---|---|---|
| **WF-NORM-1** | publicado | `Familia de interés` nunca se normalizaba |
| **WF-SWITCH** | publicado | cambiar de familia **nunca limpiaba** el interés viejo |
| **SP06** | publicado | su trigger por tag estaba muerto; corría solo porque el bot lo llama con `add_to_workflow` |
| **AP01** | draft | — |
| **PS01-B** | draft | — |

**Arreglado** con `scripts_ghl/reparar_targetaction.py`: recalcula el nodo de entrada (el único
sin `parent` y al que nadie apunta con `next`) y reapunta el trigger, respetando `active` y el
estado de cada workflow. Los cinco tenían un único candidato. Re-escaneado después: limpio.

El de WF-SWITCH era el más peligroso de los cinco y nadie lo había notado: un lead que empieza
preguntando por talleres y termina en software se quedaba con el curso y la sede del taller
pegados encima.

La regla quedó anotada en el handoff §2: **todo script que haga PUT de `workflowData` tiene que
reapuntar el trigger después**, y conviene pasar el auditor tras cada reconstrucción.

### 6.2 · El nodo Round Robin marcó Error

En el registro de ejecución el nodo *Round Robin (6 asesores)* sale en rojo, y aun así el lead
terminó con dueño. Los 7 usuarios de la lista existen, lo verifiqué.

Lo más probable es que sea **un artefacto de la prueba**: al contacto se le asignó un usuario a
mano antes de empezar (para que el plugin de SMS pudiera responder), y el round robin de GHL falla
cuando el contacto ya tiene dueño. Si es eso, en producción no pasa, porque el lead entra sin
asignar.

El flujo siguió igual y salió bien porque `{{user.name}}` resolvió al dueño que ya estaba. Vale la
pena notar que **el diseño aguantó**: si no hubiera habido dueño previo y el round robin fallaba,
el if/else de "Asesor asignado" habría mandado el lead a la rama de fallo — avisar a Lucía, tag
`asignacion-fallida` y **sin** silenciar al bot. Que es justamente para lo que se construyó.

Confirmarlo cuesta 10 segundos: clic en el nodo rojo del registro y leer el mensaje de error.
Hay que hacerlo antes de mandar tráfico real, porque el round robin es la asignación de todos los
leads.

**La lección de arquitectura:** ninguna condición escrita en lenguaje natural dentro de un bot es
una garantía. El workflow es la última línea de defensa y no debe confiar en quien lo llama.

Conviene además apretar el texto de la acción en la UI, aunque sea la capa blanda:

> Ejecuta SOLO si los tres campos del contacto ya tienen valor guardado: Curso de interés,
> Modalidad y Sede. No te bases en lo que tú escribiste en la conversación, sino en que la persona
> te haya dicho el nivel exacto del curso y la sede con sus propias palabras. Si falta cualquiera
> de los tres, NO ejecutes: sigue conversando hasta completarlos.
