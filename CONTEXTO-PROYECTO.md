# Contexto del proyecto — Grupo GALK · Implementación GHL

> Para cualquiera del equipo que entre a construir. Explica **qué problema resolvemos**,
> **qué prometimos** y **por qué existe cada pieza** que estamos armando.
> Detalle técnico (IDs, keys): ver `guias-bots/INVENTARIO-assets-ghl.md` y `HANDOFF-SESION-2026-07-23.md`.

---

## 1. Quién es quién

| Rol | Quién |
|---|---|
| Cliente final | **Grupo GALK** — instituto técnico en Perú. Talleres presenciales (melamina, drywall, electricidad) en Surco, Los Olivos y Arequipa + cursos online por Zoom. 6 asesoras + Lucía (supervisora). |
| Cliente directo | **Francisco Rodríguez** — agencia. Ya había implementado GHL para GALK. Su socio **Vicente** maneja la pauta de Meta. |
| Nosotros | **Profit Technology** — Henry (dirección), Germán y Oliver (construcción). |

**Le vendemos a Francisco, no a GALK.** Francisco se queda el 100% de la mensualidad que le cobre
a GALK; nosotros cobramos **$2,450 una sola vez** ($1,150 al arrancar + $1,300 contra entrega).

---

## 2. El problema real

GALK metió pauta agresiva en Meta y generó **~10,900 contactos en un mes**. El sistema no aguantó:

- **6 asesoras con ~600 mensajes/día.** Conversaciones sin responder por días.
- **2,370 oportunidades, 100% abiertas.** Ninguna cerrada, ni ganada ni perdida.
- **92% apiladas en "En riesgo"** — un anti-fuga las barre ahí y se quedan a morir.
- **S/ 1.3 millones flotando** sin gestionar.
- **GoGHL** (WhatsApp no oficial) → ya les bloquearon números.
- Horarios que cambian cada semana, actualizados a mano workflow por workflow.

### Los dos hallazgos de la auditoría que definen el proyecto

1. **El round robin asigna la oportunidad pero no escribe en el contacto.**
   Campo "Asesor asignado" al **0% sobre 500 contactos**. Nadie sabe de quién es cada lead.
2. **Faltaban los campos de modalidad y horario** → el sistema calificaba con **2 de 4 datos**.

---

## 3. Qué prometimos

| Promesa | Cómo se cumple |
|---|---|
| Ningún lead sin responder | Bots de IA 24/7 en WhatsApp **oficial** (WABA + 6 números) |
| Solo leads calificados a las asesoras | El bot no transfiere sin los **4 datos**: curso + modalidad + sede + horario |
| Saber siempre de quién es cada lead | Round robin que **escribe en el contacto** |
| Que el pipeline cierre | 9 etapas con ganado/perdido y **razón obligatoria** |
| Optimizar la pauta hacia compradores | Eventos **CAPI** a Meta |
| Horarios actualizables una vez | El panel **RoasSeeker** cambia la ficha y todo el sistema la toma sola |

Incluye alta de WABA con 6 números, 2 capacitaciones, 2 puestas a punto y limpieza del
snapshot contaminado.

---

## 4. El recorrido del lead, de punta a punta

```
Anuncio Meta → WhatsApp
   ↓
LS01  captura atribución (UTMs, anuncio) + crea la oportunidad
   ↓
BOT-00 (Secretaria)  saluda, pide nombre, detecta la FAMILIA
   ↓  Transfer Bot nativo
BOT-01 Talleres  /  BOT-02 Software  /  BOT-03 Gestión
   ↓  conversa: curso → sede/modalidad
SP05  manda la ficha correcta (24 combinaciones) desde un Custom Value
   ↓  el lead elige horario → 4/4 datos completos
SP06  CALIFICA → round robin 6 asesoras → escribe el asesor EN EL CONTACTO
      → notifica al asesor → silencia al bot
   ↓  a partir de aquí es humano
SP09 datos de pago → SP10 valida comprobante (Lucía) → SP11 Matriculado
   ↓
AP01 confirmación · AP02 recordatorios · AP03 grupo WhatsApp · AP04 reprogramación
   ↓
PS01 encuesta y reseña · PS02 venta cruzada · PS03 reintento a 60 días
```

