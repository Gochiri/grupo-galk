# Knowledge Bases — Bots Conversation AI (Grupo GALK)

## ⚠️ Sube los .txt, no los .csv

| Archivo | Bot | Se sube en |
|---|---|---|
| **`KB-BOT-01-talleres.txt`** | BOT-01 Talleres | Settings → AI Agents → BOT-01 → Knowledge Base |
| **`KB-BOT-02-software.txt`** | BOT-02 Software | ídem en BOT-02 |
| **`KB-BOT-03-gestion.txt`** | BOT-03 Gestión | ídem en BOT-03 |

Los `.csv` quedan como respaldo estructurado. **La KB busca de forma semántica**: responde
mucho mejor con texto redactado (temario, FAQ, reglas en prosa) que con filas de tabla.

Los `.txt` incluyen temarios, duraciones y qué incluye cada curso — datos **extraídos de los
workflows FICHA que Francisco tiene vivos en la subcuenta**, o sea los textos reales que hoy
se le envían al cliente.

---

3 CSVs, uno por bot especialista. Se suben en **Settings → AI Agents → [bot] → Knowledge Base**.

| CSV | Bot | Cursos |
|---|---|---|
| `catalogo-talleres-galk.csv` | BOT-01 Talleres | Melamina DC/Avanzado, Drywall DC/Avanzado, Electricidad+Domótica |
| `catalogo-software-galk.csv` | BOT-02 Software | SketchUp (G1), Revit (G4), Mobiliario (G8), AutoCAD (G12) |
| `catalogo-gestion-galk.csv` | BOT-03 Gestión | Cocinas (G5), Obra Interiorista (G3), Espacios Comerciales (G15), Supervisión (G2) |

**KB separada por bot a propósito:** cada bot solo conoce los precios de su familia → estructuralmente imposible cotizar mal el precio de otra sede/curso.

## Reglas generales (incluir en el prompt `## Instructions` de cada bot)
- **Medios de pago:** Yape, Plin, tarjeta.
- **Pack x2** (solo talleres): Desde Cero + Avanzado, misma persona, **solo Lima (Surco / Los Olivos)** → **S/890** con reserva de **S/200**. **Arequipa no tiene pack.**
- **Precios:** el bot responde SOLO desde estos CSV. Nunca inventa. La fuente de verdad final es el **panel RoasSeeker**.
- **Horarios:** NO están en el CSV (cambian semanalmente). Vienen en la ficha que envía SP05 desde el Custom Value; el bot solo captura el horario que elige el lead.

## ⚠️ Datos PROVISIONALES — pendientes de Fase 0
- **Precios de las versiones "Avanzado"** (Melamina/Drywall): marcados `por confirmar` — el §4 no los lista. Confirmar en **Fase 0.2** con el panel.
- **Duraciones:** todas `por confirmar`.
- **Códigos G:** los del §4. **AutoCAD (G12)** y **Espacios Comerciales (G15)** están marcados por el conflicto panel vs brochure (§4) → congelar en **Fase 0.1**.
- **Sedes Los Olivos:** se asume mismo precio que Surco (Lima). Confirmar en Fase 0.4 (dedup del catálogo).

Precios confirmados por el §4 del handoff (regular → promo, PEN): Melamina DC Lima 750→525 / Arequipa 575→400 · Drywall DC Lima 650→450 / Arequipa 645→400 · Electricidad 780→600 (solo Lima) · SketchUp/Revit online 740→370 / Surco 1100→550 · Mobiliario/AutoCAD online 740→370 · Cocinas 840→420 · Obra Interiorista 780→390 · Espacios Comerciales 700→350 · Supervisión 598→298.
