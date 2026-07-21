# Auditoría de subcuenta GHL — Grupo GALK

- **Fecha de auditoría:** 2026-07-21
- **Location ID:** `YN2uRSDcNeBdTWm3UPCU`
- **Método:** CLI GoHighLevel del repo (rama de instalación `claude/installation-config-7vsh0l`), API pública v2 (`services.leadconnectorhq.com`) con Private Integration Token. **Solo lectura** — únicamente `GET` y `POST` a endpoints `*/search`. No se creó, modificó ni borró nada.
- **Baseline de comparación:** snapshot del 2026-07-20 indicado en el encargo.

## Resumen ejecutivo (delta vs. baseline 20-jul)

| Área | Baseline 20-jul | Hoy 21-jul | Delta |
|---|---|---|---|
| Workflows | ~40 | **40** (33 published, 7 draft) | Sin cambios; ninguno tocado desde el 19-jul |
| Custom fields | Sin MODALIDAD ni HORARIO (2/4) | **14 campos**; MODALIDAD y HORARIO siguen sin existir | Sin cambios (sigue 2/4) |
| Tags | 41, triplicado flyer-horarios, tags `wa: +51…` | **41**; triplicado y 6 tags `wa:` intactos | Sin cambios |
| Oportunidades | 2,231 todas open, 91.5% "En riesgo" | **2,369** todas open, **92.1%** "En riesgo" | **+138** oportunidades (261 creadas desde el 20-jul 00:00 UTC) |
| Calendarios | 18, con duplicados y residuos bakery | **20** | **+2** calendarios (personales) |
| Custom values | 4 genéricos vacíos | **4** genéricos vacíos | Sin cambios |
| Contactos | 10,698 | **10,895** | **+197** contactos |
| Contaminación snapshot | workout / Bakery / Dunder Mifflin | Todo sigue presente | Sin limpieza realizada |

**Lo único que cambió desde el baseline es volumen operativo** (nuevos leads → contactos, oportunidades y 2 calendarios personales). No hubo cambios de configuración: ningún workflow nuevo o modificado, ningún campo nuevo, mismos tags, mismos custom values, y toda la contaminación del snapshot sigue ahí.

---

## 1. Workflows — 40 total (33 published, 7 draft)

Última modificación más reciente: **2026-07-19**. **Ningún workflow fue creado ni modificado después del baseline del 20-jul.**

