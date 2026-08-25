# Ticket para soporte GHL — 24-ago-2026

> Location: **YN2uRSDcNeBdTWm3UPCU** (GRUPO GALK). Copiar/pegar el texto según el idioma
> del agente. Los dos problemas son independientes; conviene reportarlos por separado.

---

## Problema 1 — Las acciones Contact Info de Conversation AI se ejecutan de forma intermitente

**Texto para soporte (ES):**

> En la subcuenta YN2uRSDcNeBdTWm3UPCU, las acciones "Contact Info" de nuestro agente de
> Conversation AI (BOT-00 Secretaria GALK) se ejecutan de forma INTERMITENTE. El bot
> responde siempre correctamente, pero sus acciones de captura a veces corren todas, a
> veces solo la primera de la lista, y a veces ninguna — con la misma configuración, sin
> ningún cambio entre una prueba y otra. El 24 de agosto documentamos 6 pruebas en ~1 hora:
> solo 2 ejecutaron todas las acciones (ejemplos: contacto bonqXmMcD3lK57QrCzmX 15:08 UTC =
> cero acciones ejecutadas; contacto l4BhaZZgkYzd9o2BwsYI 16:16 UTC = todas OK; contacto
> rG6ClkSaa0E5H19avcvb 16:31 UTC = cero). Borramos y recreamos las acciones y persiste.
> ¿Hay un incidente conocido con la ejecución de acciones de Conversation AI?

**EN:** In sub-account YN2uRSDcNeBdTWm3UPCU, our Conversation AI agent's "Contact Info"
actions execute INTERMITTENTLY. The bot always replies correctly, but its capture actions
sometimes all run, sometimes only the first in the list, sometimes none — same config, no
changes between tests. On Aug 24 we documented 6 tests within ~1 hour: only 2 executed all
actions (examples: contact bonqXmMcD3lK57QrCzmX 15:08 UTC = zero actions; l4BhaZZgkYzd9o2BwsYI
16:16 UTC = all OK; rG6ClkSaa0E5H19avcvb 16:31 UTC = zero). We deleted and recreated the
actions and it persists. Is there a known issue with Conversation AI action execution?

---

## Problema 2 — Triggers "El cliente ha respondido" con filtro de texto: enrolamiento intermitente

**Texto para soporte (ES):**

> En la misma subcuenta, los workflows con trigger "El cliente ha respondido" + filtro
> "Cuerpo del mensaje Contiene" enrolan de forma INTERMITENTE, incluso creados 100% desde
> la UI. Ejemplo reproducible: workflow "test electricidad" (adbe3751-4ea9-4b3e-898b-1dd20b430af5),
> publicado, keywords [electricidad, elec], filtro de etiqueta "pruebas demo", canal WhatsApp.
> El mismo contacto con la etiqueta enviando la keyword exacta a veces enrola y a veces no
> (24-ago: mensajes "elec" 23:00 UTC enroló, "elect"/"elec" 23:01 no, "electricidad" 23:03
> enroló, "elect" 23:04 no — el historial de inscripciones muestra solo 2 filas de ~6
> mensajes). Necesitamos saber: (a) si hay un incidente con la evaluación de estos triggers,
> y (b) la semántica exacta del operador "Contiene" del cuerpo del mensaje — en nuestras
> pruebas matchea solo PALABRAS COMPLETAS (tokens), no subcadenas ("elect" no matchea la
> keyword "elec"), y no encontramos documentación de esto.

**EN:** Same sub-account: workflows triggered by "Customer Replied" + "Message body
contains any of" enroll INTERMITTENTLY, even when built 100% in the UI. Reproducible
example: workflow "test electricidad" (adbe3751-4ea9-4b3e-898b-1dd20b430af5), published,
keywords [electricidad, elec], tag filter "pruebas demo", WhatsApp channel. The same tagged
contact sending an exact keyword sometimes enrolls and sometimes doesn't (Aug 24: "elec"
23:00 UTC enrolled; "elect"/"elec" 23:01 didn't; "electricidad" 23:03 enrolled; "elect"
23:04 didn't — enrollment history shows only 2 rows out of ~6 messages). We need to know:
(a) whether there's an incident affecting these trigger evaluations, and (b) the exact
semantics of the "contains" operator — in our tests it matches WHOLE WORDS (tokens) only,
not substrings ("elect" does not match keyword "elec"), which we couldn't find documented.

---

## Contexto por si el agente lo pide

- Número WhatsApp API oficial: +51 972 240 645 (id 1138517799350419).
- Las pruebas se hacen con contactos nuevos con etiqueta `pruebas demo` creados antes de escribir.
- Los triggers `customer_reply` heredados (workflows "CAMPOS 01-24", julio) funcionan a diario
  con el mismo patrón de filtros — el problema afecta workflows nuevos y también al de prueba
  creado hoy desde la UI.
