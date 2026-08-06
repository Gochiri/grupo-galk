"""WF-SWITCH — limpia los datos de interés cuando el lead cambia de familia.

POR QUÉ EXISTE
--------------
Los cross-transfers entre especialistas (BOT-01 ↔ BOT-02 ↔ BOT-03) tienen un problema:
la acción **Contact Info de Conversation AI solo rellena campos VACÍOS, no sobrescribe**.

Sin esto, un lead que le dice "melamina" a BOT-01 y luego cambia a AutoCAD se transfiere a
BOT-02, BOT-02 intenta escribir `Curso de interés = AutoCAD`, el campo YA dice "Melamina"
→ se queda en Melamina → **SP05 le manda la ficha equivocada** y SP06 lo califica con el
curso de la otra familia.

WF-SWITCH borra los 10 campos de interés para que el bot receptor arranque en limpio.
No toca nombre, teléfono, correo ni la atribución de Meta.
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, nid, n_update

NOMBRE = "WF-SWITCH | Limpiar interés al cambiar de familia"
CARPETA = "af354b55-6cf2-44e8-a062-da45855f7175"      # GALK 2.0 · 01 Setup y Normalización
TAG = "cambio-de-familia"

# Los 10 campos que se vacían. Los `(bot)` y sus gemelos dropdown, en ese orden:
# primero los dropdown, luego los de texto — así WF-NORM, que escucha los `(bot)`,
# no vuelve a rellenar el dropdown que acabamos de limpiar.
CAMPOS = [
    "contact.familia_de_inters",     # dropdown
    "contact.modalidad",
    "contact.sede",
    "contact.pack_x2",
    "contact.curso_de_inters",       # texto
    "contact.horario_de_inters",
    "contact.familia_de_inters_bot",
    "contact.modalidad_bot",
    "contact.sede_bot",
    "contact.pack_x2_bot",
]


def main():
    r = C.request("GET", f"/workflow/{LOC}")
    lista = r if isinstance(r, list) else r.get("workflows", [])
    wid = next((w["id"] for w in lista if w.get("name") == NOMBRE), None)

    n1 = nid()
    templates = [n_update(n1, [(k, "") for k in CAMPOS], name="Vaciar datos de interés")]

    if not wid:                                        # idempotencia (§3)
        wf = C.request("POST", f"/workflow/{LOC}", {"name": NOMBRE, "parentId": CARPETA})
        wid = wf.get("id") if isinstance(wf, dict) else None
        if not wid:
            sys.exit(f"ABORT: no se pudo crear -> {wf}")
    d = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    C.request("PUT", f"/workflow/{LOC}/{wid}",
              {"name": NOMBRE, "version": d.get("version", 1), "parentId": CARPETA,
               "status": "draft", "workflowData": {"templates": templates}})

    C.create_location_tag(TAG)
    if not (C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []):
        v = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
        first = ((v.get("workflowData") or {}).get("templates") or [{}])[0].get("id")
        C.request("POST", f"/workflow/{LOC}/trigger", {
            "status": "draft", "workflowId": wid, "schedule_config": {},
            "conditions": [{"operator": "index-of-true", "field": "tagsAdded",
                            "value": TAG, "title": "Tag Added", "type": "select",
                            "id": "tag-added"}],
            "type": "contact_tag", "masterType": "highlevel", "name": "Cambio de familia",
            "allowMultiple": "no",
            "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
            "active": False,          # nunca True: publica el workflow (ver fix_wf_norm.py)
            "triggersChanged": True, "location_id": LOC, "targetActionId": first,
            "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})

    v = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    tpl = (v.get("workflowData") or {}).get("templates") or []
    campos = (tpl[0]["attributes"]["fields"] if tpl else [])
    print(f"{NOMBRE}\n  id={wid}  status={v.get('status')}  nodos={len(tpl)}  campos={len(campos)}")
    for f in campos:
        print(f"    vaciar: {f['title']}")
    print("  triggers:", len(C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []))


if __name__ == "__main__":
    main()
