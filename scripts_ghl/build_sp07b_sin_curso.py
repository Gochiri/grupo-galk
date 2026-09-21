"""SP07-B — Rescate de leads que nunca dijeron qué curso quieren.

EL HUECO (medido el 21-sep sobre 630 leads de 7 días)
------------------------------------------------------
SP07 rescata al que recibió ficha y no respondió: entra por el tag `ficha-enviada`.
Pero el lead que escribe por la campaña y NUNCA nombra un curso no llega a tener
ficha — y sin ficha no hay tag, así que SP07 no lo ve. Nadie lo ve. Dos casos
reales que trajo Oliver (10-sep "Dirección en los olivos…", 16-sep "Taller de
surco"): Valeria prometió la información, el curso quedó vacío, la ficha nunca
salió y el lead se quedó esperando.

TAMAÑO REAL DEL PROBLEMA
------------------------
303 contactos de la semana quedaron sin curso, sin ficha y sin dueño. Pero 275
de ellos NO tienen teléfono ni el tag `origen-meta`: son handles de redes que la
plataforma crea por otra vía y que jamás pasaron por LS01 — otro asunto, no este.
Los leads de verdad atrapados son 24 en 7 días: ~3-4 por día. Por eso el trigger
es `origen-meta` (lo pone LS01 al entrar): aísla justo a esos y deja fuera al
ruido de redes.

EL DISEÑO
---------
Trigger: tag `origen-meta` puesto. 20 minutos de espera —más que los 15 de SP07,
para darle tiempo al bot y a los SP04 de detectar el curso— y dos guardas:

    ¿Tiene "Curso de interés"?  → sale: el sistema ya lo trabajó (SP05/SP07 siguen)
    ¿Tiene asesor asignado?     → sale: ya tiene dueño humano
    ninguna                     → round robin → 1 min → Asesor+Fecha → avisa

La notificación dice lo que le falta al asesor: este lead NO recibió información,
hay que preguntarle qué curso quiere. Es distinto del aviso de SP07, donde el
lead sí recibió su ficha.

Nada de `bot-silenciado`: Valeria sigue viva por si el lead responde y nombra su
curso — ahí SP05 dispara la ficha y el circuito se cierra solo.

Guarda nativa `assigned_to` (molde wf_lib.cond_assigned_to, capturado del SP07
que Oliver corrigió en la UI): también respeta asignaciones hechas a mano.

Como siempre: se crea en DRAFT. Publicar y "Guardar trigger" se hace en la UI.
"""
import os, sys, json, time, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import (C, LOC, SUPERVISORA, nid, n_update, n_tag, n_notif, n_wait,
                    arbol, cond_assigned_to)

NOMBRE      = "SP07-B | Rescate sin curso — lead de campaña sin ficha"
CARPETA     = "3dc6be37-5389-4385-9806-36722ba042ef"   # GALK 2.0 · 04 Sales Pipeline
SP06        = "84811c16-30d8-4c08-a05d-0c12fa46567d"   # molde del round robin
TAG_ENTRADA = "origen-meta"
TAG_OK      = "rescate-sin-curso"
TAG_FALLO   = "asignacion-fallida"
K_CURSO     = "contact.curso_de_inters"
K_ASESOR    = "contact.asesor_asignado_nuevo"
K_F_ASIGNA  = "contact.fecha_de_asignacin"
ESPERA_MIN  = 20


def cond_has_value(field_key):
    """has_value NO lleva conditionValue (molde de SP06 v2, verificado en vivo)."""
    return {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(field_key),
            "conditionOperator": "has_value", "__conditionId": nid(), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": wf_lib.NESTED, "allowIsOperatorTypes": wf_lib.ALLOWIS}


def construir(assign_attrs):
    n_wt20 = nid()

    # --- desenlace del rescate (árbol interno, molde SP07) ---
    s_notif, s_tag = nid(), nid()
    rama_ok = [
        {**n_notif(s_notif, "🆘 Lead sin curso — preguntarle qué le interesa",
                   "{{contact.name}} ({{contact.phone}}) escribió por la campaña hace "
                   "20 min pero no dijo qué curso quiere, así que el sistema NO pudo "
                   "enviarle información. Escríbele y pregúntale cuál le interesa."),
         "next": s_tag},
        n_tag(s_tag, [TAG_OK], parent=s_notif),
    ]
    f_notif, f_tag = nid(), nid()
    rama_fallo = [
        {**n_notif(f_notif, "⚠️ Round robin no asignó — lead sin dueño",
                   "El lead {{contact.name}} ({{contact.phone}}) lleva 20 min sin curso "
                   "detectado y el round robin no lo asignó. Tomarlo a mano.",
                   usuario=SUPERVISORA),
         "next": f_tag},
        n_tag(f_tag, [TAG_FALLO], parent=f_notif),
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
    interno[0]["parent"] = interno[0]["parentKey"] = r_upd

    # --- dos guardas: si ya tiene curso, o ya tiene dueño, no hay nada que rescatar ---
    externo = arbol([("Ya tiene curso", [cond_has_value(K_CURSO)], []),
                     ("Ya tiene asesor", [cond_assigned_to()], [])],
                    none_next=cadena)
    externo[0]["parent"] = externo[0]["parentKey"] = n_wt20

    return [n_wait(n_wt20, ESPERA_MIN, "minutes", nxt=externo[0]["id"])] + externo + interno


def main():
    aplicar = "--aplicar" in sys.argv

    ya = [w for w in (C.request("GET", f"/workflow/{LOC}") or [])
          if str(w.get("name", "")).startswith("SP07-B")]
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
    print(f"plan: {NOMBRE}\n      {len(templates)} nodos · trigger tag `{TAG_ENTRADA}` · "
          f"espera {ESPERA_MIN} min · draft")
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
    ids = {n["id"] for n in tpl}
    print(f"VERIFY: {v.get('status')} · {len(tpl)} nodos · reingreso={v.get('allowMultiple')}")
    for t in C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []:
        print(f"  trigger [{t.get('type')}] {t.get('name')} · active={t.get('active')} · "
              f"entrada={'OK' if t.get('targetActionId') in ids else 'ROTA'}")
    print(f"\nID nuevo: {wid} — publicar desde la UI (y 'Guardar trigger' al abrirlo)")


if __name__ == "__main__":
    main()
