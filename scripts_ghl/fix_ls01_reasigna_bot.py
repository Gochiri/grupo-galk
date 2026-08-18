"""LS01 reasignaba BOT-00 en CADA mensaje del lead, robándole la conversación al especialista.

QUÉ PASABA
----------
LS01 entra por `customer_reply`, o sea **en cada mensaje que manda el lead**, y con el
reingreso activo. Sus dos primeros nodos corrían siempre, antes de cualquier condición:

    1. desactivar bot d3SigGiEfOxEGQVtUZsm   (el viejo de Francisco)
    2. activar     bot FvWG0eZkzx5AutuN79Jo  = BOT-00 Secretaria   <-- el problema

Ese segundo nodo no solo enciende: el campo es *Change assigned Conversation AI bot*, así que
**reasigna la conversación a BOT-00**. Secuencia real del 18-ago:

    lead escribe        -> LS01 asigna BOT-00, BOT-00 saluda y transfiere a BOT-02  OK
    lead vuelve a escribir -> LS01 corre otra vez -> REASIGNA a BOT-00
                           -> contesta BOT-00, no BOT-02

Por eso el mensaje que salió fue *"el precio te lo confirma tu asesora, ¿te comunico con
ella?"*: es el patrón de BOT-00, que tiene prohibido dar precios. BOT-02 tenía S/740 y S/370
embebidos y nunca llegó a responder. Y por eso el borrador salió en Suggestive aunque BOT-02
esté en Auto-Pilot: quien contestaba era BOT-00, con su propio modo.

De paso explica los campos vacíos: BOT-02 nunca ejecutó su *Contact Info*.

EL ARREGLO
----------
LS01 ya distingue la primera visita con `Fecha de primer contacto has_no_value`, solo que los
dos nodos de bot quedaban fuera de esa comprobación. Se mueve **el de activar BOT-00** dentro
de la rama de primera visita.

El de desactivar el bot de Francisco se queda fuera a propósito: es idempotente y protege por
si su bot vuelve a engancharse a la conversación.

    ANTES:  desactivar -> activar BOT-00 -> UTMs -> if primera vez? -> ...
    DESPUÉS: desactivar -> UTMs -> if primera vez?
                                     |- sí  -> activar BOT-00 -> fecha, fuente, tag, oportunidad
                                     |- no  -> (sin tocar el bot asignado)
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
from wf_lib import C, LOC

BOT00 = "FvWG0eZkzx5AutuN79Jo"


def main():
    w = next(x for x in C.request("GET", f"/workflow/{LOC}") if x["name"].startswith("LS01"))
    d = C.request("GET", f"/workflow/{LOC}/{w['id']}") or {}
    tpl = (d.get("workflowData") or {}).get("templates") or []
    if not tpl:
        sys.exit("ABORT: no pude leer los nodos de LS01")
    byid = {n["id"]: n for n in tpl}
    print(f"LS01 v{d.get('version')} · {d.get('status')} · {len(tpl)} nodos")

    act = next((n for n in tpl if n.get("type") == "update_conversation_ai_status"
                and (n.get("attributes") or {}).get("assignedEmployeeId") == BOT00), None)
    if not act:
        sys.exit("ABORT: no encontré el nodo que activa BOT-00")
    head = next(n for n in tpl if n.get("nodeType") == "condition-node")
    rama = next(n for n in tpl if n.get("nodeType") == "branch-yes"
                and n.get("parentKey") == head["id"])

    if act.get("parentKey") == rama["id"]:
        print("Ya está dentro de la rama de primera visita. Nada que hacer (idempotencia §3).")
        return

    previo = next((n for n in tpl if n.get("next") == act["id"]), None)
    if not previo:
        sys.exit("ABORT: el nodo de activar BOT-00 no cuelga de nadie. Revisar a mano.")

    print(f"  saco  {act['id'][:8]} de la cadena principal (venía de {previo['id'][:8]})")
    previo["next"] = act.get("next")                      # puentear
    act["next"] = rama.get("next")                        # encabezar la rama
    act["parent"] = act["parentKey"] = rama["id"]
    rama["next"] = act["id"]
    print(f"  meto  {act['id'][:8]} como primer nodo de la rama '{rama.get('name')}'")

    r = C.request("PUT", f"/workflow/{LOC}/{w['id']}",
                  {"name": d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"), "status": d.get("status"),
                   "allowMultiple": d.get("allowMultiple"),
                   "workflowData": {"templates": tpl}})
    print("PUT:", "OK" if r and not r.get("_error") else r)

    v = C.request("GET", f"/workflow/{LOC}/{w['id']}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    vb = {n["id"]: n for n in vt}
    print(f"\nVERIFY: v{v.get('version')} · {v.get('status')} · {len(vt)} nodos")
    raiz = next(n for n in vt if not n.get("parent")
                and n["id"] not in {x.get("next") for x in vt if isinstance(x.get("next"), str)})
    cur, i = raiz, 0
    while cur and i < 6:
        a = cur.get("attributes") or {}
        x = f" bot={a.get('assignedEmployeeId')}->{a.get('status')}" if cur.get("type") == "update_conversation_ai_status" else ""
        print(f"  {cur.get('type')}{x}")
        nx = cur.get("next")
        cur = vb.get(nx) if isinstance(nx, str) and nx else None
        i += 1
    vr = next(n for n in vt if n.get("nodeType") == "branch-yes")
    prim = vb.get(vr.get("next"))
    pa = (prim or {}).get("attributes") or {}
    print(f"  rama '{vr.get('name')}' empieza con: {(prim or {}).get('type')}"
          f"{' bot=' + str(pa.get('assignedEmployeeId')) if pa.get('assignedEmployeeId') else ''}")


if __name__ == "__main__":
    main()
