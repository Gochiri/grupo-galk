# Ficha G25 · Taller de Electricidad y Automatización Residencial

> Contenido oficial recibido de Lucía vía Oliver el 20-ago-2026. Este es el paquete que la
> secuencia de ficha (SP05 v2) debe reproducir TAL CUAL: texto de apertura → 4 imágenes en
> orden → texto final. Ver `ACUERDOS-reunion-2026-08-19.md` §1 para la estructura.

## Mensaje 1 · Apertura (verbatim de Lucía)

```
💬 ¡Hola! ¿Cuál es tu nombre? 😊
Soy Camila de Grupo GALK y tengo una oportunidad especial para ti 🎉

Aprende una habilidad muy demandada con nuestro G25 Taller de Electricidad y Automatización Residencial ⚡💡
Un curso *100% práctico*, ideal para comenzar desde cero y desarrollar competencias reales en instalaciones eléctricas y automatización.

📌 Ofertas vigentes hasta el 24 de agosto:
✅ S/600 – separa tu vacante con S/100

📍*Sedes:* Lima-Surco (Calle Aldabas 559) o Los Olivos (Av. Antunes de Mayolo 822). Provincia-Arequipa (Calle José Santos Chocano 249– Umacollo)
🧾 Incluye: certificación, materiales y asesorías personalizadas

📸 Te comparto las imágenes del taller con toda la información y beneficios. ¡Mira lo completo que está este programa! 👇
```

## Imágenes 2-5 · En este orden (numeración de Lucía)

| # | Contenido | Archivo en `FICHAS WHATSAPP/Electricidad` (⚠️ confirmar mapeo) | URL CDN |
|---|---|---|---|
| 1 | Portada: nombre del taller, incluye herramientas+materiales, "5 días presenciales / 100% prácticas", respaldo Domótika CELSA, sedes | `Electricidad-1.jpeg` | `.../6a51b6b10e67afc013822d3f.jpeg` |
| 2 | Temario: dirigido a, 5 módulos del taller de 20 horas (fundamentos → proyecto final con Alexa), direcciones de sedes Lima, marcas que respaldan | `Electricidad-2.jpeg` | `.../6a51b6b19c9b37b5fd3f5d4a.jpeg` |
| 3 | Motivacional: "aprende a instalar, automatizar y transformar tu hogar desde cero", G25, sin experiencia previa, "descuento disponible al llevar dos talleres" | `Electricidad-3.jpeg` | `.../6a51b6b1eada8c1f450813db.jpeg` |
| 4 | Reserva y pagos: reserva S/100 (2 talleres S/200 promo), resto hasta 2 días antes, políticas (sin devoluciones, mínimo 10 alumnos, reprogramación 1-3, sin cambio de curso), cuentas BCP/BBVA/Interbank/Yape o Plin | `Electricidad-4.jpeg` | `.../6a51b6b1eada8c1f450813d7.jpeg` |

⚠️ El mapeo nombre-de-archivo ↔ contenido está ASUMIDO por el número (no puedo abrir el CDN
desde este entorno). **Oliver debe confirmar de un vistazo en el media store** que
Electricidad-1 es la portada, -2 el temario, -3 la motivacional y -4 la de pagos.

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

## Hallazgos y conflictos a resolver ANTES de armar

1. **"Yape o Plin" en la imagen 4 y nuestra KB dice "No existe Plin".** La ficha oficial
   manda: hay que corregir las 3 KB y los prompts (medios de pago: Yape o Plin al 986 780 351,
   BCP, BBVA, Interbank — o al menos que el bot no niegue Plin).
2. **La imagen 1 dice "5 días presenciales"** — contradice la regla D3 del 12-ago ("la imagen
   no lleva fechas ni duración", la puso el propio cliente) y nuestra regla de "solo horas".
   El cliente manda: se acepta tal cual, pero queda registrado el cambio de criterio. La KB
   del bot sigue con la regla de horas para el TEXTO conversacional.
3. **"Ofertas vigentes hasta el 24 de agosto"** en el texto de apertura: es contenido
   perecedero. Si va literal en la plantilla WABA, cada cambio de fecha/precio = re-aprobación
   de Meta (~1 día). Recomendación: plantilla con **variables** ({{fecha}}, {{precio}}) para
   que Francisco actualice mensualmente sin re-aprobar.
4. **La secuencia se presenta como "Camila de Grupo GALK"** — persona con nombre. Los prompts
   v4 de los bots deben hablar como Camila (o al menos no contradecirla) para que el lead no
   note el cambio de "voz".
5. **La apertura ya pide el nombre** y el mensaje final condiciona los horarios a confirmarlo.
   El BOT-00 deja de preguntar nombre en este camino; el bot de familia que se enciende tras
   la ficha debe capturar nombre + sede de la respuesta.
6. **Políticas nuevas para las KB** (salen de la imagen 4, el bot debe saberlas para responder
   dudas sin inventar): sin devoluciones de reserva; mínimo 10 alumnos (si no, se reprograma
   hasta en 1-3 oportunidades); no se permite cambio de curso tras confirmar inscripción;
   el saldo se paga hasta 2 días antes del inicio; certificado respaldado por Grupo Galk y
   marcas aliadas; direcciones exactas de las sedes.
7. **Precio confirmado**: S/600 (promo vigente) y reserva S/100 — coincide con la KB actual
   (S/780 regular / S/600 promo / reserva S/100). El "descuento al llevar dos talleres"
   (imagen 3) es el Pack: reserva S/200 según imagen 4.
