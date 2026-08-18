"""El desactivador del bot viejo también REASIGNA — y quedó corriendo en cada mensaje.

QUÉ PASÓ (18-ago, segunda prueba de AutoCAD)
--------------------------------------------
BOT-00 contestó el primer mensaje y murió en el segundo. Verificado por API: cero salientes
después del "Oliver Guerrero".

El arreglo anterior movió "activar BOT-00" dentro de la rama de primera visita, pero dejó
FUERA el primer nodo: "bot d3Sig (heredado de Francisco) → inactive". Y ese campo es
*Change assigned Conversation AI bot*: no solo apaga, **reasigna la conversación al bot que
nombra**. En cada mensaje posterior a la primera visita, LS01 le entregaba la conversación
al bot viejo de Francisco, apagado. Resultado: silencio total desde el segundo mensaje.

Antes no se veía porque el "activar BOT-00" corría justo después y volvía a robar la
conversación — un bug tapaba al otro.

EL ARREGLO
----------
El desactivador se mueve TAMBIÉN dentro de la rama de primera visita, delante del activador
(el último en asignar gana, así que el orden deja a BOT-00 al mando):

    ANTES:   d3Sig→inactive  →  UTMs  →  ¿primera vez?
                                            ├ sí → BOT-00→active → fecha, fuente, ...
                                            └ no → (la conversación quedaba en d3Sig, muerta)
    DESPUÉS: UTMs  →  ¿primera vez?
                        ├ sí → d3Sig→inactive → BOT-00→active → fecha, fuente, ...
                        └ no → (no toca el bot: sigue el que estaba)

⚠️ El nodo raíz cambia (pasa a ser el de UTMs) → correr `reparar_targetaction.py --aplicar`
después, o el trigger queda apuntando a un nodo movido.
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
from wf_lib import C, LOC

VIEJO = "d3SigGiEfOxEGQVtUZsm"      # bot heredado de Francisco
BOT00 = "FvWG0eZkzx5AutuN79Jo"


def main():
    w = next(x for x in C.request("GET", f"/workflow/{LOC}") if x["name"].startswith("LS01"))
    d = C.request("GET", f"/workflow/{LOC}/{w['id']}") or {}
    tpl = (d.get("workflowData") or {}).get("templates") or []
    if not tpl:
        sys.exit("ABORT: no pude leer los nodos de LS01")
    print(f"LS01 v{d.get('version')} · {d.get('status')} · {len(tpl)} nodos")

    des = next((n for n in tpl if n.get("type") == "update_conversation_ai_status"
                and (n.get("attributes") or {}).get("assignedEmployeeId") == VIEJO), None)
    act = next((n for n in tpl if n.get("type") == "update_conversation_ai_status"
                and (n.get("attributes") or {}).get("assignedEmployeeId") == BOT00), None)
    if not des or not act:
        sys.exit("ABORT: no encontré los dos nodos de bot")
    head = next(n for n in tpl if n.get("nodeType") == "condition-node")
    rama = next(n for n in tpl if n.get("nodeType") == "branch-yes"
                and n.get("parentKey") == head["id"])

    if des.get("parentKey") == rama["id"]:
        print("El desactivador ya está dentro de la rama. Nada que hacer (idempotencia §3).")
        return
    if rama.get("next") != act["id"]:
        sys.exit(f"ABORT: la rama no empieza con el activador ({str(rama.get('next'))[:8]}); revisar a mano")

    # sacarlo de la cadena principal: era la raíz, así que nadie le apunta
    if any(n.get("next") == des["id"] for n in tpl):
        sys.exit("ABORT: alguien apunta al desactivador; no era la raíz. Revisar a mano.")
    nueva_raiz = des.get("next")

    des["next"] = act["id"]
    des["parent"] = des["parentKey"] = rama["id"]
    rama["next"] = des["id"]
    print(f"  desactivador {des['id'][:8]} → dentro de la rama, delante del activador")
    print(f"  nueva raíz: {str(nueva_raiz)[:8]} (recordar reparar_targetaction)")

    r = C.request("PUT", f"/workflow/{LOC}/{w['id']}",
                  {"name": d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"), "status": d.get("status"),
                   "allowMultiple": d.get("allowMultiple"),
                   "workflowData": {"templates": tpl}})
    print("PUT:", "OK" if r and not r.get("_error") else r)

    v = C.request("GET", f"/workflow/{LOC}/{w['id']}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    vb = {n["id"]: n for n in vt}
    vr = next(n for n in vt if n.get("nodeType") == "branch-yes")
    cadena, cur, i = [], vb.get(vr.get("next")), 0
    while cur and i < 6:
        a = cur.get("attributes") or {}
        et = cur.get("type")
        if et == "update_conversation_ai_status":
            et += f"({str(a.get('assignedEmployeeId'))[:6]}→{a.get('status')})"
        cadena.append(et)
        nx = cur.get("next")
        cur = vb.get(nx) if isinstance(nx, str) and nx else None
        i += 1
    print(f"VERIFY: v{v.get('version')} · rama primera-visita: " + " → ".join(cadena))


if __name__ == "__main__":
    main()
