# G8 — Diseño de Mobiliario Profesional (IA, Modelado 3D y Planimetría)

> Paquete recibido de Oliver el 24-ago (dictado, formato estándar). Curso del área
> SOFTWARE → bot destino BOT-02 (captura modalidad + sede). Secuencia: apertura →
> 4 imágenes → 2 mensajes finales SEPARADOS (dos nodos de WhatsApp).

## Texto de apertura (con el cambio Camila → Valeria, regla del 20-ago)

```
💬 ¡Hola! ¿Cuál es tu nombre? 😊
Soy Valeria del equipo de Grupo GALK 🙌

Te escribo porque tenemos abierta la preventa de nuestro nuevo curso:

✨ DISEÑO DE MOBILIARIO PROFESIONAL – IA, Modelado 3D y Planimetría ✨

Ideal para quienes desean aprender a diseñar muebles modernos y presentar proyectos con acabado profesional 🪵📐
📌 Importante: el curso requiere conocimientos de SketchUp a nivel básico-intermedio.

📌 ¿Qué aprenderás?
✅ Diseño funcional de mobiliario
✅ Modelado 3D profesional
✅ Planimetría técnica
✅ Renderizado y presentación para clientes
✅ Uso de IA aplicada al diseño
✅ Optimización y despiece para fabricación real
```

## Imágenes — orden confirmado por Oliver

| # | Imagen | Nombre sugerido al subir |
|---|---|---|
| 1 | Portada oscura "DISEÑO DE MOBILIARIO PROFESIONAL: IA, MODELADO 3D Y PLANIMETRÍA" (modalidad virtual/presencial · 15 horas académicas) | `G8-1-portada` |
| 2 | "¿YA DISEÑAS MOBILIARIOS, PERO QUIERES VENDERLOS COMO TODO UN PROFESIONAL?" (dirigido a + temario 01-04 + sedes) | `G8-2-temario` |
| 3 | "Domina el diseño de mobiliario… CURSO: DISEÑO DE MOBILIARIO PROFESIONAL" (motivacional + descuento por combinar 2 cursos) | `G8-3-motivacional` |
| 4 | "RESERVA TU CURSO" (políticas + datos de pago) | `G8-4-reserva` |

## Mensaje final 1 (nodo WhatsApp propio)

```
🎁 Además, incluye:
✔️ Instaladores de programas
✔️ Clases en vivo
✔️ Asesorías personalizadas
✔️ Grupo de WhatsApp
✔️ Certificación a nombre de Grupo GALK

💰 PREVENTA DISPONIBLE:
🔹 Virtual en vivo: S/370
🔹 Presencial: desde S/380 (varia según la sede)

📍 Contamos con sedes en:
* Surco Lima: Calle aldabas 559
* Arequipa Provinvia: Calle José Santos Chocano 249 – Umacollo
```

## Mensaje final 2 (nodo WhatsApp propio — pregunta de cierre)

```
✨ Cuéntame, ¿te gustaría llevarlo en modalidad virtual o presencial?
Y en caso sea presencial, ¿prefieres Lima Surco o Provincia Arequipa? 😊

Así puedo brindarte los horarios y promociones 🙌🏻
```

## Inconsistencias registradas (política: se dejan tal cual, responsabilidad del cliente)

1. **Apertura decía "Camila"** → cambiado a **Valeria** (decisión del 20-ago: nombre único
   del bot; único cambio nuestro permitido).
2. **Sedes**: la imagen 2 lista **LOS OLIVOS** como sede; el mensaje final 1 solo menciona
   Surco y Arequipa. Se deja tal cual.
3. **"Provinvia"** (typo por "Provincia") y "Calle aldabas" (minúscula) en el mensaje
   final 1: texto del cliente, se envía tal cual.
4. **Yape o Plin** en la imagen de reserva: consistente con la decisión del 20-ago (Plin
   se queda).
5. Portada dice **15 horas académicas**; los mensajes no mencionan duración (sin
   conflicto, solo nota).
6. Precio presencial "desde S/380 (varía según la sede)" — impreciso, del cliente.

## Datos técnicos para el cascarón

- **Valor oficial de Curso de interés**: `Diseño de Mobiliario` (lista v4.2 del BOT-00).
- **Conds de la rama SP05**: contains `mobiliario` (no colisiona con ningún otro curso).
- **Bot destino**: BOT-02 (software) — el cierre pide modalidad Y sede, que son
  exactamente las capturas del BOT-02.
- **SP04 de respaldo**: agregar SP04.6 Mobiliario con keywords (tokens completos):
  `mobiliario`, `mobiliarios`, `g8` (NO "muebles": demasiado genérico, chocaría con
  leads de melamina).
- **Modalidad NO se deriva** (curso con ambas modalidades, como SketchUp/Revit): sin
  rama en WF-MOD; decide el lead y captura BOT-02.
