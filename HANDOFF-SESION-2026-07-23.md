# HANDOFF DE SESIÓN — Grupo GALK · 23-jul-2026

> Contexto completo para continuar en una sesión nueva de Claude Code.
> Repo: `Gochiri/grupo-galk` · Rama de trabajo: **`claude/ghl-cli-read-audit-qd9f7s`**
> Subcuenta GHL (location): **`YN2uRSDcNeBdTWm3UPCU`**

---

## 0. CÓMO RETOMAR (primeros 5 minutos)

1. **Credenciales**: viven en `.env` en la raíz (gitignoreado, NO está en el repo). Si la sesión nueva es un contenedor limpio, hay que volver a crearlo con:
   - `GHL_API_KEY` = el PIT (el vigente empieza por `pit-abe35f6d-…`)
   - `GHL_LOCATION_ID=YN2uRSDcNeBdTWm3UPCU`
   - `GHL_FIREBASE_REFRESH_TOKEN` = token de Firebase (el de esta sesión empieza por `AMf-vBzvIi0Uqy…`). **Caduca/rota**: si da 401, pedir uno nuevo con la extensión de Chrome del repo.
2. **Instalación**: `./install.sh` (crea `.venv`, instala el paquete). Smoke test: `./ghl --json contacts list --limit 3`.
3. **Permiso de escritura**: ya existe `.claude/settings.local.json` con la regla `Bash(/home/user/grupo-galk/.venv/bin/python:*)`. Sin eso, el clasificador **bloquea** las llamadas de escritura a GHL. Los scripts se invocan con **ruta absoluta del python del venv** y cargan el `.env` internamente.
4. **Scripts**: todo lo construido está en `scripts_ghl/` (commiteado). Los CSVs de Knowledge Base en `knowledge-base/`.

---

## 1. ESTADO: QUÉ YA ESTÁ CONSTRUIDO EN LA SUBCUENTA

Todo esto está **hecho y verificado por API** (23-jul). Regla de oro §3 respetada: nada heredado se editó; todo lo nuevo es aditivo.

### ✅ Pipeline "Ventas GALK" (SETUP-02 — completo)
`pipeline_id` = **`Pm48HGVyRbd5TAZDrKQS`**

| # | Etapa | stage_id |
|---|---|---|
| 0 | Nuevo Lead | `cff49047-ba9e-48a2-913d-502a9d7c3c5c` |
| 1 | En conversación (bot) | `2af2c764-dda1-4c44-ba2a-80355ab654af` |
| 2 | Ficha enviada | `3c63e11a-ca60-4e35-b01c-a2e17fa9837f` |
| 3 | Calificado | `a8fc4fba-b821-44f4-9c22-f3d58636fadd` |
| 4 | Asignado a asesor | `cad87dc6-85d5-4790-b399-2899d7949d97` |
| 5 | Datos de pago enviados | `6a31b31e-3b73-4aae-8156-e6cf41ec131a` |
| 6 | Pago en validación | `52655bf6-5718-44c2-9b32-abb5b4eeca25` |
| 7 | Matriculado | `adc03786-792f-4db7-9950-158a9a47b5ec` |
| 8 | Perdido | `0d22f17e-6b1c-4c17-bc7c-4c22af5c179f` |

El pipeline heredado `[GALK] Cursos y Capacitaciones` (`95f7TlUen51QyUax2pji`, 7 etapas, ~2.370 oportunidades) sigue **intacto**; se migra/archiva en el cutover.

### ✅ 27 campos custom en 4 carpetas (SETUP-03 — completo)
Carpetas (el `parentId` se saca de la URL de la UI):
- Identificación del lead `R5Aa0kU4gDXkMAlQJUJp` (9 campos)
- Calificación `LMLDqpaeMoec2OEeBkyb` (8)
- Pago y matrícula `bCbLvp8svNbdSyOrZjPQ` (7)
- Post-venta `ZUUUGDgRxbcKyWfdA5yo` (3)

