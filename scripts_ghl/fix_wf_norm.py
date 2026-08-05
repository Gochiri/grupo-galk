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


def harvest():
    """FASE 1 — vuelca los triggers de workflows vivos para copiar el schema exacto.

    No tenemos el schema de `triggers` documentado: los dumps que hay en el repo solo
    guardaron `workflowData.templates`. Sin esto no se puede crear un trigger a ciegas.
    """
    wfs = c.request("GET", f"/workflow/{LOC}")
    if not wfs or (isinstance(wfs, dict) and wfs.get("_error")):
        sys.exit(f"ABORT: la API interna no responde (¿token de Firebase caducado?) -> {wfs}")
    lista = wfs if isinstance(wfs, list) else wfs.get("workflows", [])
    muestras = []
    for w in lista:
        if w.get("type") == "directory":
            continue
        d = c.request("GET", f"/workflow/{LOC}/{w['id']}")
        trg = (d or {}).get("triggers") or []
        # nos interesan los que disparan por cambio de campo del contacto
        if any("contact" in json.dumps(t).lower() for t in trg):
            muestras.append({"workflow": w.get("name"), "triggers": trg})
        if len(muestras) >= 3:
            break
    out = ROOT / "scripts_ghl" / "trigger_schema_sample.json"
    out.write_text(json.dumps(muestras, ensure_ascii=False, indent=2))
    print(json.dumps(muestras, ensure_ascii=False, indent=2)[:4000])
    print(f"\nGuardado en {out}")
    print("\nSiguiente paso: rellenar construir_trigger() con este schema y correr --apply.")


def construir_trigger(campo_bot_id):
    """FASE 2 — trigger 'Contact Changed' sobre el campo (bot) de este workflow.

    PENDIENTE: completar con el schema real que devuelva --harvest. No lo inventamos:
    un trigger mal formado hace que el PUT devuelva 400 'corrupted type', que es
    exactamente el error que ya nos costó SP05.
    """
    raise NotImplementedError(
        "Corre primero --harvest y pega aquí el schema real del trigger."
    )


def apply():
    wfs = c.request("GET", f"/workflow/{LOC}")
    if not wfs or (isinstance(wfs, dict) and wfs.get("_error")):
        sys.exit(f"ABORT: la API interna no responde (¿token de Firebase caducado?) -> {wfs}")
    lista = wfs if isinstance(wfs, list) else wfs.get("workflows", [])
    carpeta = next((w["id"] for w in lista
                    if w.get("type") == "directory" and w.get("name") == "SP · Pipeline de Ventas (NUEVO)"),
                   None)
    existentes = {w.get("name"): w["id"] for w in lista if w.get("type") != "directory"}

    for spec in WORKFLOWS:
        nombre = spec["nombre"]
        if nombre in existentes:                      # idempotencia (§3)
            print(f"SKIP (ya existe): {nombre}")
            continue
        templates = construir_templates(spec)
        wf = c.request("POST", f"/workflow/{LOC}", {"name": nombre, "parentId": carpeta})
        wid = wf.get("id") if isinstance(wf, dict) else None
        if not wid:
            print(f"ERROR creando {nombre}: {wf}")
            continue
        body = {"name": nombre, "version": 1, "workflowData": {"templates": templates},
                "triggers": [construir_trigger(fid(spec["campo_bot"]))]}
        put = c.request("PUT", f"/workflow/{LOC}/{wid}", body)
        ok = bool(put and not (isinstance(put, dict) and put.get("_error")))
        d = c.request("GET", f"/workflow/{LOC}/{wid}") or {}
        n_nodos = len((d.get("workflowData") or {}).get("templates") or [])
        n_trg = len(d.get("triggers") or [])
        print(f"{'OK ' if ok else 'ERR'} {nombre}  id={wid}  nodos={n_nodos}  triggers={n_trg}")
        if n_trg == 0:
            print("   ⚠️  SIN TRIGGER — el workflow no se dispara con nada. Revisar.")


if __name__ == "__main__":
    if "--harvest" in sys.argv:
        harvest()
    elif "--apply" in sys.argv:
        apply()
    else:
        print(__doc__)
