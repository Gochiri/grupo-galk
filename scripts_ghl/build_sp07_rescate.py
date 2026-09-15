"""SP07 — Red de rescate por tiempo: ningún lead con ficha se queda sin dueño.

EL HUECO (auditoría 15-sep, 329 leads de 3 días)
------------------------------------------------
SP06 asigna solo cuando el lead CALIFICA (curso + modalidad + sede). Todos los que
calificaron fueron asignados — cero fallas. Pero 145 leads recibieron su ficha, se
quedaron callados y nunca calificaron → jamás llegaron a un asesor. El 92% del
volumen se moría en silencio, que es exactamente lo que este proyecto vino a matar.

EL DISEÑO
---------
Trigger: tag `ficha-enviada` puesto (el marcador que SP05 pone al terminar la
secuencia). 15 minutos de espera y una pregunta:

    ¿"Asesor asignado" tiene valor?
       SÍ → nada que hacer: SP06 ya lo trabajó (o un humano). Sale sin efecto.
       NO → round robin (mismos 6 asesores, mismo nodo que SP06) → 1 min de
            seguro → escribe Asesor + Fecha → segunda pregunta:
              SÍ → notifica al dueño "hacer seguimiento" + tag `rescate-15min`
              NO → notifica a Lucía + tag `asignacion-fallida` (molde SP06 v2)

POR QUÉ NO CHOCA CON SP06
-------------------------
El assign_user de SP06 lleva `only_unassigned_contact: true` (verificado en el
workflow vivo): si el rescate asignó primero y el lead responde después, SP06
califica, mueve la oportunidad y notifica — pero NO le cambia el asesor.
Y al revés, si SP06 asignó dentro de los 15 min, la guarda de aquí corta.

Nada de bot-silenciado en el rescate: el lead no respondió, así que el bot se
queda vivo por si vuelve — y si vuelve y califica, SP06 cierra el circuito.

Reingreso (allowMultiple) en true: el conmutador quita y re-pone `ficha-enviada`
al cambiar de curso, y cada re-puesta debe poder re-enrolar. La guarda del asesor
hace el reingreso inofensivo.

Como siempre: se crea en DRAFT. Publicar y "Guardar trigger" se hace en la UI.
"""
import os, sys, json, time, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, SUPERVISORA, nid, n_update, n_tag, n_notif, n_wait, arbol

NOMBRE      = "SP07 | Rescate 15 min — ficha sin respuesta"
CARPETA     = "3dc6be37-5389-4385-9806-36722ba042ef"   # GALK 2.0 · 04 Sales Pipeline
SP06        = "84811c16-30d8-4c08-a05d-0c12fa46567d"
TAG_ENTRADA = "ficha-enviada"
TAG_OK      = "rescate-15min"
TAG_FALLO   = "asignacion-fallida"
K_ASESOR    = "contact.asesor_asignado_nuevo"
K_F_ASIGNA  = "contact.fecha_de_asignacin"
ESPERA_MIN  = 15