Keys (modelo `contact`) — **usar EXACTO**:

`contact.familia_de_inters` (Talleres/Software/Gestion) · `contact.curso_de_inters` · `contact.fuente` · `contact.fecha_de_primer_contacto` · `contact.utm_source` · `contact.utm_medium` · `contact.utm_campaign` · `contact.anuncio_ad_name` · `contact.ad_id`
`contact.modalidad` (Presencial/Online) · `contact.sede` (Surco/Los Olivos/Arequipa/No aplica) · `contact.horario_de_inters` · `contact.calificado` · `contact.fecha_de_calificacin` · `contact.asesor_asignado_nuevo` · `contact.fecha_de_asignacin` · `contact.pack_x2`
`contact.precio_cotizado` · `contact.comprobante_recibido` · `contact.comprobante_validado` · `contact.validado_por` · `contact.fecha_de_validacin` · `contact.fecha_de_inicio` · `contact.grupo_whatsapp_asignado`
`contact.nota_encuesta_15` · `contact.fecha_fin_de_taller` · `contact.razn_de_prdida` (7 opciones, alinea con SP12)

field IDs útiles: curso `bjDW7b9QoRiFWL5d578w` · sede `B2tnsFlAOp9kYWF9Ij4R` · modalidad `M2Ra6FDckxrylnFygVVH` · calificado `f4VzKV05rOxdyKX9rq1G` · fecha calif. `aR0Dne9NV5FG5NyzYNDw` · asesor `m36ikoz5RjrJFrtDh3kt` · fecha asig. `z2mA0nEBefblpZaE3NZH`

> ⚠️ Se llamó **"Asesor asignado (nuevo)"** para no colisionar con el heredado `contact.asesor_asignado` (0% de llenado). En SETUP-01 se borra el heredado y este pasa a ser el oficial.

### ✅ 24 Custom Values de fichas, vacíos (SETUP-04 — completo)
Convención `Ficha <Curso> - <Sede/Modalidad>`; los keys quedan como `{{custom_values.ficha_melamina_desde_cero__surco}}`, etc. **Valor vacío a propósito** — las URLs reales las pone el panel RoasSeeker en Fase 0.3.

### 🟡 SP06 · Calificación y asignación — **DRAFT, sin publicar**
`workflow_id` = **`84811c16-30d8-4c08-a05d-0c12fa46567d`** · carpeta "SP · Pipeline de Ventas (NUEVO)" (`88df3a08-da28-4a19-a239-20ff3ae675e9`)
Trigger: Tag Added `lead-calificado`. 7 nodos:
1. Update fields: Calificado=Sí + Fecha de calificación
2. Oportunidad → etapa Calificado
3. **Round Robin** 6 asesores
4. **Update fields EN EL CONTACTO: Asesor + Fecha de asignación** ← fix del bug nº1
5. Oportunidad → etapa Asignado a asesor
6. Notificación interna al asesor
7. Add Tag `bot-silenciado`

**Falta / verificar en UI**: guard `if_else` "asesor no vacío → STOP"; webhook **CAPI CompleteRegistration** (no hay ejemplo en la subcuenta y depende del dataset de Meta); confirmar merge tokens `{{user.name}}` y `{{right_now}}`; confirmar que "create or update opportunity" **mueve** y no duplica.

### 🟡 SP05 · Envío de ficha (árbol 24 ramas) — **DRAFT, sin publicar**
`workflow_id` = **`ae78625c-8f91-4af1-a7b0-3be0b2e4a667`**
Trigger: Tag Added `enviar-ficha`. **51 nodos** = 1 router `if_else` con 24 ramas (curso × sede/modalidad) → 24 `whatsapp_v2` + rama None → notificación "ficha sin match".
**§6 cumplido**: cada rama usa `media_url = {{custom_values.ficha_…}}`, cero URLs hardcodeadas.