---

## 5. Por qué existe cada pieza

| Pieza | Problema que resuelve |
|---|---|
| **4 bots separados, KB propia cada uno** | Que un bot no pueda cotizar precio de otra sede o curso. Imposible **por diseño**, no por prompt. |
| **Los 27 campos custom** | Modalidad, Sede y Horario **no existían** → calificaban 2 de 4. |
| **SP06 escribiendo en el contacto** | Es *el* fix del bug nº1. Sin eso nadie sabe de quién es el lead. |
| **Pipeline de 9 etapas** | El viejo no tenía etapas de pago ni cierre real → nada se cerraba. |
| **SP05: 24 ramas + Custom Values** | Antes las URLs estaban hardcodeadas en 24 workflows: cambiar una ficha = editar 24. Ahora se edita un custom value. |
| **SP12 con 7 razones de pérdida** | Para que exista un "perdido" con causa y se pueda reintentar a 60 días. |
| **WF-NORM y los campos `(bot)`** | Parche técnico: las acciones de Conversation AI no escriben en dropdowns. |
| **Auto Followup en los bots** | Sustituye a SP07, que habría **dormido al bot** cada vez que disparaba. |
| **Transfer Bot nativo** | Sustituye a WF-DERIV: GHL maneja el sleep al transferir, sin hacks de timing. |

---

## 6. Las tres reglas que gobiernan todo

**1. Reconstrucción total (§3).** Nada de lo de Francisco se edita ni se reutiliza. Todo lo nuestro
es aditivo; lo viejo se archiva al final. Razón: que la garantía cubra el sistema completo sin
asteriscos, sin que nadie pueda decir "es que esa pieza ya venía así".

**2. Todo en DRAFT.** La subcuenta está **en producción con 10,900 contactos reales**. Nada se
publica sin revisión humana.
> Esto ya nos salvó: SP06 iba a escuchar el tag `lead-calificado`, que el workflow **vivo** de
> Francisco (WF1) le pone a leads reales. Publicarlo habría movido oportunidades reales y
> notificado a las 6 asesoras. Se cambió a `galk-bot-calificado`.

**3. Cero URLs hardcodeadas.** Todo por Custom Values.

---

## 7. Estado actual

**Construido:** pipeline de 9 etapas · 31 campos custom · 36 custom values · 15 tags ·
**20 workflows** (todos draft, en carpetas `GALK 2.0 ·`) · 3 CSVs de Knowledge Base ·
todas las tareas de ClickUp con su configuración exacta.

**Bloqueado por Fase 0:** alta de WABA + 6 números y las 5 plantillas aprobadas por Meta
(trámite externo, camino crítico) · congelar el catálogo del panel · las 24 URLs de fichas.
Sin eso los workflows tienen placeholders y los bots no se pueden desplegar.

**Entrega comprometida:** miércoles 5 de agosto.

---

## 8. Riesgos vivos

1. **WABA/plantillas** — la migración a WhatsApp oficial probablemente **no existe** (los tags
   `wa: +51…` son firma de GoGHL multidevice). Las "6 plantillas aprobadas" de Francisco
   seguramente hay que re-someterlas. Es el camino crítico.
2. **Panel RoasSeeker** — lo mantiene Francisco, fuera de nuestra garantía. Si cambia URLs, rompe SP05.
3. **Base histórica** — disparar masivo antes de tiempo quema el WABA nuevo. Solo lotes chicos, al final.
4. **Códigos G inconsistentes** entre panel y brochures → congelar antes de construir el árbol de SP05.
5. **Convivencia con el sistema viejo** — mientras no haya cutover, los 40 workflows de Francisco
   siguen corriendo sobre los mismos contactos. Cuidado con tags y campos compartidos.
