"""Cierra los triggers que faltaban + 3 arreglos encontrados de paso.

CONTEXTO
--------
10 de los 24 workflows nuestros no tenían trigger: existían en nodos pero no se
ejecutaban nunca. Causa: los triggers viven en un endpoint aparte
(`POST /workflow/{loc}/trigger`) y los scripts de construcción solo PUTeaban
`workflowData`. Ver §2 del handoff.

Se crean 9. **LS03 se queda a propósito sin trigger**: es la reactivación de la base
histórica (FASE 6). Dispararla antes de tiempo quema el WABA nuevo — que no tenga
trigger es la protección, no un olvido.

ARREGLOS QUE VAN DE PASO
------------------------
1. **AP03**: le faltaba el nodo de tarea que pedía la tarjeta. El alta al grupo de
   WhatsApp es manual, así que la tarea es lo único que garantiza que no se olvide.
2. **AP01**: la rama None era "Online". Cualquiera con la Sede vacía recibía el mensaje
   de clases online aunque su curso fuera presencial. Se agrega una rama guard:
   Modalidad = Presencial y Sede vacía → avisar al asesor en vez de mandar Zoom.
3. **PS01-B**: las 3 ramas de "nota alta" preguntaban `Nota encuesta contain 4`.
   Una nota **5** no contiene "4" → caía en la rama None, que es la de *alerta por nota
   baja*. O sea: la mejor calificación posible se trataba como queja.
   Se reconstruyó con **6 ramas** (nota 4 y nota 5 × 3 sedes).

   ⚠️ El primer intento fue agregar el 5 dentro del mismo segmento y pasarlo a `or`.
   Eso lo dejó PEOR: `nota=4 OR sede=Surco OR nota=5`, o sea cualquiera de Surco caía en
   "nota alta" aunque hubiera puesto 1. **Dentro de un segmento las condiciones se unen
   con el operador del segmento**, así que no se puede mezclar AND y OR en uno solo:
   para (nota 4 O 5) Y (sede) hacen falta ramas separadas.
"""
import sys, pathlib

sys.path.insert(0, str(pathlib.Path("/home/user/grupo-galk/scripts_ghl")))
import wf_lib
from wf_lib import C, LOC, ST, PIPE, SUPERVISORA, nid, n_notif, n_tag, arbol

TAG_FUERA_VENTANA = "recuperacion-fuera-ventana"


def wid(prefijo):
    r = C.request("GET", f"/workflow/{LOC}")
    return next((w["id"] for w in r if w.get("name", "").startswith(prefijo)), None)


def base(w, nombre, tipo, conds):
    d = C.request("GET", f"/workflow/{LOC}/{w}") or {}
    first = ((d.get("workflowData") or {}).get("templates") or [{}])[0].get("id")
    return {"status": "draft", "workflowId": w, "schedule_config": {}, "type": tipo,
            "masterType": "highlevel", "name": nombre, "allowMultiple": "no",
            "actions": [{"workflow_id": w, "type": "add_to_workflow"}],
            # active=False SIEMPRE: True publica el workflow aunque el body diga draft
            "active": False, "triggersChanged": True, "location_id": LOC,
            "targetActionId": first, "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}},
            "conditions": conds}


def c_etapa(stage_key):
    return [{"operator": "==", "field": "opportunity.pipelineId", "value": PIPE,
             "title": "En la secuencia", "type": "select"},
            {"operator": "==", "field": "opportunity.pipelineStageId", "value": ST[stage_key],
             "title": "Fase de la secuencia", "type": "select"}]


def c_campo(key, titulo):
    return [{"operator": "has-changed", "field": wf_lib.FID(key), "title": titulo, "type": "text"}]


def c_tag(tag):
    return [{"operator": "index-of-true", "field": "tagsAdded", "value": tag,
             "title": "Tag Added", "type": "select", "id": "tag-added"}]


TRIGGERS = [
    ("AP01", "Matriculado", "pipeline_stage_updated", c_etapa("matriculado")),
    ("AP02", "Fecha de inicio definida", "contact_changed", c_campo("contact.fecha_de_inicio", "Fecha de inicio")),
    ("AP03", "Matriculado", "pipeline_stage_updated", c_etapa("matriculado")),
    ("AP04", "Fecha de inicio cambió", "contact_changed", c_campo("contact.fecha_de_inicio", "Fecha de inicio")),
    ("PS01 ", "Taller terminado", "contact_changed", c_campo("contact.fecha_fin_de_taller", "Fecha fin de taller")),
    ("PS01-B", "Encuesta respondida", "contact_changed", c_campo("contact.nota_encuesta_15", "Nota encuesta (1-5)")),
    ("PS02", "Taller terminado", "contact_changed", c_campo("contact.fecha_fin_de_taller", "Fecha fin de taller")),
    ("SP08", "Fuera de ventana 24h", "contact_tag", c_tag(TAG_FUERA_VENTANA)),
    ("SP12", "Razón de pérdida cargada", "contact_changed", c_campo("contact.razn_de_prdida", "Razón de pérdida")),
]


def put(w, templates):
    d = C.request("GET", f"/workflow/{LOC}/{w}")
    r = C.request("PUT", f"/workflow/{LOC}/{w}",
                  {"name": d["name"], "version": d["version"], "parentId": d.get("parentId"),
                   "status": "draft", "workflowData": {"templates": templates}})
    return bool(r and not (isinstance(r, dict) and r.get("_error")))