**Placeholders a reemplazar antes de publicar**: `template_id` y `from_phone_number` llevan los IDs de **GoGHL de Francisco** → cambiar por plantilla WABA aprobada (Fase 0.6) y número WABA nuevo (Fase 0.5) en los 24 nodos. Verificar en UI que `media_url` acepte `{{custom_values…}}`.

### ✅ 3 CSVs de Knowledge Base (`knowledge-base/`)
`catalogo-talleres-galk.csv` (14 filas) · `catalogo-software-galk.csv` (6) · `catalogo-gestion-galk.csv` (4) + `README.md`.
Precios confirmados del §4 puestos; **precios de "Avanzado" y duraciones marcados `por confirmar`** (el §4 no los da). Códigos G en conflicto (G12 AutoCAD, G15 Espacios Comerciales) señalados → Fase 0.1.

### ❌ Lo que NO está hecho en la subcuenta
- **SETUP-01 limpieza** (Henry): borrar campo "How often do you normally workout?", 4 calendarios de panadería, funnels Bakery/Bakery Offer, 3 businesses de ejemplo, 4 custom values genéricos, tags basura (triplicado flyer-horarios, `equipo-interno ficha-melamina-enviada`, 6 tags `wa: +51…`), y el heredado `contact.asesor_asignado`.
- **Bots BOT-00..03** — ver §3, requieren UI/Playwright.
- LS01/LS02/LS03, SP08–SP12, AP01–AP04, PS01–PS03 — no construidos.

---

## 2. DESCUBRIMIENTOS TÉCNICOS (lo más valioso para no repetir trabajo)

### API pública (`services.leadconnectorhq.com`, PIT)
| Operación | ¿Funciona? |
|---|---|
| Crear **pipeline** con etapas | ✅ `POST /opportunities/pipelines` → 201 |
| Crear **campos custom** | ✅ `POST /locations/{loc}/customFields` (con `options` para SINGLE_OPTIONS) |
| Mover campo a carpeta | ✅ `PUT /locations/{loc}/customFields/{id}` con `{"name":…, "parentId":…}` |
| Crear **custom values** | ✅ `POST /locations/{loc}/customValues` |
| Listar/crear **carpetas de campos** | ❌ No existe endpoint. **Truco: el `parentId` aparece en la URL de la UI** al abrir la carpeta |
| Listar usuarios | ✅ `GET /users/?locationId=…` |
| Contactos: total y muestra | ✅ `POST /contacts/search` con **`pageLimit`** (no `pageSize`) + `searchAfter` |

### API interna (`backend.leadconnectorhq.com`, token Firebase)
| Servicio | ¿Autoriza el token? |
|---|---|
| **workflows** (`/workflow/{loc}…`) | ✅ **CRUD completo** (crear carpeta/workflow, trigger, PUT de nodos, GET, DELETE) |
| opportunities/pipelines | ❌ 401 |
| custom-fields | ❌ 401 |

### Esquema de nodos de workflow (errores que costaron tiempo)
- `whatsapp_v2` **requiere** `"workflowsActionType": "INTERNAL"` — sin eso: *"action has a corrupted type"*.
- `if_else` requiere `"cat": "conditions"` y `nodeType`: `condition-node` (header, `next` = **lista** de branch ids), `branch-yes` (entrada de cada rama, con `sibling` = ids de las otras), `branch-no` (rama None).
- `internal_notification` no lleva `next`/`parent`, solo `parentKey`.
- Método fiable: **leer un workflow existente de la misma subcuenta y copiar el esquema** (`scripts_ghl/harvest_node_schemas.py`, `dump_ficha.py`). Los 12 tipos presentes: add_contact_tag, add_notes, assign_user, create_opportunity, if_else, internal_notification, remove_contact_tag, sms, task-notification, update_contact_field, wait, whatsapp_v2.
- `create_opportunity` en realidad es **"create or update opportunity"** → sirve para mover de etapa (lleva `pipeline_id` + `pipeline_stage_id` + `opportunity_status`).
- **No hay ejemplos** en la subcuenta de: webhook/CAPI ni de mover etapa (el pipeline heredado nunca avanza etapas).

