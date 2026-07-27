# Inventario de assets en la subcuenta — verificado 2026-07-23

> Todo lo que bots y workflows necesitan referenciar. **Estado: completo, 0 faltantes.**
> Regenerar con `.venv/bin/python scripts_ghl/auditar_faltantes.py`

---

## Campos custom NUEVOS (27) — dónde está cada uno

⚠️ **Ojo con la carpeta**: `Familia de interés` y `Curso de interés` están en **Identificación del lead**, no en Calificación.

### 📁 Identificación del lead (9)
| Campo | Key | Tipo | Opciones |
|---|---|---|---|
| Familia de interés | `contact.familia_de_inters` | SINGLE_OPTIONS | `Talleres` · `Software` · `Gestion` |
| Curso de interés | `contact.curso_de_inters` | TEXT | — |
| Fuente | `contact.fuente` | SINGLE_OPTIONS | Meta Ads · Manual · Referido · Reactivación |
| Fecha de primer contacto | `contact.fecha_de_primer_contacto` | DATE | — |
| UTM Source / Medium / Campaign | `contact.utm_source` · `contact.utm_medium` · `contact.utm_campaign` | TEXT | — |
| Anuncio (Ad Name) | `contact.anuncio_ad_name` | TEXT | — |
| Ad ID | `contact.ad_id` | TEXT | — |

### 📁 Calificación (8)
| Campo | Key | Tipo | Opciones |
|---|---|---|---|
| Modalidad | `contact.modalidad` | SINGLE_OPTIONS | `Presencial` · `Online` |
| Sede | `contact.sede` | SINGLE_OPTIONS | `Surco` · `Los Olivos` · `Arequipa` · `No aplica` |
| Horario de interés | `contact.horario_de_inters` | TEXT | — |
| Calificado | `contact.calificado` | SINGLE_OPTIONS | `Sí` · `No` |
| Fecha de calificación | `contact.fecha_de_calificacin` | DATE | — |
| Asesor asignado (nuevo) | `contact.asesor_asignado_nuevo` | TEXT | — |
| Fecha de asignación | `contact.fecha_de_asignacin` | DATE | — |
| Pack x2 | `contact.pack_x2` | SINGLE_OPTIONS | `Sí` · `No` |

### 📁 Pago y matrícula (7)
`contact.precio_cotizado` (NUM) · `contact.comprobante_recibido` (Sí/No) · `contact.comprobante_validado` (Sí/No) · `contact.validado_por` (TEXT) · `contact.fecha_de_validacin` (DATE) · `contact.fecha_de_inicio` (DATE) · `contact.grupo_whatsapp_asignado` (TEXT)

### 📁 Post-venta (3)
`contact.nota_encuesta_15` (NUM) · `contact.fecha_fin_de_taller` (DATE) · `contact.razn_de_prdida` (SINGLE_OPTIONS: Precio · Solo información · Ya se matriculó en otro lugar · No responde · Horario/sede no disponible · Sin presupuesto ahora · Otro)

> Los **14 campos heredados** (UPPERCASE, `contact.servicio_identificado`, `how_often_do_you_normally_workout`, etc.) se deprecan en SETUP-01. **No usarlos.**

---

## Tags (15 nuevos, creados ✅)

| Tag | Lo usa | Para qué |
|---|---|---|
| `enviar-ficha` | bots → SP05 | dispara el envío de la ficha |
| `lead-calificado` | bots → SP06 | dispara calificación + round robin |
| `bot-silenciado` | SP06 | marca que el asesor tomó la conversación |
| `origen-meta` | LS01 | lead entrado por CTWA |
| `recuperacion-enviada` | SP08 | ya se le mandó plantilla fuera de ventana |
| `matriculado` | SP11 | cierre ganado |
| `alumno-activo` | AP03 / AP04 | alumno en curso (guard de reprogramación) |
| `reintento-60d` | PS03 | reintento de perdidos |
| `perdido-precio` · `perdido-solo-informacion` · `perdido-ya-se-matriculo` · `perdido-no-responde` · `perdido-horario-sede` · `perdido-sin-presupuesto` · `perdido-otro` | SP12 | 7 razones de pérdida |

> Los **41 tags heredados** (triplicado flyer-horarios, `wa: +51…`, genéricos) se borran en SETUP-01.

---

## Custom Values (36 = 24 fichas + 12 operativos)

### Fichas (24) — las usa SP05
`{{custom_values.ficha_melamina_desde_cero__surco}}` y equivalentes. **Todos vacíos** hasta Fase 0.3 (URLs reales del panel RoasSeeker).

### Operativos (12) — creados ✅, todos vacíos
| Custom Value | Lo usa | Quién lo llena |
|---|---|---|
| Yape - Número | SP09 | cliente |
| Plin - Número | SP09 | cliente |
| Link de pago con tarjeta | SP09 | cliente |
| Dirección sede Surco | AP01 | cliente |
| Dirección sede Los Olivos | AP01 | cliente |
| Dirección sede Arequipa | AP01 | cliente |
| Link Zoom clases online | AP01 | cliente |
| Link reseña Google Surco | PS01 | cliente |
| Link reseña Google Los Olivos | PS01 | cliente |
| Link reseña Google Arequipa | PS01 | cliente |
| Link grupo WhatsApp | AP03 | cliente |
| Link encuesta satisfacción | PS01 | Profit (se crea el form) |

> Los **4 custom values genéricos heredados** (Hours of Operation, Promotion Name, Marketing ×2) se borran en SETUP-01.

---

## Pipeline "Ventas GALK" — `Pm48HGVyRbd5TAZDrKQS`
9 etapas: Nuevo Lead · En conversación (bot) · Ficha enviada · Calificado · Asignado a asesor · Datos de pago enviados · Pago en validación · Matriculado · Perdido.

## Workflows construidos (draft)
- **SP05** `ae78625c-8f91-4af1-a7b0-3be0b2e4a667` — árbol 24 ramas, trigger tag `enviar-ficha`
- **SP06** `84811c16-30d8-4c08-a05d-0c12fa46567d` — calificación + round robin, trigger tag `lead-calificado`

---

## ✅ Conclusión
**No falta ningún asset para armar los 4 bots.** Todo lo que las acciones necesitan referenciar
(campos, tags, custom values) ya existe en la subcuenta.

Lo único pendiente es **contenido**, no estructura: las URLs de las fichas y los datos operativos
(Yape, direcciones, links) los llena el cliente en Fase 0.