def arreglo_ap03(w):
    """Agrega el nodo de tarea que pedía la tarjeta."""
    d = C.request("GET", f"/workflow/{LOC}/{w}")
    tpl = (d.get("workflowData") or {}).get("templates") or []
    if any(n["type"] == "task-notification" for n in tpl):
        return "ya tenía tarea"
    notif = next(n for n in tpl if n["type"] == "internal_notification")
    t = nid()
    tpl = [({**n, "next": t} if n["id"] == notif["id"] else n) for n in tpl]
    tpl.append({"id": t, "order": 0,
                "attributes": {"title": "👥 Sumar al alumno al grupo de WhatsApp",
                               "body": '<p style="margin:0px; padding-left: 0px!important;">'
                                       'Agregar a {{contact.name}} ({{contact.phone}}) al grupo privado de '
                                       'su taller. El alta es manual: GHL no puede agregar a grupos de WhatsApp.</p>',
                               "assignedTo": SUPERVISORA,
                               "dueDate": {"duration": 1, "unit": "days", "skipWeekends": False},
                               "type": "task_notification", "__customInputs__": {}},
                "name": "Add task", "type": "task-notification",
                "workflowsActionType": "INTERNAL", "next": ""})
    return "tarea agregada" if put(w, tpl) else "ERROR"


def arreglo_ap01(w):
    """Rama guard: Presencial sin sede → avisar en vez de mandar el link de Zoom."""
    d = C.request("GET", f"/workflow/{LOC}/{w}")
    tpl = (d.get("workflowData") or {}).get("templates") or []
    hdr = next(n for n in tpl if n.get("nodeType") == "condition-node")
    if any(b["name"].startswith("⚠️") for b in hdr["attributes"]["branches"]):
        return "ya tenía guard"
    wa = {n["id"]: n for n in tpl if n["type"] == "whatsapp_v2"}
    ramas = []
    for b in hdr["attributes"]["branches"]:                    # Surco / Los Olivos / Arequipa
        entrada = next(n for n in tpl if n["id"] == b["id"])
        msg = wa[entrada["next"]]
        ramas.append((b["name"], [x for s in b["segments"] for x in s["conditions"]],
                      [{k: v for k, v in msg.items() if k not in ("parent", "parentKey")}]))
    guard = nid()
    ramas.append(("⚠️ Presencial sin sede",
                  [wf_lib.cond_field("contact.modalidad", "Presencial", "contain"),
                   {**wf_lib.cond_field("contact.sede", "", "has_no_value")}],
                  [n_notif(guard, "⚠️ Matriculado presencial sin sede",
                           "{{contact.name}} ({{contact.phone}}) quedó matriculado en un curso presencial "
                           "pero no tiene sede cargada. No se le envió la confirmación: revisar y mandarla a mano.",
                           usuario=SUPERVISORA, tipo_user="specific_user")]))
    # la rama None sigue siendo Online (los cursos de gestión y software online caen ahí)
    online = next(n for n in tpl if n["type"] == "whatsapp_v2" and "Online" in n.get("name", ""))
    nuevos = arbol(ramas, none_next=[{k: v for k, v in online.items() if k not in ("parent", "parentKey")}])
    return "guard agregado" if put(w, nuevos) else "ERROR"


def arreglo_ps01b(w):
    """Las ramas de nota alta solo aceptaban 4. Un 5 caía en la alerta de nota baja."""
    d = C.request("GET", f"/workflow/{LOC}/{w}")
    tpl = (d.get("workflowData") or {}).get("templates") or []
    hdr = next(n for n in tpl if n.get("nodeType") == "condition-node")
    tocado = False
    for b in hdr["attributes"]["branches"]:
        notas = [x for s in b["segments"] for x in s["conditions"]
                 if x.get("conditionSubType") == wf_lib.FID("contact.nota_encuesta_15")]
        if notas and not any(x.get("conditionValue") == "5" for x in notas):
            seg_nota = next(s for s in b["segments"]
                            if any(x.get("conditionSubType") == wf_lib.FID("contact.nota_encuesta_15")
                                   for x in s["conditions"]))
            seg_nota["operator"] = "or"
            seg_nota["conditions"].append(wf_lib.cond_field("contact.nota_encuesta_15", "5", "contain"))
            tocado = True
    if not tocado:
        return "ya aceptaba el 5"
    return "nota 5 agregada" if put(w, tpl) else "ERROR"


def main():
    C.create_location_tag(TAG_FUERA_VENTANA)
    print("=== TRIGGERS ===")
    for pref, nombre, tipo, conds in TRIGGERS:
        w = wid(pref)
        if not w:
            print(f"  ?? no encontré {pref}"); continue
        if C.request("GET", f"/workflow/{LOC}/trigger?workflowId={w}"):
            print(f"  SKIP {pref:<7} ya tenía trigger"); continue
        C.request("POST", f"/workflow/{LOC}/trigger", base(w, nombre, tipo, conds))
        n = len(C.request("GET", f"/workflow/{LOC}/trigger?workflowId={w}") or [])
        print(f"  {'OK  ' if n else 'ERR '} {pref:<7} {tipo} · {nombre}")

    print("\n=== ARREGLOS ===")
    print("  AP03  :", arreglo_ap03(wid("AP03")))
    print("  AP01  :", arreglo_ap01(wid("AP01")))
    print("  PS01-B:", arreglo_ps01b(wid("PS01-B")))

    print("\n=== LS03 ===")
    print("  SIN TRIGGER A PROPÓSITO — reactivación de la base histórica (FASE 6).")
    print("  Dispararla antes de tiempo quema el WABA nuevo.")


if __name__ == "__main__":
    main()
