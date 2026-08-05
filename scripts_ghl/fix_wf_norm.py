"""WF-NORM v2 — corrige los 3 defectos del WF-NORM original.

CONTEXTO
--------
El WF-NORM original (e97e101e-4f92-4fc4-8ad4-72d4f2907a95, 27-jul) mete los 4 campos
en UN SOLO if_else de 11 ramas. En GHL las ramas de un if_else son excluyentes:
**gana la primera que matchea y el resto ni se evalúa**. Como `Familia` siempre viene
llena (la escribe BOT-00), en la práctica nunca se normaliza Modalidad, Sede ni Pack x2.

Defectos corregidos:
  1. UN if_else para 4 campos  → 4 workflows independientes, uno por campo.
  2. Pack x2 "contains s"      → `is` exacto. Antes, "no gracias" contiene "s" y la rama
                                 Sí va primero → Pack x2 quedaba en Sí. Dato erróneo que
                                 cambia el precio que se le cotiza al lead.
  3. "gestion" sin tilde       → rama con segmentos OR: "gestion" y "gestión".

Además el script original NUNCA creó triggers (solo PUTeaba workflowData), así que el
workflow no se dispara con nada. Ver FASE 2 abajo.

USO
---
    .venv/bin/python scripts_ghl/fix_wf_norm.py --harvest   # FASE 1: ver schema de trigger
    .venv/bin/python scripts_ghl/fix_wf_norm.py --apply     # FASE 2: crear los 4 workflows

Requiere GHL_FIREBASE_REFRESH_TOKEN vivo (la API interna da 401 con uno caducado).
"""
import os, sys, uuid, json, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
for l in (ROOT / ".env").read_text().splitlines():
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient

LOC = os.environ["GHL_LOCATION_ID"]
c = InternalGHLClient(TokenManager(), LOC)

NESTED = ["inboundWebhookRequest", "sheet", "datetime_formatter", "custom_webhook",
          "array_functions", "ivr_gather", "ivr_connect_call", "custom_code", "ai_agent",
          "task-notification"]
ALLOWIS = ["contact_reply", "inboundWebhookRequest", "custom_webhook", "custom_code",
           "ai_agent", "contact_detail", "array_functions", "appointment",
           "service_booking", "rental_booking"]

cf = {f["fieldKey"]: f for f in api.get(f"/locations/{LOC}/customFields").get("customFields", [])}


def fid(key):
    if key not in cf:
        sys.exit(f"ABORT: no existe el campo {key}")
    return cf[key]["id"]


