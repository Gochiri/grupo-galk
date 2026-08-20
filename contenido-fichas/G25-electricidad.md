# Ficha G25 · Taller de Electricidad y Automatización Residencial

> Contenido oficial recibido de Lucía vía Oliver el 20-ago-2026. Este es el paquete que la
> secuencia de ficha (SP05 v2) debe reproducir TAL CUAL: texto de apertura → 4 imágenes en
> orden → texto final. Ver `ACUERDOS-reunion-2026-08-19.md` §1 para la estructura.

## Mensaje 1 · Apertura (v2, recibida el 20-ago — REEMPLAZA a la primera)

Diferencia única con la v1: "Ofertas vigentes **hasta el 24 de agosto**" pasó a "Ofertas
vigentes **por tiempo limitado**" — el cliente mismo la hizo perenne, lo que resuelve el
problema de la fecha perecedera en la plantilla WABA (hallazgo 3). Nombre de vendedora
reemplazado por **Valeria**. Texto final a usar:

```
💬 ¡Hola! ¿Cuál es tu nombre? 😊
Soy Valeria de Grupo GALK y tengo una oportunidad especial para ti 🎉

Aprende una habilidad muy demandada con nuestro G25 Taller de Electricidad y Automatización Residencial ⚡💡
Un curso *100% práctico*, ideal para comenzar desde cero y desarrollar competencias reales en instalaciones eléctricas y automatización.

📌 Ofertas vigentes por tiempo limitado:
✅ S/600 – separa tu vacante con S/100

📍*Sedes:* Lima-Surco (Calle Aldabas 559) o Los Olivos (Av. Antunes de Mayolo 822). Provincia-Arequipa (Calle José Santos Chocano 249– Umacollo)
🧾 Incluye: certificación, materiales y asesorías personalizadas

📸 Te comparto las imágenes del taller con toda la información y beneficios. ¡Mira lo completo que está este programa! 👇
```

## Imágenes 2-5 · En este orden (numeración de Lucía)

| # | Contenido | Archivo en `FICHAS WHATSAPP/Electricidad` | URL CDN |
|---|---|---|---|
| 1 | Portada: nombre del taller, incluye herramientas+materiales, "5 días presenciales / 100% prácticas", respaldo Domótika CELSA, sedes | `Electricidad-3.jpeg` | `.../6a51b6b1eada8c1f450813db.jpeg` |
| 2 | Temario: dirigido a, 5 módulos del taller de 20 horas (fundamentos → proyecto final con Alexa), direcciones de sedes Lima, marcas que respaldan | `Electricidad-2.jpeg` | `.../6a51b6b19c9b37b5fd3f5d4a.jpeg` |
| 3 | Motivacional: "aprende a instalar, automatizar y transformar tu hogar desde cero", G25, sin experiencia previa, "descuento disponible al llevar dos talleres" | `Electricidad-1.jpeg` | `.../6a51b6b10e67afc013822d3f.jpeg` |
| 4 | Reserva y pagos: reserva S/100 (2 talleres S/200 promo), resto hasta 2 días antes, políticas (sin devoluciones, mínimo 10 alumnos, reprogramación 1-3, sin cambio de curso), cuentas BCP/BBVA/Interbank/Yape o Plin | `Electricidad-4.jpeg` | `.../6a51b6b1eada8c1f450813d7.jpeg` |

✅ **Mapeo confirmado por Oliver el 20-ago mirando el media store.** Ojo: el número del
archivo NO es el orden de envío — la portada es `Electricidad-3` y la motivacional es
`Electricidad-1`. El orden de envío es el de esta tabla.

### Textos cortos por imagen (BORRADOR nuestro — pendiente de aprobar con Lucía)

Cada plantilla WABA de imagen exige un texto. Propuesta corta y alusiva (acordado en la
reunión 19-ago, 39:13):

1. `⚡ Así se vive el taller — 100% práctico y presencial`
2. `📚 Temario completo: las 20 horas, paso a paso`
3. `💪 Empiezas desde cero, sales instalando y automatizando`
4. `📝 Reserva tu vacante con S/100 — medios de pago`

## Mensaje final (verbatim de Lucía)

```
⭐ Una vez que me confirmes tu nombre, te envío los horarios y fechas disponibles en la sede que te quede más cerca.
¿Te interesa en Surco, Los Olivos o Provincia Arequipa? 😊
```

## Hallazgos y decisiones (cerrados el 20-ago con Oliver)

1. **Plin — RESUELTO: se deja tal cual.** El cliente dijo expresamente el 5-ago que GALK no
   maneja Plin (consta en `INVENTARIO-assets-ghl.md`), y su ficha oficial dice "Yape o Plin".
   Info contradictoria del propio cliente → la ficha se envía como la mandaron y la KB no se
   toca; es responsabilidad del cliente unificar su info.
2. **"5 días presenciales" en la imagen 1 — aceptado tal cual** (las imágenes son del
   cliente). La KB del bot sigue con la regla de horas para el texto conversacional.
3. **"Ofertas vigentes hasta el 24 de agosto" — se queda literal.** El mantenimiento mensual
   de plantillas es de Francisco (actualizar texto y re-aprobar). La idea de variables
   {{fecha}}/{{precio}} se le puede proponer, pero la implementa él si la quiere.
4. **Nombre unificado del bot: Valeria** (decisión Oliver 20-ago). Los textos de todas las
   fichas reemplazan el nombre de vendedora (Camila, Rosa...) por Valeria, y el prompt de
   BOT-00 la presenta así (ver `BOT-00-guia-armado.md` · Personality).
5. **La apertura ya pide el nombre** y el mensaje final condiciona los horarios a confirmarlo.
   El BOT-00 deja de preguntar nombre en este camino; el bot de familia que se enciende tras
   la ficha debe capturar nombre + sede de la respuesta.
6. **Arequipa — RESUELTO (20-ago): sí se ofrece.** La regla "electricidad solo Lima" la
   habíamos DEDUCIDO de la plataforma de horarios (no fue afirmación del cliente, a
   diferencia del Plin), y la ficha oficial trae Arequipa con dirección → la ficha manda.
   Corregido en KB-01, PROMPTS-v3, PROMPTS-especialistas y ACCIONES. Oliver actualiza la
   línea en el prompt del BOT-01 en la UI y re-sube KB-01.
6. **Políticas nuevas para las KB** (salen de la imagen 4, el bot debe saberlas para responder
   dudas sin inventar): sin devoluciones de reserva; mínimo 10 alumnos (si no, se reprograma
   hasta en 1-3 oportunidades); no se permite cambio de curso tras confirmar inscripción;
   el saldo se paga hasta 2 días antes del inicio; certificado respaldado por Grupo Galk y
   marcas aliadas; direcciones exactas de las sedes.
7. **Precio confirmado**: S/600 (promo vigente) y reserva S/100 — coincide con la KB actual
   (S/780 regular / S/600 promo / reserva S/100). El "descuento al llevar dos talleres"
   (imagen 3) es el Pack: reserva S/200 según imagen 4.
