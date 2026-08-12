"""WF-MOD — deduce la Modalidad a partir del Curso, sin depender del bot.

POR QUÉ
-------
La acción *Contact Info* de Conversation AI **extrae** datos de lo que dice el lead.
`Modalidad` en talleres es siempre "Presencial", así que el lead nunca lo dice y la
acción nunca se dispara → el campo queda vacío → **SP06 no se ejecuta**, porque le
faltan datos de calificación.

Pedírselo al prompt no lo arregla: no hay nada que extraer. Y preguntárselo al lead
("¿presencial u online?") cuando solo existe presencial es una pregunta tonta que
empeora la conversación.

Solución: un workflow lo deduce del curso y escribe **directamente en el dropdown**
`Modalidad` (los workflows sí pueden escribir dropdowns, los bots no).

⚠️ EL ORDEN DE LAS RAMAS IMPORTA
Las ramas de un if_else son excluyentes: gana la primera que matchea. "Supervisión de
Melamina" **contiene** "Melamina", así que va PRIMERO — si no, la rama de Melamina lo
marcaría Presencial y ese curso es de gestión, online.

SketchUp y Revit NO tienen rama a propósito: son los dos únicos cursos con las dos
modalidades, así que ahí sí decide el lead y lo captura BOT-02.
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path("/home/user/grupo-galk/scripts_ghl")))
import wf_lib
from wf_lib import C, LOC, nid, n_update, arbol, cond_field

NOMBRE = "WF-MOD | Modalidad automática por curso"
CARPETA = "af354b55-6cf2-44e8-a062-da45855f7175"      # GALK 2.0 · 01 Setup y Normalización

# (texto a buscar en Curso de interés, modalidad resultante)
# El orden es el de evaluación. Supervisión antes que Melamina, a propósito.
MAPEO = [
    ("Supervisión",         "Online"),      # G2 es gestión, NO el taller de melamina
    ("Melamina",            "Presencial"),
    ("Drywall",             "Presencial"),
    ("Electricidad",        "Presencial"),
    ("Cocinas",             "Online"),
    ("Obra Interiorista",   "Online"),
    ("Espacios Comerciales", "Online"),
    ("Mobiliario",          "Online"),
    ("AutoCAD",             "Online"),
    # SketchUp y Revit: sin rama. El lead elige y lo captura el bot.
]


def main():
    r = C.request("GET", f"/workflow/{LOC}")
    wid = next((w["id"] for w in r if w.get("name") == NOMBRE), None)

    ramas = []
    for texto, modalidad in MAPEO:
        u = nid()
        ramas.append((f"{texto} → {modalidad}",
                      [cond_field("contact.curso_de_inters", texto, "contain")],
                      [n_update(u, [("contact.modalidad", modalidad)],
                                name=f"Modalidad = {modalidad}")]))
    templates = arbol(ramas)

    if not wid:                                        # idempotencia (§3)
        wf = C.request("POST", f"/workflow/{LOC}", {"name": NOMBRE, "parentId": CARPETA})
        wid = wf.get("id") if isinstance(wf, dict) else None
        if not wid:
            sys.exit(f"ABORT: no se pudo crear -> {wf}")
    d = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    C.request("PUT", f"/workflow/{LOC}/{wid}",
              {"name": NOMBRE, "version": d.get("version", 1), "parentId": CARPETA,
               "status": "draft", "workflowData": {"templates": templates}})

    if not (C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []):
        v = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
        first = ((v.get("workflowData") or {}).get("templates") or [{}])[0].get("id")
        C.request("POST", f"/workflow/{LOC}/trigger", {
            "status": "draft", "workflowId": wid, "schedule_config": {},
            "conditions": [{"operator": "has-changed",
                            "field": wf_lib.FID("contact.curso_de_inters"),
                            "title": "Curso de interés", "type": "text"}],
            "type": "contact_changed", "masterType": "highlevel",
            "name": "Curso de interés definido", "allowMultiple": "no",
            "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
            "active": False,          # nunca True: publica el workflow
            "triggersChanged": True, "location_id": LOC, "targetActionId": first,
            "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})

    v = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    tpl = (v.get("workflowData") or {}).get("templates") or []
    hdr = next(n for n in tpl if n.get("nodeType") == "condition-node")
    print(f"{NOMBRE}\n  id={wid}  status={v.get('status')}  nodos={len(tpl)}")
    for b in hdr["attributes"]["branches"]:
        print(f"    {b['name']}")
    print("  triggers:", len(C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []))


if __name__ == "__main__":
    main()
