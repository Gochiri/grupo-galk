# Pendientes vivos — quién debe qué

> Registro acordado el 20-ago: lo que Oliver confirma hecho se tacha aquí y NO se le vuelve
> a pedir. Lo que no esté confirmado sigue pendiente. Actualizar en cada intercambio.

## ✅ Hecho por Oliver (confirmado por él — no volver a pedir)

| Fecha | Qué |
|---|---|
| 20-ago | Decisiones de fichas: Plin se queda tal cual · fecha "24 de agosto" literal · mantenimiento mensual de plantillas es de Francisco · inconsistencias entre imágenes/textos del cliente se dejan tal cual (responsabilidad del cliente) |
| 20-ago | Mapeo de imágenes validado COMPLETO de los 3 talleres: Electricidad (portada=E-3, temario=E-2, motivacional=E-1, reserva=E-4) · Melamina (1=portada, 2=temario, 3=motivacional, 4=reserva) · Drywall (1=portada, 2=temario, 3=motivacional, 4=reserva) + sets Avanzado documentados |
| 20-ago | Prompt BOT-00 secretaria: Personality actualizado con nombre **Valeria** |
| 20-ago | Prompt de talleres: línea de electricidad cambiada a "se dicta en las tres sedes" |
| 20-ago | Implementación por canal: agente de Francisco excluye `pruebas demo` en el 645; BOT-00 lo incluye. LS01 dispara por etiqueta en cualquier canal |
| 20-ago | **PRUEBA E2E DE LA SECUENCIA POR WHATSAPP OFICIAL: PASÓ** — apertura + 4 imágenes + pregunta, bot pausado, BOT-01 despertó, calificación y asignación completas |
| 20-ago | Prompts v4 pegados (BOT-00 y BOT-01), captura de Horario eliminada del 01, captura de Nivel agregada |
| 20-ago | **PRUEBA 2 CON PROMPTS V4: PASÓ — PILOTO DE TALLERES CERRADO** — BOT-00 una línea, sin re-presentación, nivel en su campo (Avanzado), calificación completa |

## ⬜ Pendiente de Oliver

0. ~~PIT~~ ✅ (20-ago: nuevo PIT recibido, .env recreado, brochures subidos, ramas
   SketchUp y Revit ACTIVAS en SP05)
0b. **Pegar el prompt v4 de BOT-02** (está en `PROMPTS-bots-v4.md`) — antes de probar
   cualquier curso de software.
0c. ~~PDFs de Revit~~ ✅ (20-ago: eran el mismo archivo — Francisco lo envió dos veces por
   error; la rama queda con 1 PDF. Si apareciera un segundo documento real, se agrega)
0d. **Confirmar orden del cierre de Revit**: hoy va pregunta de modalidad → duración/reserva
   (tal como llegó). ¿La pregunta debería ir al final?
1. ~~**Re-subir las 3 Bases de Conocimiento**~~ ✅ (20-ago: KB-01 v4 subida 3:20 PM;
   KB-02/03 ya estaban al día — confirmado por Oliver)
2. **Probar las otras 2 ramas de talleres** (1 contacto cada una): drywall y electricidad —
   mismo guion que melamina. Tras subir KB, probar también 1-2 dudas ("¿aceptan Plin?",
   "¿cuánto dura?").
3. **Pedir a Lucía/Francisco el contenido de software y gestión**: por cada curso, texto de
   apertura + 4 imágenes en orden + texto final (mismo formato que talleres). Es EL
   bloqueante para replicar la secuencia a las otras áreas.
4. Corregir con **Francisco** el Pack de drywall: texto dice S/850, imagen de reserva dice
   S/890.

## ⬜ Pendiente de Claude

1. Al llegar el contenido de software/gestión: ramas nuevas en SP05 v2 (agregar entradas a
   RAMAS del script y re-correr) + prompts v4 de BOT-02/03 + KB v4 de ambos.
2. Definir con el cliente la pregunta final de los cursos online (no hay sede) — pregunta
   abierta №2 del 19-ago.
3. Pasada final de contenido/limpieza: custom values de ficha viejos (24, ya sin uso),
   plantillas WABA solo si hicieran falta mensajes iniciados por la empresa (los flujos
   actuales son de sesión abierta y no las requieren), SP05 v1 archivado.
4. Go-live talleres cuando el cliente diga: quitar filtro `pruebas demo` de LS01 y de los
   canales, apuntar pauta al 645, decidir agente default del 645.

## 🔒 Bloqueado por el cliente / Francisco

- Contenido de fichas de software y gestión (imágenes + textos) — prioridad talleres primero.
- WhatsApp API oficial conectado a la subcuenta (bloqueante para plantillas WABA y el viernes).
- Textos cortos por imagen: borradores nuestros pendientes de visto bueno de Lucía.
- P1 matriculados (bloquea AP01-04) · P2 precios faltantes restantes · P4 política de domingos.
