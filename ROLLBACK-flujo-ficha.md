# Qué se cambió para la demo y cómo volver atrás

> ## 🟢 DECISIÓN TOMADA — 12-ago-2026: no hay rollback
>
> Lucía lo confirmó en la reunión: *"lo que es horarios sí sería bueno que obviamente lo maneje el
> vendedor, porque nosotros cambiamos horarios una vez a la semana"*. El modo demo se queda.
>
> Este documento pasa a ser **histórico**. Se conserva porque describe exactamente qué se tocó, y
> porque BOT-02 y BOT-03 **todavía están en el flujo viejo de 4 datos** y hay que pasarlos al nuevo
> usando la tabla de §"Lo manual" al revés. Ver `ACUERDOS-reunion-2026-08-12.md`.
>
> Los prompts vigentes son los de `guias-bots/PROMPTS-bots-v3.md`.

> El cambio "el asesor da los horarios" era **provisional** hasta que el cliente lo confirmara.
> Aquí está todo lo que se tocó y cómo revertirlo. Nada de esto es destructivo.

## Lo automático — un comando

```bash
.venv/bin/python scripts_ghl/toggle_flujo.py demo      # asesor da horarios
.venv/bin/python scripts_ghl/toggle_flujo.py original  # bot manda la ficha
```

Cambia dos cosas: la **notificación de SP06** al asesor y el bloque **`## Horarios`** de las
3 Knowledge Base. Probado en las dos direcciones.

⚠️ Si estabas en modo demo y vuelves a `original`, **hay que volver a subir las 3 KB a los
bots**: los archivos del repo cambian, los de GHL no se actualizan solos.

---

## Lo manual — 4 cosas de UI

| # | Qué | Modo DEMO (3 datos) | Modo ORIGINAL (4 datos) | Tiempo |
|---|---|---|---|---|
| 1 | **Prompt de cada bot** | El `## Goal` pide 3 datos + bloque *HORARIOS Y FECHAS* | Los prompts de las tarjetas de ClickUp `wdx6zequw1` / `wdx6zequwe` / `wdx6zequwq`, que siguen con la versión de 4 datos | 2 min/bot |
| 2 | **Action Contact Info** | 3 campos: Curso · Modalidad (bot) · Sede (bot) | + 4.º campo `Horario de interés` (config en `wdx6zequvz`) | 2 min/bot |
| 3 | **Action Trigger a Workflow → SP05** | **no se crea** | Crear la acción → `SP05 | Envío de ficha` (config en `wdx6zequw2`) | 3 min/bot |
| 4 | **SP05 publicado** | queda en **draft** | Publicar | 30 seg |

**Las tarjetas de ClickUp siguen con la versión original de 4 datos** — a propósito. Son el
respaldo del rollback: si hay que volver, se copia de ahí y ya está.

---

## Por qué SP05 no hay que "desactivar"

**Ya está inerte por construcción.** Su trigger es el tag `enviar-ficha`, y verificado el
11-ago: **ningún workflow lo agrega** — ni los 25 nuestros ni los 40 de Francisco. La única
forma de que SP05 corriera sería que un bot lo disparara con la acción *Trigger a Workflow*,
y esa acción **no se va a crear** en el modo demo.

O sea: no hay nada que apagar. SP05 está en draft, sin nadie que lo llame, y sus 24 ramas y
sus 24 custom values quedan intactos esperando la decisión del cliente.

---

## Lo que NO cambia en ninguno de los dos modos

Esto conviene tenerlo claro para la reunión: **el cambio toca muy poco del sistema**.

- **BOT-00** — su prompt ya dice *"NO cotizas. NO das horarios. NO envías fichas."* Nunca
  manejó horarios, así que no se toca en ninguno de los dos modos.
- **SP06** — la lógica es idéntica. Quién decide si el lead está listo es el **bot**, no SP06.
  Solo cambia el texto de la notificación.
- **WF-NORM-1..4** — normalizan Familia, Modalidad, Sede y Pack x2. Ninguno toca el horario.
- **El campo `Horario de interés`** — sigue existiendo. En modo demo simplemente lo llena el
  asesor a mano en vez del bot.
- **Todo lo de pago en adelante** (SP09 → SP12, AP01-04, PS01-03) — sin cambios.

---

## Estado actual

**Modo DEMO aplicado** el 11-ago:
- ✅ SP06 con la notificación nueva
- ✅ Las 3 KB con el bloque de Horarios nuevo (**hay que subirlas a los bots**)
- ⬜ Prompts — los pega Oliver
- ⬜ Contact Info sin el 4.º campo — lo configura Oliver
- ⬜ SP05 sigue en draft y sin acción que lo llame ← correcto, no tocar
