"""WF-SEDE — pone `Sede = No aplica` cuando el curso es online.

POR QUÉ
-------
La guarda de SP06 exige los tres campos: Curso, Modalidad y Sede. En talleres siempre hay
sede porque son presenciales, y por eso talleres funcionó. Pero en **software online y en
todo gestión no hay sede que capturar**: el lead jamás va a decir "no aplica", la acción
*Contact Info* no tiene nada que extraer, y `Sede` se queda vacía para siempre.

Resultado sin esto: **ningún lead de BOT-02 online ni de BOT-03 llega nunca al asesor.**
SP06 los corta en la guarda, en silencio, igual que pasaba con `Modalidad` antes de WF-MOD.

Es el mismo agujero que WF-MOD, un escalón más abajo.

CÓMO
----
Cuando la `Modalidad` queda en Online y la `Sede` sigue vacía, se escribe **No aplica**, que
ya existe como opción del desplegable.

La condición `Sede está vacía` importa: sin ella, un lead de SketchUp presencial en Surco que
después cambie a online se quedaría con Surco encima. Y al revés, nunca pisa una sede real.

ENCADENADO
----------
    Curso de interés  ->  WF-MOD    ->  Modalidad = Online
                                    ->  WF-SEDE   ->  Sede = No aplica
                                                  ->  SP06 ya tiene los tres, califica

Para SketchUp y Revit, que sí tienen las dos modalidades, la Modalidad la dice el lead y la
captura el bot; WF-SEDE actúa igual en cuanto esa modalidad resulte Online.
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, nid, n_update, arbol

NOMBRE = "WF-SEDE | Sede No aplica cuando es online"
CARPETA = "af354b55-6cf2-44e8-a062-da45855f7175"      # GALK 2.0 · 01 Setup y Normalización


def cond(key, operador, valor=None):
    c = {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(key),
         "conditionOperator": operador, "__conditionId": nid(), "ifElseNodeId": "",
         "__customFieldType__": "standard", "isWait": False,
         "nestedDropdownTypes": wf_lib.NESTED, "allowIsOperatorTypes": wf_lib.ALLOWIS}
    if valor is not None:
        c["conditionValue"] = valor
    return c


def main():
    r = C.request("GET", f"/workflow/{LOC}")
    wid = next((w["id"] for w in r if w.get("name") == NOMBRE), None)

    u = nid()
    templates = arbol([("Online sin sede → No aplica",
                        [cond("contact.modalidad", "is", "Online"),
                         cond("contact.sede", "has_no_value")],
                        [n_update(u, [("contact.sede", "No aplica")],
                                  name="Sede = No aplica")])])

    if not wid:                                        # idempotencia (§3)
        wf = C.request("POST", f"/workflow/{LOC}", {"name": NOMBRE, "parentId": CARPETA})
        wid = wf.get("id") if isinstance(wf, dict) else None
        if not wid:
            sys.exit(f"ABORT: no se pudo crear -> {wf}")
        print(f"creado {wid}")
    d = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    C.request("PUT", f"/workflow/{LOC}/{wid}",
              {"name": NOMBRE, "version": d.get("version", 1), "parentId": CARPETA,
               "status": d.get("status", "draft"),
               "allowMultiple": True,          # el lead puede cambiar de curso y recalcular
               "workflowData": {"templates": templates}})

    v = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    tpl = (v.get("workflowData") or {}).get("templates") or []
    entrada = next(n["id"] for n in tpl if n.get("nodeType") == "condition-node")

    if not (C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []):
        C.request("POST", f"/workflow/{LOC}/trigger", {
            "status": v.get("status"), "workflowId": wid, "schedule_config": {},
            "conditions": [wf_lib.cond_trigger_campo("contact.modalidad")],
            "type": "contact_changed", "masterType": "highlevel",
            "name": "Modalidad definida", "allowMultiple": "yes",
            "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
            "active": False,          # nunca True aquí: publica el workflow
            "triggersChanged": True, "location_id": LOC, "targetActionId": entrada,
            "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})

    v = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    tpl = (v.get("workflowData") or {}).get("templates") or []
    print(f"{NOMBRE}\n  id={wid}  status={v.get('status')}  reingreso={v.get('allowMultiple')}"
          f"  nodos={len(tpl)}")
    for t in C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []:
        ok = t.get("targetActionId") == entrada
        print(f"  trigger '{t.get('name')}' active={t.get('active')} entrada={'OK' if ok else 'ROTA'}")


if __name__ == "__main__":
    main()
