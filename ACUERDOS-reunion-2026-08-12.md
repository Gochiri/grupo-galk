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