| Estado | Últ. modif. | Creado | Nombre |
|---|---|---|---|
| draft | 2026-07-19 | 2026-07-08 | FICHA - Drywall Avanzado |
| published | 2026-07-19 | 2026-06-19 | WF2 \| Round Robin → Asignar Asesor |
| draft | 2026-07-19 | 2026-07-07 | FICHA - Melamina Avanzado |
| draft | 2026-07-19 | 2026-07-11 | FICHA - Electricidad |
| draft | 2026-07-19 | 2026-07-08 | FICHA - Drywall |
| draft | 2026-07-16 | 2026-07-10 | HORARIOS - Drywall |
| draft | 2026-07-16 | 2026-07-06 | FICHA - Melamina |
| published | 2026-07-15 | 2026-06-19 | WF1 \| IA Califica el Lead |
| published | 2026-07-13 | 2026-07-09 | ALERTA - Pago por verificar |
| published | 2026-07-13 | 2026-07-13 | AVISO - Lead transferido a humano |
| published | 2026-07-11 | 2026-07-02 | CAMPOS 24 - Electricidad |
| published | 2026-07-10 | 2026-07-10 | HORARIOS - Drywall Avanzado |
| published | 2026-07-10 | 2026-07-09 | HORARIOS - Melamina Avanzado |
| published | 2026-07-10 | 2026-07-09 | HORARIOS - Melamina |
| published | 2026-07-08 | 2026-07-02 | CAMPOS 06 - G28 |
| published | 2026-07-08 | 2026-07-02 | CAMPOS 02 - Drywall |
| published | 2026-07-08 | 2026-07-02 | CAMPOS 04 - G16 |
| published | 2026-07-07 | 2026-07-02 | CAMPOS 01 - Melamina |
| published | 2026-07-04 | 2026-07-02 | CAMPOS 03 - G13 |
| published | 2026-07-04 | 2026-07-02 | CAMPOS 07 - Surco |
| published | 2026-07-03 | 2026-07-02 | CAMPOS 13 - Whatsapp |
| published | 2026-07-03 | 2026-07-02 | CAMPOS 12 - Facebook |
| published | 2026-07-03 | 2026-07-02 | CAMPOS 11 - Instagram |
| published | 2026-07-03 | 2026-07-02 | CAMPOS 10 - TikTok |
| published | 2026-07-03 | 2026-07-02 | CAMPOS 09 - Arequipa |
| published | 2026-07-03 | 2026-07-02 | CAMPOS 08 - Olivos |
| published | 2026-07-03 | 2026-07-02 | CAMPOS 05 - G24 |
| published | 2026-07-03 | 2026-06-19 | WF4 \| Seguimiento Anti-fuga |
| published | 2026-07-03 | 2026-06-24 | WF5 \| Reasignación Automática |
| published | 2026-07-03 | 2026-06-19 | WF3 \| Notificación al Asesor |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 21 - Espacios Comerciales |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 23 - Mobiliario |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 22 - AutoCAD |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 20 - Cocinas |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 19 -  Revit BIM |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 18 -  Interiorismo |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 17 - Gestión Melamina |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 15 - Origen Facebook |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 16 - Origen Instagram |
| published | 2026-07-02 | 2026-07-02 | CAMPOS 14 - SketchUp + Render |

Nota: los 5 drafts de "FICHA" y "HORARIOS - Drywall" siguen sin publicar desde antes del baseline.

## 2. Custom fields — 14 (todos de contacto)

| Tipo | Field key | Nombre |
|---|---|---|
| LARGE_TEXT | `contact.message` | Message |
| TEXT | `contact.cdigo_exacto` | CÓDIGO_EXACTO |
| SINGLE_OPTIONS | `contact.perfil_tipo` | Perfil Tipo |
| RADIO | `contact.how_often_do_you_normally_workout` | How often do you normally workout? ⚠️ *residuo de snapshot* |
| TEXT | `contact.asesor_asignado` | Asesor Asignado |
| DATE | `contact.ltima_interaccin_asesor` | Última Interacción Asesor |
| NUMERICAL | `contact.confianza_ia` | Confianza IA |
| SINGLE_OPTIONS | `contact.origen_lead` | ORIGEN_LEAD |
| SINGLE_OPTIONS | `contact.calificacin_lead` | Calificación Lead |
| DATE | `contact.fecha_asignacin` | Fecha Asignación |
| TEXT | `contact.servicio_identificado` | SERVICIO_IDENTIFICADO |
| NUMERICAL | `contact.precio_curso` | PRECIO_CURSO |
| TEXT | `contact.plataforma_origen` | PLATAFORMA_ORIGEN |
| TEXT | `contact.sede_especificada` | SEDE_ESPECIFICADA |

- **MODALIDAD: NO existe.** **HORARIO: NO existe.** → Se confirma el baseline: la calificación de datos sigue en **2 de 4**.
- No se creó ningún campo nuevo desde el baseline.

## 3. Tags — 41 (igual que baseline)

- **Triplicado confirmado:** `flyer-horarios-enviado` / `flyers-horarios-enviado` / `flyers-horarios-enviados` (3 variantes del mismo concepto; no son duplicados exactos de nombre, son variantes).
- **Tag basura adicional:** `equipo-interno ficha-melamina-enviada` (dos tags concatenados en uno, con espacio).
- **6 tags `wa: +51…` de GoGHL** (números de WhatsApp como tags): `wa: +51940177398`, `wa: +51956359766`, `wa: +51964364799`, `wa: +51967948899`, `wa: +51974386585`, `wa: +51979338376`.
- Tags genéricos de snapshot/CRM que conviven con la nomenclatura propia: `assigned`, `customer`, `subscriber`, `warm lead`, `high priority`, `follow-up`, `first_contact_sent`.