def cond_has_value(field_key):
    """has_value NO lleva conditionValue (molde de rebuild_sp06, verificado en vivo)."""
    return {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(field_key),
            "conditionOperator": "has_value", "__conditionId": nid(), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": wf_lib.NESTED, "allowIsOperatorTypes": wf_lib.ALLOWIS}


def construir(assign_attrs):
    n_wt15 = nid()

    # --- desenlace del rescate (árbol interno, molde SP06 v2) ---
    s_notif, s_tag = nid(), nid()
    rama_ok = [
        {**n_notif(s_notif, "🛟 Lead rescatado — hacer seguimiento",
                   "{{contact.name}} ({{contact.phone}}) recibió la ficha de "
                   "{{contact.curso_de_inters}} hace 15 min y no respondió. "
                   "Quedó asignado a ti para seguimiento manual."),
         "next": s_tag},
        n_tag(s_tag, [TAG_OK], parent=s_notif),
    ]
    f_notif, f_tag = nid(), nid()
    rama_fallo = [
        {**n_notif(f_notif, "⚠️ Round robin no asignó — lead sin dueño",
                   "El lead {{contact.name}} ({{contact.phone}}) lleva 15 min con ficha "
                   "sin respuesta y el round robin no lo asignó. Tomarlo a mano.",
                   usuario=SUPERVISORA),
         "next": f_tag},
        n_tag(f_tag, [TAG_FALLO], parent=f_notif),
        # Sin bot-silenciado a propósito: nadie tomó el lead, el bot sigue vivo.
    ]
    interno = arbol([("Asesor rescatado", [cond_has_value(K_ASESOR)], rama_ok)],
                    none_next=rama_fallo)

    # --- cadena de rescate (rama None del árbol externo) ---
    r_asig, r_wt1, r_upd = nid(), nid(), nid()
    cadena = [
        {"id": r_asig, "order": 0, "attributes": assign_attrs,
         "name": "Round Robin (6 asesores)", "type": "assign_user", "next": r_wt1},
        n_wait(r_wt1, 1, "minutes", nxt=r_upd, parent=r_asig),
        n_update(r_upd, [(K_ASESOR, "{{user.name}}"), (K_F_ASIGNA, "currentDate")],
                 nxt=interno[0]["id"], parent=r_wt1, name="Asesor + Fecha EN EL CONTACTO"),
    ]
    # el árbol interno cuelga del update: parentKey = quien te referencia por `next`
    interno[0]["parent"] = interno[0]["parentKey"] = r_upd

    externo = arbol([("Ya tiene asesor", [cond_has_value(K_ASESOR)], [])],
                    none_next=cadena)
    externo[0]["parent"] = externo[0]["parentKey"] = n_wt15

    return [n_wait(n_wt15, ESPERA_MIN, "minutes", nxt=externo[0]["id"])] + externo + interno


def main():
    aplicar = "--aplicar" in sys.argv

    ya = [w for w in (C.request("GET", f"/workflow/{LOC}") or [])
          if str(w.get("name", "")).startswith("SP07 |")]
    if ya:
        print(f"SKIP: ya existe {ya[0]['name']} ({ya[0]['id']}) — idempotencia §3")
        return

    d = C.request("GET", f"/workflow/{LOC}/{SP06}") or {}
    assign = next((n["attributes"] for n in
                   ((d.get("workflowData") or {}).get("templates") or [])
                   if n.get("type") == "assign_user"), None)
    if not assign:
        sys.exit("ABORT: no encontré el assign_user de SP06 — no invento el round robin")
    print(f"molde: round robin de SP06 · {assign.get('total_index')} asesores · "
          f"only_unassigned={assign.get('only_unassigned_contact')}")

    templates = construir(assign)
    print(f"plan: {NOMBRE} · {len(templates)} nodos · trigger tag `{TAG_ENTRADA}` · draft")
    if not aplicar:
        print("(simulación; --aplicar para crear)")
        return

    wf = C.request("POST", f"/workflow/{LOC}", {"name": NOMBRE, "parentId": CARPETA})
    wid = wf.get("id") if isinstance(wf, dict) else None
    if not wid:
        sys.exit(f"ABORT creando workflow: {wf}")
    print(f"workflow: {wid}")

    C.create_location_tag(TAG_OK)
    tb = {"status": "draft", "workflowId": wid, "schedule_config": {},
          "conditions": [{"operator": "index-of-true", "field": "tagsAdded",
                          "value": TAG_ENTRADA, "title": "Tag Added",
                          "type": "select", "id": "tag-added"}],
          "type": "contact_tag", "masterType": "highlevel",
          "name": f"Tag {TAG_ENTRADA} puesto", "allowMultiple": "yes",
          "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
          "active": True, "triggersChanged": True, "location_id": LOC}
    tr = C.request("POST", f"/workflow/{LOC}/trigger", tb)
    tid = tr.get("id") if isinstance(tr, dict) else None
    if not tid:
        sys.exit(f"ABORT creando trigger: {tr}")
    time.sleep(10)                       # el bucket de triggers es asíncrono
    C.request("PUT", f"/workflow/{LOC}/trigger/{tid}",
              {**tb, "targetActionId": templates[0]["id"],
               "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})

    r = C.request("PUT", f"/workflow/{LOC}/{wid}",
                  {"name": NOMBRE, "version": 1, "parentId": CARPETA, "status": "draft",
                   "allowMultiple": True, "workflowData": {"templates": templates}})
    if isinstance(r, dict) and r.get("_error"):
        sys.exit(f"ABORT en nodos: {str(r)[:300]}")

    v = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    tpl = (v.get("workflowData") or {}).get("templates") or []
    print(f"VERIFY: {v.get('status')} · {len(tpl)} nodos · reingreso={v.get('allowMultiple')}")
    for t in C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []:
        ok = t.get("targetActionId") == templates[0]["id"]
        print(f"  trigger [{t.get('type')}] {t.get('name')} · active={t.get('active')} · "
              f"entrada={'OK' if ok else 'ROTA'}")
    print(f"\nID nuevo: {wid} — publicar desde la UI (y 'Guardar trigger' al abrirlo)")


if __name__ == "__main__":
    main()
