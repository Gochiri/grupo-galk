# G7 — AutoCAD desde Cero

> Paquete recibido de Oliver el 24-ago. Área SOFTWARE → BOT-02. Doble modalidad
> (virtual Zoom / presencial Surco). Secuencia: apertura → texto de temario →
> brochure PDF → cierre (reserva + pregunta de modalidad, un solo nodo).

## Texto de apertura (con el cambio Camila → Valeria, regla del 20-ago)

```
💬 ¡Hola! ¿Cuál es tu nombre? 😊

Soy _Valeria del equipo de Grupo GALK_, ¡un gusto saludarte! 🙌

Te brindo información en *"AutoCAD desde Cero (G7)"*, ideal para estudiantes, técnicos, arquitectos, diseñadores e ingenieros que desean aprender a desarrollar planos profesionales desde cero ✨

📌 Modalidad: Virtual – En vivo por Zoom y Presencial Lima, Surco (Calle Aldabas 559)
📌 Ofertas vigentes por tiempo limitado:
✅ S/370 modalidad virtual (reserva con S/100)
✅ S/490 modalidad presencial (reserva con S/100)

🧾 Incluye: certificación, clases en vivo, instaladores de programas, asesorías personalizadas y grupo de WhatsApp 💻

📸 Te comparto el brochure con toda la información sobre el contenido, duración y beneficios del curso. ¡Mira lo completo que está este programa! 👇
```

## Texto 2 (nodo propio, antes del PDF)

```
💡 En este programa aprenderás desde la interfaz y comandos básicos de AutoCAD hasta la elaboración completa de planos, cortes, elevaciones, bloques dinámicos e impresión profesional de proyectos 📐✨

Además, trabajarás con herramientas como cotas, hatch, layouts, escalas y configuración de planos para presentación profesional 💯
```

## Brochure PDF

- Media store: id `6a8ce4af67bb7ac351f3d644`, 1,236,240 bytes
- Nombre en el store: "G7 AUTOCAD DESDE CERO" (se envía como `G7 AutoCAD desde Cero.pdf`)

## Cierre (un solo nodo: reserva + pregunta de modalidad)

```
Reserva tu vacante con S/100 y cancela el saldo hasta 2 días antes del inicio de clases 🙌

✨ ¿Te gustaría aprender en modalidad virtual o prefieres la experiencia presencial? 😊
```

## Notas / decisiones técnicas

1. **Apertura decía "Camila"** → cambiado a **Valeria** (regla 20-ago).
2. **⚠️ FIX EN WF-MOD**: el mapeo original (planeación de julio) derivaba AutoCAD →
   Online y Mobiliario → Online. Ambos cursos resultaron de DOBLE modalidad
   (virtual + presencial), así que se les QUITA la rama de WF-MOD — la modalidad la
   decide el lead y la captura BOT-02, igual que SketchUp/Revit. Sin este fix, WF-MOD
   escribía "Online" al detectar el curso y SP06 podía calificar antes de que el lead
   eligiera.
3. **Valor oficial**: `AutoCAD` (lista v4.2) · **conds rama SP05**: contains `autocad`
   · **bot destino**: BOT-02 · **SP04.8 respaldo**: tokens `autocad`, `auto cad`, `g7`.
