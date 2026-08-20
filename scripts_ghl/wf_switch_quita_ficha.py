"""WF-SWITCH: al cambiar de familia también debe quitarse el tag `ficha-enviada`,
si no la guarda de SP05 v2 bloquea la ficha del curso nuevo (ACUERDOS 19-ago §3.5).

Si el workflow ya tiene un nodo remove_contact_tag, se le añade el tag a su lista
(cambio mínimo, sin tocar la cadena). Si no, se inserta un nodo nuevo justo después
del nodo de vaciado hecho en la UI, preservando todos los IDs existentes.

Uso: wf_switch_quita_ficha.py [--aplicar]
"""
import os, sys, json, uuid, pathlib
ROOT = pathlib.Path("/home/user/grupo-galk")
for l in (ROOT / ".env").read_text().splitlines():
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts_ghl"))
from wf_lib import C, LOC

aplicar = "--aplicar" in sys.argv
ws = C.request("GET", f"/workflow/{LOC}")
sw = [w for w in ws if w.get("name", "").startswith("WF-SWITCH")][0]
d = C.request("GET", f"/workflow/{LOC}/{sw['id']}")
tpl = d["workflowData"]["templates"]

rm = [n for n in tpl if n["type"] == "remove_contact_tag"]
if rm:
    n = rm[0]
    tags = n["attributes"].get("tags", [])
    if "ficha-enviada" in tags:
        print("ya estaba (idempotencia §3):", tags); sys.exit(0)
    n["attributes"]["tags"] = tags + ["ficha-enviada"]
    print("añado 'ficha-enviada' al Remove Tag existente:", n["attributes"]["tags"])
else:
    limpiar = [n for n in tpl if n["type"] == "update_contact_field"
               and n.get("attributes", {}).get("actionType") == "clear_field_data"]
    if not limpiar:
        print("ABORT: no encuentro ni remove_contact_tag ni el nodo de vaciado en WF-SWITCH"); sys.exit(1)
    prev = limpiar[0]
    nuevo_id = str(uuid.uuid4())
    nuevo = {"id": nuevo_id, "order": 0, "attributes": {"tags": ["ficha-enviada"]},
             "name": "Quitar ficha-enviada", "type": "remove_contact_tag",
             "parent": prev["id"], "parentKey": prev["id"], "next": prev.get("next", "")}
    # el hijo que colgaba del nodo de vaciado pasa a colgar del nuevo
    for n in tpl:
        if n.get("parent") == prev["id"]:
            n["parent"] = nuevo_id; n["parentKey"] = nuevo_id
    prev["next"] = nuevo_id
    tpl.append(nuevo)
    print("inserto nodo 'Quitar ficha-enviada' tras el vaciado de la UI")

if not aplicar:
    print("(dry-run — usa --aplicar)"); sys.exit(0)

r = C.request("PUT", f"/workflow/{LOC}/{sw['id']}",
              {"name": d.get("name"), "version": d.get("version"), "parentId": d.get("parentId"),
               "status": d.get("status"), "allowMultiple": d.get("allowMultiple", True),
               "workflowData": {"templates": tpl}})
print("PUT:", "OK" if r and not (isinstance(r, dict) and r.get("_error")) else r)
v = C.request("GET", f"/workflow/{LOC}/{sw['id']}")
print("verificado: allowMultiple =", v.get("allowMultiple"), "· nodos:", len(v["workflowData"]["templates"]))
trs = C.request("GET", f"/workflow/{LOC}/trigger?workflowId={sw['id']}") or []
if isinstance(trs, dict): trs = trs.get("triggers", [])
ids = {n["id"] for n in v["workflowData"]["templates"]}
for t in trs:
    ta = t.get("targetActionId")
    print(f"trigger {t.get('name')!r}: active={t.get('active')} target={'OK' if (ta is None or ta in ids) else 'ROTO -> reparar_targetaction'}")