def cond(field_id, op, val):
    return {"conditionType": "contact_detail", "conditionSubType": field_id,
            "conditionOperator": op, "conditionValue": val,
            "__conditionId": str(uuid.uuid4()), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": NESTED, "allowIsOperatorTypes": ALLOWIS}


def segments(field_id, op, valores):
    """Varios valores = varios segmentos con operator 'or' (schema verificado en un
    workflow vivo de la subcuenta: dump_FICHA__Drywall.json)."""
    return [{"__segmentId": str(uuid.uuid4()), "operator": "or",
             "conditions": [cond(field_id, op, v)]} for v in valores]


# ---------------------------------------------------------------------------
# Los 4 workflows. El ORDEN de las ramas importa: gana la primera que matchea.
# ---------------------------------------------------------------------------
WORKFLOWS = [
    {
        "nombre": "WF-NORM-1 | Normalizar Familia de interés",
        "campo_bot": "contact.familia_de_inters_bot",
        "campo_dest": "contact.familia_de_inters",
        "titulo": "Familia de interés",
        "ramas": [
            ("Familia → Talleres", "contain", ["taller"], "Talleres"),
            ("Familia → Software", "contain", ["software"], "Software"),
            ("Familia → Gestion",  "contain", ["gestion", "gestión"], "Gestion"),
        ],
    },
    {
        "nombre": "WF-NORM-2 | Normalizar Modalidad",
        "campo_bot": "contact.modalidad_bot",
        "campo_dest": "contact.modalidad",
        "titulo": "Modalidad",
        "ramas": [
            ("Modalidad → Presencial", "contain", ["presencial"], "Presencial"),
            ("Modalidad → Online",     "contain", ["online"],     "Online"),
        ],
    },
    {
        "nombre": "WF-NORM-3 | Normalizar Sede",
        "campo_bot": "contact.sede_bot",
        "campo_dest": "contact.sede",
        "titulo": "Sede",
        "ramas": [
            # "no aplica" primero: si fuera al final, nada lo pisa, pero deja explícito
            # que es el caso por defecto de los cursos online.
            ("Sede → No aplica",  "contain", ["no aplica"], "No aplica"),
            ("Sede → Surco",      "contain", ["surco"],     "Surco"),
            ("Sede → Los Olivos", "contain", ["olivos"],    "Los Olivos"),
            ("Sede → Arequipa",   "contain", ["arequipa"],  "Arequipa"),
        ],
    },
    {
        "nombre": "WF-NORM-4 | Normalizar Pack x2",
        "campo_bot": "contact.pack_x2_bot",
        "campo_dest": "contact.pack_x2",
        "titulo": "Pack x2",
        "ramas": [
            # `is` EXACTO, no `contain`. Y "No" va primero. Los dos cambios son a
            # propósito: con `contain "s"` cualquier frase con una ese caía en Sí.
            ("Pack x2 → No", "is", ["No", "no", "NO"],             "No"),
            ("Pack x2 → Sí", "is", ["Si", "Sí", "si", "sí", "SI"], "Sí"),
        ],
    },
]


def construir_templates(spec):
    """Devuelve la lista de nodos de un workflow: 1 if_else + N ramas + N updates + None."""
    f_bot, f_dest = fid(spec["campo_bot"]), fid(spec["campo_dest"])
    header_id, none_id = str(uuid.uuid4()), str(uuid.uuid4())
    branches, nodes, bids = [], [], []

    for nombre, op, valores, valor_final in spec["ramas"]:
        bid, upd = str(uuid.uuid4()), str(uuid.uuid4())
        bids.append(bid)
        branches.append({"id": bid, "name": nombre, "segments": segments(f_bot, op, valores)})
        nodes.append({"id": bid, "order": 0,
                      "attributes": {"if": False, "conditionName": "Condition",
                                     "operator": "and", "branches": []},
                      "name": nombre, "type": "if_else", "nodeType": "branch-yes",
                      "cat": "conditions", "parent": header_id, "parentKey": header_id,
                      "next": upd})
        nodes.append({"id": upd, "order": 0,
                      "attributes": {"type": "update_contact_field",
                                     "actionType": "update_field_data",
                                     "fields": [{"field": f_dest, "value": valor_final,
                                                 "title": spec["titulo"], "type": "string",
                                                 "date": ""}]},
                      "name": f"Set {spec['titulo']} = {valor_final}",
                      "type": "update_contact_field", "parent": bid, "parentKey": bid,
                      "next": ""})

    for n in nodes:
        if n.get("nodeType") == "branch-yes":
            n["sibling"] = [x for x in bids + [none_id] if x != n["id"]]

    header = {"id": header_id, "order": 0,
              "attributes": {"currentRecipeType": "CUSTOM", "branches": branches,
                             "operator": "and", "if": True, "conditionName": "Condition",
                             "version": 2, "noneBranchName": "None"},
              "name": "yes", "type": "if_else", "nodeType": "condition-node",
              "cat": "conditions", "next": bids + [none_id]}
    none_node = {"id": none_id, "order": 0, "attributes": {"else": True}, "name": "None",
                 "type": "if_else", "nodeType": "branch-no", "cat": "conditions",
                 "sibling": bids, "parent": header_id, "parentKey": header_id}
    return [header] + nodes + [none_node]


CARPETA = "af354b55-6cf2-44e8-a062-da45855f7175"   # GALK 2.0 · 01 Setup y Normalización


def crear_trigger(wid, campo_bot_key, titulo, target_action_id):
    """Trigger 'Contact Changed' sobre el campo (bot).

    Schema cosechado de 'WF3 | Notificación al Asesor', el único contact_changed vivo
    de la subcuenta. Los triggers NO viajan dentro del objeto workflow: van en
    `POST /workflow/{loc}/trigger` y se leen con `GET .../trigger?workflowId=`.
    Para un campo custom, `field` es el ID del campo (no el fieldKey).
    """
    body = {"status": "draft", "workflowId": wid, "schedule_config": {},
            "conditions": [{"operator": "has-changed", "field": fid(campo_bot_key),
                            "title": titulo, "type": "text"}],
            "type": "contact_changed", "masterType": "highlevel",
            "name": f"{titulo} cambió", "allowMultiple": "no",
            "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
            "active": True, "triggersChanged": True, "location_id": LOC,
            "targetActionId": target_action_id,
            "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}}
    r = c.request("POST", f"/workflow/{LOC}/trigger", body)
    return r.get("id") if isinstance(r, dict) else None


def apply():
    wfs = c.request("GET", f"/workflow/{LOC}")
    if not wfs or (isinstance(wfs, dict) and wfs.get("_error")):
        sys.exit(f"ABORT: la API interna no responde (¿token de Firebase caducado?) -> {wfs}")
    lista = wfs if isinstance(wfs, list) else wfs.get("workflows", [])
    existentes = {w.get("name"): w["id"] for w in lista if w.get("type") != "directory"}

    for spec in WORKFLOWS:
        nombre = spec["nombre"]
        templates = construir_templates(spec)
        wid = existentes.get(nombre)
        if not wid:                                    # idempotencia (§3): no duplica
            wf = c.request("POST", f"/workflow/{LOC}", {"name": nombre, "parentId": CARPETA})
            wid = wf.get("id") if isinstance(wf, dict) else None
            if not wid:
                print(f"ERROR creando {nombre}: {wf}")
                continue

        # OJO: el PUT reescribe el objeto entero. Si no reenvías workflowData, pierdes
        # los nodos — el error que ya costó SP05.
        put = c.request("PUT", f"/workflow/{LOC}/{wid}",
                        {"name": nombre, "version": 1, "parentId": CARPETA,
                         "workflowData": {"templates": templates}})
        ok = bool(put and not (isinstance(put, dict) and put.get("_error")))

        d = c.request("GET", f"/workflow/{LOC}/{wid}") or {}
        first = ((d.get("workflowData") or {}).get("templates") or [{}])[0].get("id")
        trg = c.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []
        if not trg:
            crear_trigger(wid, spec["campo_bot"], spec["titulo"] + " (bot)", first)
            trg = c.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []

        n_nodos = len((d.get("workflowData") or {}).get("templates") or [])
        print(f"{'OK ' if ok else 'ERR'} {nombre}")
        print(f"      id={wid}  nodos={n_nodos}  triggers={len(trg)}  status={d.get('status') or 'draft'}")
        if not trg:
            print("      ⚠️  SIN TRIGGER — no se dispara con nada.")


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    else:
        print(__doc__)
