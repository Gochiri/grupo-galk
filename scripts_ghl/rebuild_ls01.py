"""LS01 reconstruido en forma canónica: el grafo había quedado con dos convenciones mezcladas.

QUÉ PASÓ
--------
LS01 se armó en la UI, donde `parent` = nodo anterior (lista enlazada). Los dos arreglos por
API le metieron nodos con `parent` = id de la rama (la convención de `arbol()`), y quedaron
además punteros `parent` viejos sin actualizar. La lógica por `next` seguía bien —la
verificación la leía correcta— pero **el canvas no sabe dibujar la mezcla**: pintaba el flujo
lineal, sin el if/else. Y si alguien guardaba desde esa vista, la UI persistía la versión
plana y la guarda se perdía de verdad.

QUÉ HACE
--------
Reconstruye los nodos desde cero con `arbol()`, comportamiento idéntico al diseño v13:

    Atribución Meta (UTMs)
      → ¿Fecha de primer contacto vacía?  (= primera visita)
          ├ sí → bot viejo→inactive → BOT-00→active → fecha → fuente → tag → oportunidad
          └ no → fuente → tag → oportunidad          (antes lo hacía un `goto`; ahora son
                                                      nodos duplicados — mismo efecto y la
                                                      UI lo dibuja sin inventos)

Los atributos de cada nodo se copian tal cual de los actuales (UTMs, fecha=currentDate,
Fuente=Meta Ads, tag origen-meta, oportunidad en Nuevo Lead con monetary_value).

El trigger no se toca: su `targetActionId` es None = entrada por defecto, válido.
⚠️ La nota adhesiva del canvas ("Revisar con Henry…") puede perderse: vive en la capa visual.
"""
import sys, copy, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, nid, arbol

VIEJO = "d3SigGiEfOxEGQVtUZsm"
BOT00 = "FvWG0eZkzx5AutuN79Jo"


def clon(attrs, nodo_id, tipo, nombre, nxt=""):
    return {"id": nodo_id, "order": 0, "attributes": copy.deepcopy(attrs),
            "name": nombre, "type": tipo, "next": nxt}


def main():
    w = next(x for x in C.request("GET", f"/workflow/{LOC}") if x["name"].startswith("LS01"))
    d = C.request("GET", f"/workflow/{LOC}/{w['id']}") or {}
    tpl = (d.get("workflowData") or {}).get("templates") or []
    if not tpl:
        sys.exit("ABORT: no pude leer LS01")
    print(f"LS01 v{d.get('version')} · {d.get('status')} · {len(tpl)} nodos")

    def attrs_de(tipo, filtro=None):
        for n in tpl:
            if n.get("type") != tipo:
                continue
            if filtro and not filtro(n.get("attributes") or {}):
                continue
            return n["attributes"]
        sys.exit(f"ABORT: no encontré el nodo {tipo} para copiar sus atributos")

    a_des  = attrs_de("update_conversation_ai_status", lambda a: a.get("assignedEmployeeId") == VIEJO)
    a_act  = attrs_de("update_conversation_ai_status", lambda a: a.get("assignedEmployeeId") == BOT00)
    a_utm  = attrs_de("update_contact_field", lambda a: any("UTM" in (f.get("title") or "") for f in a.get("fields", [])))
    a_fech = attrs_de("update_contact_field", lambda a: any("primer contacto" in (f.get("title") or "") for f in a.get("fields", [])))
    a_fuen = attrs_de("update_contact_field", lambda a: any((f.get("title") == "Fuente") for f in a.get("fields", [])))
    a_tag  = attrs_de("add_contact_tag")
    a_opp  = attrs_de("create_opportunity")

    fid_fecha = wf_lib.FID("contact.fecha_de_primer_contacto")
    cond = {"conditionType": "contact_detail", "conditionSubType": fid_fecha,
            "conditionOperator": "has_no_value", "__conditionId": nid(), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": wf_lib.NESTED, "allowIsOperatorTypes": wf_lib.ALLOWIS}

    # rama SÍ (primera visita)
    s = [nid() for _ in range(6)]
    rama_si = [
        # update_conversation_ai_status exige workflowsActionType=INTERNAL a nivel de
        # nodo (igual que whatsapp_v2); sin eso: "action has a corrupted type"
        {**clon(a_des, s[0], "update_conversation_ai_status", "Silenciar bot heredado", nxt=s[1]),
         "workflowsActionType": "INTERNAL"},
        {**clon(a_act, s[1], "update_conversation_ai_status", "Asignar BOT-00 Secretaria", nxt=s[2]),
         "workflowsActionType": "INTERNAL"},
        clon(a_fech, s[2], "update_contact_field", "Fecha primer contacto", nxt=s[3]),
        clon(a_fuen, s[3], "update_contact_field", "Fuente Meta", nxt=s[4]),
        clon(a_tag,  s[4], "add_contact_tag", "Add Tag Origen Meta", nxt=s[5]),
        clon(a_opp,  s[5], "create_opportunity", "Crear oportunidad → Nuevo Lead"),
    ]
    # rama None (visitas siguientes): lo que antes hacía el goto
    m = [nid() for _ in range(3)]
    rama_no = [
        clon(a_fuen, m[0], "update_contact_field", "Fuente Meta", nxt=m[1]),
        clon(a_tag,  m[1], "add_contact_tag", "Add Tag Origen Meta", nxt=m[2]),
        clon(a_opp,  m[2], "create_opportunity", "Actualizar oportunidad"),
    ]

    ramas = arbol([("Primera visita", [cond], rama_si)], none_next=rama_no)
    raiz = nid()
    templates = [clon(a_utm, raiz, "update_contact_field",
                      "Atribución Meta (5 campos)", nxt=ramas[0]["id"])] + ramas

    r = C.request("PUT", f"/workflow/{LOC}/{w['id']}",
                  {"name": d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"), "status": d.get("status"),
                   "allowMultiple": d.get("allowMultiple"),
                   "workflowData": {"templates": templates}})
    print("PUT:", "OK" if r and not r.get("_error") else r)

    v = C.request("GET", f"/workflow/{LOC}/{w['id']}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    vb = {n["id"]: n for n in vt}
    print(f"VERIFY: v{v.get('version')} · {v.get('status')} · reingreso={v.get('allowMultiple')} · {len(vt)} nodos")
    for hijo in [n for n in vt if str(n.get("nodeType", "")).startswith("branch")]:
        cadena, cur, i = [], vb.get(hijo.get("next")), 0
        while cur and i < 8:
            a = cur.get("attributes") or {}
            et = cur.get("type")
            if et == "update_conversation_ai_status":
                et = f"bot({str(a.get('assignedEmployeeId'))[:6]}→{a.get('status')})"
            cadena.append(et)
            nx = cur.get("next")
            cur = vb.get(nx) if isinstance(nx, str) and nx else None
            i += 1
        print(f"  rama {str(hijo.get('name')):16}: " + " → ".join(cadena))
    for t in C.request("GET", f"/workflow/{LOC}/trigger?workflowId={w['id']}") or []:
        print(f"  trigger '{t.get('name')}' active={t.get('active')} target={t.get('targetActionId')}")


if __name__ == "__main__":
    main()