### Bots
**Conversation AI NO es un flujo de nodos** (eso es Agent Studio). Es un agente con: Model (GPT 4.1) + Business Name + **Prompt** (`## Personality` / `## Goal` / `## Instructions`) + **Actions** (Appointment Booking, Trigger a Workflow, Contact Info, Stop Bot, Human Handover, **Transfer Bot**, **Auto Followup**) + **Knowledge Base Triggers** + **Response Behavior** + **Timing & Pacing** (incluye *sleep when Manual/Workflow Message*) + **Summary Settings** + pestaña **Deploy**.
**No construible por la API de workflows** → UI o Playwright.

---

## 3. CAMBIOS DE ARQUITECTURA vs. EL HANDOFF ORIGINAL

Tres decisiones del handoff se tomaron con el modelo equivocado de bots y **quedaron corregidas**:

1. **WF-DERIV → CANCELADO** (`wdx6zerpqd`). La derivación router→especialista se hace con la acción nativa **Transfer Bot** (con *Trigger Condition* por `Familia de interés`). El "orden crítico" (mensaje puente → sleep → wait 8s → activar + reset message limit) **ya no aplica**: GHL maneja el sleep nativo al transferir.
2. **SP07 → CANCELADO** (`wdx6zequu9`). El seguimiento dentro de ventana es la acción nativa **Auto Followup** del bot.
3. **Bots**: se mantienen **4 separados** (router + 3 especialistas) con **KB propia por bot** — es lo que hace estructuralmente imposible cotizar precios de otra familia/sede.

Además, nomenclatura de etapas congelada a las 9 canónicas; se corrigieron tarjetas que decían "Asignado — En negociación", "Pago por validar" y una etapa inexistente "En seguimiento" (SP08 ahora usa tag `recuperacion-enviada`, sin cambio de etapa).

---

## 4. CLICKUP — ESTRUCTURA Y IDs

Carpeta **`$$ Grupo Galk`** (`1000460000003995`), espacio Activos (`901313322174`). Reorganizada al estilo VN Supply / Advanced Health: 8 listas por módulo (la lista vieja "List" quedó vacía y se puede borrar).

| Lista | list_id |
|---|---|
| 🏗️ 00 · Fase 0 y Entrega | `1000460000007559` |
| 📦 01 · Setup | `1000460000007560` |
| 🤖 02 · Bots Conversation AI | `1000460000007561` |
| 🔵 03 · Lead Sources | `1000460000007562` |
| 🟢 04 · Sales Pipeline | `1000460000007563` |
| 💰 05 · Pagos y Cierres | `1000460000007564` |
| 🔴 06 · Post-venta | `1000460000007565` |
| 🌟 07 · Reviews y Recompra | `1000460000007566` |

**Tareas padre**: Fase 0 `wdx6zequtx` · SETUP-01 `wdx6zerpty` · SETUP-02 `wdx6zerptz` ✅ · SETUP-03 `wdx6zerpu0` ✅ · SETUP-04 `wdx6zerpu1` ✅ · BOT-00 `wdx6zequtz` · BOT-01 `wdx6zequu0` · BOT-02 `wdx6zequu2` · BOT-03 `wdx6zequu3` · WF-DERIV `wdx6zerpqd` ❌ · LS01 `wdx6zequu4` · LS02 `wdx6zequu5` · LS03 `wdx6zequu6` · SP05 `wdx6zequu7` 🟡 · SP06 `wdx6zequu8` 🟡 · SP07 `wdx6zequu9` ❌ · SP08 `wdx6zequua` · SP09 `wdx6zequub` · SP10 `wdx6zequuc` · SP11 `wdx6zequud` · SP12 `wdx6zequue` · AP01 `wdx6zequug` · AP02 `wdx6zequuh` · AP03 `wdx6zequuj` · AP04 `wdx6zequuk` · PS01 `wdx6zequum` · PS02 `wdx6zequun` · PS03 `wdx6zequup` · **QA + Entrega** `wdx6zerrya`

