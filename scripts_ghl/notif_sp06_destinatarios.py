"""Los dos avisos de SP06 van a destinatarios distintos, y no es intercambiable.

    rama "Asesor asignado"  ->  al DUEÑO DEL CONTACTO   (userType "assign")
    rama None (falló)       ->  a LUCÍA, la supervisora  (userType "user")

El de fallo **no puede ir al dueño del contacto**: existe precisamente porque el round robin
no asignó a nadie, así que no hay dueño. Avisar a "propietarios asignados" ahí es avisar a
nadie — el lead se queda calificado, sin dueño y sin que nadie se entere. Es el escenario de
pérdida silenciosa que ese ramal se construyó para evitar.

Pasó el 17-ago: al seleccionar "Propietarios asignados" en la UI se aplicó a los dos nodos y
el de fallo perdió a Lucía. Este script restituye el destinatario correcto de cada uno.

El ramal se identifica por estructura, no por el título: se busca el nodo que apunta al tag
`asignacion-fallida`. Así sigue funcionando si alguien reescribe los textos.
"""
import sys, json, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
from wf_lib import C, LOC, SUPERVISORA

WID = "84811c16-30d8-4c08-a05d-0c12fa46567d"
TAG_FALLO = "asignacion-fallida"


def main():
    d = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    tpl = (d.get("workflowData") or {}).get("templates") or []
    if not tpl:
        sys.exit("ABORT: no pude leer los nodos de SP06")
    print(f"SP06 v{d.get('version')} · {d.get('status')} · {len(tpl)} nodos")

    tag = next((n for n in tpl if n.get("type") == "add_contact_tag"
                and TAG_FALLO in ((n.get("attributes") or {}).get("tags") or [])), None)
    if not tag:
        sys.exit(f"ABORT: no encontré el tag '{TAG_FALLO}'. Revisar a mano.")
    fallo = next((n for n in tpl if n.get("next") == tag["id"]
                  and n.get("type") == "internal_notification"), None)
    if not fallo:
        sys.exit("ABORT: el nodo que apunta al tag de fallo no es una notificación. Revisar.")

    cambios = []
    for n in tpl:
        if n.get("type") != "internal_notification":
            continue
        no = (n.get("attributes") or {}).get("notification") or {}
        es_fallo = n["id"] == fallo["id"]
        quiero = ({"userType": "user", "selectedUser": SUPERVISORA} if es_fallo
                  else {"userType": "assign", "assignedOwners": ["contact_owner"]})
        actual = {k: no.get(k) for k in quiero}
        etiqueta = "fallo → Lucía" if es_fallo else "asignado → dueño del contacto"
        if actual == quiero:
            print(f"  ok   {n['id'][:8]}  {etiqueta}")
            continue
        no.pop("assignedOwners", None)
        no.pop("selectedUser", None)
        no.update(quiero)
        cambios.append(f"{n['id'][:8]} {etiqueta}")
        print(f"  FIX  {n['id'][:8]}  {etiqueta}  (estaba: {json.dumps(actual, ensure_ascii=False)})")

    if not cambios:
        print("\nLos dos avisos ya van a quien deben. Nada que hacer (idempotencia §3).")
        return

    r = C.request("PUT", f"/workflow/{LOC}/{WID}",
                  {"name": d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"), "status": d.get("status"),
                   "allowMultiple": d.get("allowMultiple"),
                   "workflowData": {"templates": tpl}})
    print("PUT:", "OK" if r and not r.get("_error") else r)

    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    print(f"\nVERIFY: v{v.get('version')} · {v.get('status')} · reingreso={v.get('allowMultiple')}")
    for n in (v.get("workflowData") or {}).get("templates") or []:
        if n.get("type") == "internal_notification":
            no = (n.get("attributes") or {}).get("notification") or {}
            dest = (f"usuario {no.get('selectedUser')}" if no.get("userType") == "user"
                    else str(no.get("assignedOwners")))
            print(f"  {n['id'][:8]}  userType={no.get('userType'):8} -> {dest}")
            print(f"            {no.get('title')}")


if __name__ == "__main__":
    main()