Lista completa (41): another-device-replied-whatsapp, asesor asignado, asesor-notificado, asignado-canal-directo, assigned, calificación lead, cliente_convertido, contactado, customer, equipo-interno, "equipo-interno ficha-melamina-enviada", fb-ad-lead-whatsapp, fecha asignación, ficha-drywall-avanzada-enviada, ficha-drywall-enviada, ficha-electricidad-enviada, ficha-melamina-avanzada-enviada, ficha-melamina-enviada, first_contact_sent, flyer-horarios-enviado, flyers-horarios-enviado, flyers-horarios-enviados, follow-up, high priority, ia-calificado, inbound whatsapp, instagram-ad-lead-whatsapp, lead-calificado, pago-por-verificar, reasignado, sin-contacto, subscriber, transferido-humano, wa: +51940177398, wa: +51956359766, wa: +51964364799, wa: +51967948899, wa: +51974386585, wa: +51979338376, warm lead, whatsapp group.

## 4. Pipeline y oportunidades

**1 pipeline:** `[GALK] Cursos y Capacitaciones` (`95f7TlUen51QyUax2pji`) con 7 etapas: Nuevo Lead, Calificado, En contacto, En riesgo, Ganado, Perdido, Pagó.

**2,369 oportunidades — el 100% en estado `open`** (0 won, 0 lost, 0 abandoned):

| Etapa | Oportunidades | % |
|---|---|---|
| En riesgo | 2,183 | 92.1% |
| Calificado | 186 | 7.9% |
| Nuevo Lead / En contacto / Ganado / Perdido / Pagó | 0 | 0% |

**Delta vs. baseline:** +138 oportunidades netas (2,231 → 2,369); **261 creadas desde el 2026-07-20** (UTC). La concentración en "En riesgo" *empeoró* de 91.5% a 92.1%. Rango de creación: 2026-07-03 a 2026-07-21. Nadie marca won/lost: la etapa "Pagó" y "Ganado"/"Perdido" siguen en cero, lo que confirma que el pipeline no se está gestionando manualmente.

## 5. Calendarios — 20 (baseline: 18, **+2**)

| Calendario | Activo | Observación |
|---|---|---|
| Schedule an Appointment | ✔ | Genérico de snapshot |
| Specialty Bread Baking | ✘ | ⚠️ residuo panadería |
| Custom Cake Design | ✘ | ⚠️ residuo panadería |
| Daily Fresh Pastries | ✘ | ⚠️ residuo panadería |
| Bakery Catering Services | ✘ | ⚠️ residuo panadería |
| Lucía Galvez's Personal Calendar | ✔ | **Duplicado** (aparece 2 veces, ids `G0qp37g2…` y `xZkwShzq…`) |
| Alejandra Díaz's Personal Calendar | ✔ | **Triplicado por typos**: "Alejandra Díaz", "Alejandra Días", "Alenjandra Díaz" (3 calendarios distintos para la misma persona) |
| Diana Burgos, Camila Borrero, Henrry Buenano, Maria Vilca, german borrello, Francisco Prueba, oliver guerrero, Rosa Araujo, Pablo Chavez, Gabriela Montañez (personales) | ✔ | 10 calendarios personales de asesores; "Francisco Prueba" parece cuenta de prueba |

Los +2 vs. baseline son calendarios personales (la API de listado no expone fecha de creación, así que no se puede determinar cuáles exactamente se agregaron después del 20-jul; los candidatos obvios son los duplicados de Lucía Galvez / variantes de Alejandra Díaz).

## 6. Custom values — 4 (igual que baseline: genéricos y vacíos)

