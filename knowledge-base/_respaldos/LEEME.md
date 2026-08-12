# Respaldos de las Knowledge Base

Todas las versiones por las que pasó la KB de talleres, sacadas del historial de git.
Están aquí por si hay que volver a una anterior. **Git las tiene todas igual** — esto es
solo para tenerlas a mano sin comandos.

| Archivo | Qué es | Commit |
|---|---|---|
| `v1_ORIGINAL_(.txt, rechazado por GHL).txt` | La primera, en `.txt`. **GHL la rechaza**: el diálogo solo acepta PDF, DOC, DOCX y MD | `adac782` |
| `v2_md_con_Plin.md` | Convertida a `.md`. Todavía dice "Yape, Plin y tarjeta" | `ab36e03` |
| `v3_md_sin_Plin_con_ficha.md` | Sin Plin. Horarios: *"al lead se le envía una ficha con los horarios"* | `bcf609c` |
| `v4_ACTUAL_asesor_da_horarios.md` | **La de ahora.** Horarios: *"te los da tu asesor"* | `40e1556` |

## ¿Cuál tienes subida hoy en el bot?

Si la subiste **antes del 11-ago**, es la **v3**. Es la única diferencia con la v4:

```diff
- Los horarios y las fechas de inicio cambian cada semana y NO están en esta base de
- conocimiento. Al lead se le envía una ficha con los horarios actualizados de su sede.
- Tu trabajo es preguntarle cuál de esos horarios le acomoda, nunca inventar uno.
+ Los horarios, las fechas de inicio y los cupos te los da tu asesor. No están en esta
+ base de conocimiento y cambian, así que nunca inventes ni prometas un horario, una
+ fecha de inicio ni un cupo disponible.
+
+ Si la persona pregunta por horarios o fechas, dile que un asesor se los pasa enseguida
+ con las opciones de su sede, y sigue con lo tuyo: confirmar curso, modalidad y sede.
```

Todo lo demás —precios, temarios, sedes, Pack x2, medios de pago, FAQ— es idéntico.

## Rollback

`v3` es la del flujo original (bot manda ficha). Para volver, o usas este archivo o corres:

```bash
.venv/bin/python scripts_ghl/toggle_flujo.py original
```

Y vuelves a subir las 3 KB a los bots.
