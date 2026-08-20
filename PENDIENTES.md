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

## ⬜ Pendiente de Oliver

1. **Pegar los prompts v4** (`guias-bots/PROMPTS-bots-v4.md`): BOT-00 y BOT-01 completos.
2. **Ajustar acciones de BOT-01**: eliminar la captura de "Horario de interés" (atrapaba el
   nivel) y agregar la de "Nivel de interés (bot)" con su texto de 219 caracteres.
3. **Re-subir las 3 Bases de Conocimiento** a sus bots y verificar que cada una quede
   **asociada** (no solo subida). KB-01 ya está en v4 en el repo; KB-02/03 sin cambios nuevos.
4. Corregir con **Francisco** el Pack de drywall: texto dice S/850, imagen de reserva dice
   S/890.

## ⬜ Pendiente de Claude (cuando Oliver dé luz verde para construir)

1. SP05 v2 "secuencia de ficha": árbol por curso, 6 mensajes por rama, activar bot de
   familia al final, WF-SWITCH quita `ficha-enviada`.
2. Reactivar captura de `Curso de interés` en BOT-00 (instrucciones para Oliver).
3. Prompts v4 (bots de familia sin presentación; voz de Valeria) + KB v4 (códigos G13/G24/
   G28, precio G16 S/525, requisitos de seguridad por taller, direcciones de sedes).
4. Custom values remodelados por curso (4 imágenes + textos).

## 🔒 Bloqueado por el cliente / Francisco

- Contenido de fichas de software y gestión (imágenes + textos) — prioridad talleres primero.
- WhatsApp API oficial conectado a la subcuenta (bloqueante para plantillas WABA y el viernes).
- Textos cortos por imagen: borradores nuestros pendientes de visto bueno de Lucía.
- P1 matriculados (bloquea AP01-04) · P2 precios faltantes restantes · P4 política de domingos.