| Nombre | Valor |
|---|---|
| Hours of Operation | *(vacío)* |
| Promotion Name | *(vacío)* |
| Marketing - New Booking Thank You Page URL | *(vacío)* |
| Marketing - Website Booking Page URL | *(vacío)* |

## 7. Contactos — 10,895 total (baseline: 10,698, **+197**)

% de llenado sobre muestra de **500 contactos** (los 500 más recientes que devuelve `/contacts/search` en orden por defecto; `dateAdded` entre 2026-07-19 y 2026-07-21 — es decir, la muestra refleja la calidad de datos de los leads *nuevos*, no del histórico):

| Campo | Llenado | % |
|---|---|---|
| SERVICIO_IDENTIFICADO | 366/500 | 73.2% |
| Calificación Lead | 368/500 | 73.6% |
| ORIGEN_LEAD | 342/500 | 68.4% |
| PRECIO_CURSO | 265/500 | 53.0% |
| SEDE_ESPECIFICADA | 258/500 | 51.6% |
| Asesor Asignado (custom field) | 0/500 | **0.0%** |
| Fecha Asignación (custom field) | 0/500 | **0.0%** |
| *(referencia: campo nativo `assignedTo`)* | 368/500 | 73.6% |

Hallazgo relevante: los custom fields **Asesor Asignado** y **Fecha Asignación** están en 0% en los leads recientes, mientras el campo nativo `assignedTo` sí se llena (73.6%) — la asignación ocurre (WF2 Round Robin) pero **no se está escribiendo en los custom fields** que la nomenclatura del sistema espera.

## 8. Contaminación de snapshot — sigue presente, sin limpieza

| Ítem | Estado |
|---|---|
| Custom field "How often do you normally workout?" | ✔ Presente (`contact.how_often_do_you_normally_workout`, tipo RADIO) |
| Funnels "Bakery" | ✔ Presentes: **"Bakery"** y **"Bakery Offer"** (2 funnels) |
| Calendarios de panadería | ✔ Presentes: 4 (Specialty Bread Baking, Custom Cake Design, Daily Fresh Pastries, Bakery Catering Services), todos inactivos |
| Business "(Example) Dunder Mifflin" | ✔ Presente, junto a **"(Example) Goliath National Bank"** y **"(Example) MacLarens Pub"** (3 businesses de ejemplo en total) |
| Custom values genéricos | ✔ Los 4 siguen vacíos y sin renombrar |
| Tags genéricos (customer, subscriber, warm lead…) | ✔ Presentes |

## 9. Lista de cambios desde el baseline (20-jul → 21-jul)

1. **+197 contactos** (10,698 → 10,895) — flujo normal de leads.
2. **+138 oportunidades netas** (2,231 → 2,369); 261 creadas desde el 20-jul, todas `open`. Concentración en "En riesgo" subió de 91.5% a 92.1%.
3. **+2 calendarios** (18 → 20), personales.
4. **Workflows: cero cambios.** Ninguno creado ni modificado después del 19-jul (los 5 drafts FICHA/HORARIOS siguen sin publicar).
5. **Custom fields: cero cambios.** MODALIDAD y HORARIO siguen sin crearse (calificación se mantiene en 2/4).
6. **Tags: cero cambios** (41, con el triplicado flyer-horarios y los 6 `wa: +51…` intactos).
7. **Custom values: cero cambios** (4 genéricos vacíos).
8. **Contaminación de snapshot: cero limpieza** (workout, Bakery ×2 funnels + 4 calendarios, 3 businesses de ejemplo).

---

*Notas metodológicas: total de oportunidades tomado de `meta.total` de `/opportunities/search` paginado completo (2,369 registros descargados). Total de contactos de `total` de `POST /contacts/search`. La muestra de contactos es no aleatoria (los 500 más recientes). La API de listado de calendarios no expone fechas de creación. No se usó el token de Firebase (API interna); toda la auditoría se hizo con la API pública en modo lectura.*
