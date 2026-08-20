# Ficha G1 · SketchUp 2025 + V-Ray 7 + PSD + Twinmotion + IA (software)

> Contenido oficial recibido de Lucía vía Oliver el 20-ago-2026. **Primera ficha del área de
> software**, y trae DOS diferencias estructurales frente a talleres:
> 1. **Un PDF (brochure) en lugar de 4 imágenes** — está en `assets/G1-SketchUp-Brochure.pdf`
>    (⚠️ pendiente de subir al media store de GHL cuando vuelva el acceso API).
> 2. **La pregunta final es la MODALIDAD** (presencial Surco vs virtual en vivo), no la sede —
>    esto responde la pregunta abierta №2 del 19-ago para este curso.
> Además el cierre son DOS mensajes de texto separados (reserva + pregunta).

## Estructura de la secuencia

```
1. Texto de apertura
2. PDF (brochure)
3. Texto: reserva
4. Texto: pregunta de modalidad
→ activar BOT-02 (software)
```

## Mensaje 1 · Apertura

Original firmado "Camila" → nombre unificado **Valeria**. Texto final a usar:

```
📢 ¡Hola! ¿Cuál es tu nombre? 😊
Soy Valeria de Grupo GALK ✨ y quiero compartirte la información de nuestro Curso G1 | SketchUp 2025 + V-Ray 7 + PSD + twinmotion + IA 🎨💻. Aprenderás a crear renders profesionales y potenciar tus proyectos con herramientas de última tecnología. 🚀

🚀 Curso 100% práctico – Aprende desde cero con expertos.
📌 Modalidad: Virtual – En vivo por Zoom y Presencial Surco (Calle Aldabas 559)

🎁 *📌 Ofertas vigentes por tiempo limitado:
✅ S/370 modalidad online en vivo– Separa tu vacante con S/100
✅ S/550 modalidad presencial – Separa tu vacante con S/100
🛠️ Incluye certificación y asesoría personalizada

📸 Te comparto el brochure con toda la información sobre el contenido, duración y beneficios del curso. ¡Mira lo completo que está este programa! 👇
```

## Mensaje 2 · PDF

`assets/G1-SketchUp-Brochure.pdf` (694 KB) → subir a `FICHAS WHATSAPP` del media store y
enviar como `whatsapp_media` con `media_type: document`. ⚠️ El tipo *document* aún no está
validado en ejecución (el molde de la UI fue con imagen) — la primera prueba lo confirma;
si no sale, pedir a Oliver un molde de WhatsApp media con PDF y clonar.

## Mensaje 3 · Reserva

```
Reserva tu vacante con S/100 y cancela el saldo hasta 2 días antes del inicio de clases.
```

## Mensaje 4 · Pregunta final (modalidad)

```
✨ Para confirmarte el grupo ideal, cuéntame:
¿Deseas llevarlo en modalidad presencial en Surco o prefieres virtual en vivo? 😊
```

## Hallazgos

1. **Nombre nuevo del curso**: "G1 | SketchUp 2025 + V-Ray 7 + PSD + Twinmotion + IA" —
   mucho más específico que el "SketchUp + Render" de la KB. Actualizar KB-02 en su v4.
2. **Precios coinciden con la KB** (online S/370 / presencial Surco S/550, ambas reservas
   S/100). "Por tiempo limitado" (sin fecha) — bien para plantilla.
3. El "Incluye" no menciona materiales (correcto para software).
4. La rama activa **BOT-02**, cuyo prompt v4 (sin re-presentación, captura de modalidad)
   debe estar pegado ANTES de probar esta rama — si sigue en v3 va a duplicar la info.
5. El brochure PDF también sirve para enriquecer la KB-02 v4 (duración, temario) — leerlo
   cuando haya herramientas de PDF disponibles en el entorno.
