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
| 20-ago | Condiciones v4 de los 3 Transfer Bot pegadas + captura de Curso v4.1 (3 áreas) pegada + ejemplo SketchUp corregido |
| 20-ago | **PRUEBA SKETCHUP: PASÓ — APROBADA POR OLIVER** — secuencia completa por WhatsApp con **PDF entregado** (primera validación de documento), curso capturado, pregunta de modalidad enviada. El patrón texto+imágenes+PDF+activación de bots queda 100% validado |

## ⬜ Pendiente de Oliver

0. ~~PIT~~ ✅ (20-ago: nuevo PIT recibido, .env recreado, brochures subidos, ramas
   SketchUp y Revit ACTIVAS en SP05)
0b. ~~Prompt v4 de BOT-02~~ ✅ (20-ago: pegado, confirmado por Oliver)
0c. ~~PDFs de Revit~~ ✅ (20-ago: eran el mismo archivo — Francisco lo envió dos veces por
   error; la rama queda con 1 PDF. Si apareciera un segundo documento real, se agrega)
0d. **Confirmar orden del cierre de Revit**: hoy va pregunta de modalidad → duración/reserva
   (tal como llegó). ¿La pregunta debería ir al final?
1. ~~**Re-subir las 3 Bases de Conocimiento**~~ ✅ (20-ago: KB-01 v4 subida 3:20 PM;
   KB-02/03 ya estaban al día — confirmado por Oliver)
1b. **Prueba Revit 24-ago: el BOT-00 no ejecutó NINGUNA captura (bug nuevo, firma distinta
   a las fallas de SketchUp).** Verificado por API campo por campo: TODO lo que tiene valor
   lo escribió Oliver a mano (Curso, Familia dropdown, Fuente, UTM, fecha); los 3 campos
   del bot (`Familia de interés (bot)`, `Curso de interés` vía bot, `Nivel`) quedaron
   vírgenes. El bot SÍ respondió sus 2 turnos con la línea v4 correcta y NO hay rastro de
   "Agente Transferido" en los mensajes de la API (la actividad de oportunidad sí aparece,
   así que las actividades sí se ven). Es decir: no fue el Transfer ni la descripción — las
   acciones de Contact Info no corrieron en absoluto. En las fallas del 20-ago al menos
   Familia se escribía. Lo que SÍ quedó validado: la rama Revit de SP05 entregó bien
   apertura + PDF + pregunta + duración al disparar (por la escritura manual); triggers
   SP05/SP06 sanos; `asesor-notificado` = WF3 de Francisco (ruido conocido).
   → Prueba A/B melamina (24-ago 9:39 AM, contacto yd5vTVuDqi3y6tpH2HIb): **la acción de
   Familia SÍ escribió** (evento "Campo de contacto actualizado" → Familia (bot) = Talleres,
   normalizador al dropdown OK) pero **la acción de Curso NO escribió — ni con melamina,
   que siempre funcionó**. Diagnóstico final: la acción Contact Info "Capturar curso de
   interés" del BOT-00 dejó de ejecutar sola entre el 20 y el 24 de agosto, sin que nadie
   tocara nada (las demás acciones corren bien). → Fix: **borrar esa acción y recrearla de
   cero** con la descripción v4.2 + los 4 ejemplos, y re-probar melamina y luego Revit.
   Si ni recreada escribe → es fallo de plataforma GHL (ticket a soporte) y armamos plan B
   (extracción por workflow con acción de IA, fuera del bot).
   · 24-ago ~10:07 AM: Oliver **recreó la acción de cero con la v4.2 y TAMPOCO escribía**
   (Familia sí, otra vez).
   · 24-ago 10:17 AM: **RESUELTO — el fix fue REORDENAR las acciones** (Curso al primer
   lugar): con eso GHL reconstruyó la lista y AMBAS capturas volvieron a ejecutar.
   Verificado por API (contacto l4BhaZZgkYzd9o2BwsYI): Curso = 'Melamina' escrito por el
   bot, Familia normalizada, Modalidad = Presencial derivada, tag `ficha-enviada` — SP05
   corrió de punta a punta sin intervención manual. La acción de Curso quedó con la
   descripción v4.2 y PRIMERA en el orden (dejarla así). Gotcha documentado en el
   playbook del CLI v2.
   · 24-ago 10:28 AM: **PRUEBA REVIT: PASÓ — APROBADA POR OLIVER.** Curso = 'Revit BIM'
   (nombre oficial vía v4.2), Familia = Software, secuencia con PDF + pregunta de
   modalidad + duración entregada completa.
   · 24-ago 10:33 AM: **prueba drywall: CERO capturas otra vez** (verificado por API,
   contacto rG6ClkSaa0E5H19avcvb — ni Familia ni Curso a los 3+ min; misma firma que la
   Revit de las 9:09). Conclusión del día: la ejecución de acciones de Conversation AI
   está INTERMITENTE del lado de GHL (~50% de los turnos hoy); cuando corre, nuestra
   config escribe perfecto.
   · 24-ago ~11 AM: **SP04 CONSTRUIDO (aprobado por Oliver)** — 6 mini-workflows de
   respaldo determinístico en DRAFT con triggers inactivos, verificados por API
   (`scripts_ghl/build_sp04_respaldo.py`): customer_reply por palabras clave (listas de
   los CAMPOS de Francisco) + etiqueta `pruebas demo` → wait 90 s (60 s Supervisión) →
   guarda (sale si ya hay curso o ficha-enviada) → escribe el nombre oficial en Curso.
   IDs: SP04.0 Supervisión 71865893 · SP04.1 Melamina 958eb984 · SP04.2 Drywall
   50d6c0ac · SP04.3 Electricidad e965d90b · SP04.4 SketchUp e1908cf9 · SP04.5 Revit
   b5bfbfb1 (carpeta GALK 2.0 · 04 Sales Pipeline). Falta: revisión de Oliver en la UI
   → activar triggers (los 6 PUT active:true publican) → probar drywall de nuevo.
   En go-live: quitar el filtro `pruebas demo` de los 6 triggers (junto con LS01/canales).
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