**Asignaciones (9/9/9)** — Germán `180203721`: bots + SP05/SP06/SP08 + SETUP-03. Oliver `89242515`: LS01-03 + SP09-12 + SETUP-02/04. Henry `111980811`: Fase 0 + SETUP-01 + AP01-04 + PS01-03.

**Cronograma comprimido — entrega miércoles 5-ago-2026** (QA 4–5 ago). Fase 0 23–24 jul · Setup 27 jul · LS+SP05/06 28–29 jul · Bots 29 jul–3 ago · Pagos/AP 30–31 jul · PS 3 ago. LS03 (reactivación de base) queda 17–21 ago, post go-live.

---

## 5. USUARIOS DE LA SUBCUENTA GHL

**6 asesores (round robin de SP06)**: Alejandra Díaz `IGRfggnJvAIkyAeMfycr` · Camila Borrero `2O8FOfMSzbRtRMb1FnMf` · Diana Burgos `izAqkNAiyM1zUWOYltFy` · Gabriela Montañez `6N9uVNvdpUCw8LdFnrzE` · Pablo Chavez `LCwIaJwIu1xcOAISNJsI` · Rosa Araujo `cRNnOExeNFPOoqvwC99z`
**Admins**: Lucía Galvez `w7Lzp83UoLfgFb9s8H8w` (supervisora, valida pagos — fuera del round robin) · Germán `mubBlotps59Jarh728fe` · Henry `ui3ZuduHYa70IQhqPE86` · Oliver `UzJ7iMLLEiSv8aNnIft3`

---

## 6. AUDITORÍA (informe en `audit-subcuenta-galk-2026-07-21.md`)

Inventario al 21-jul: 40 workflows (33 pub / 7 draft, ninguno tocado desde el 19-jul) · 10.896 contactos · **2.370 oportunidades, 100% `open`, 92,3% apiladas en "En riesgo"** · 41 tags · 20 calendarios · 4 custom values genéricos vacíos · 14 campos.

Hallazgo central (motiva el fix de SP06): el round robin heredado **asigna a nivel oportunidad pero no escribe en el contacto** → `Asesor asignado` y `Fecha Asignación` al **0%** sobre 500 contactos, mientras el `assignedTo` nativo va al 73,8%.
Calificación heredada 2 de 4 (no existían Modalidad ni Horario) → **resuelto** con SETUP-03.
Contaminación de snapshot intacta (workout, Bakery, Dunder Mifflin…) → pendiente SETUP-01.

---

## 7. BLOQUEANTES / PENDIENTES

1. **Gate del primer pago** ($1.150 con cupón OFF150) antes de construir en producción.
2. **Fase 0** (Henry + Francisco), 7 puntos — los críticos: congelar códigos G, precios vigentes, **verificar las 24 URLs de fichas**, **alta WABA + 6 números**, **someter 5 plantillas a Meta** (camino crítico externo), política de base histórica, dedup del catálogo del panel.
3. Nada se publica hasta verificar los drafts en la UI.
4. Riesgo abierto del handoff: la migración a WABA oficial probablemente no existe (los tags `wa: +51…` son firma de GoGHL multidevice) → las "6 plantillas aprobadas" seguramente hay que re-someterlas.

## 8. SIGUIENTE PASO SUGERIDO
Construir por API el resto de workflows deterministas reutilizando el método validado (leer esquema de nodo existente → adaptar → crear draft → verificar): **LS01** (captura Meta + atribución), **SP09–SP12** (pagos y cierres), **AP01–AP04**, **PS01–PS03**. Los bots quedan para UI/Playwright.
