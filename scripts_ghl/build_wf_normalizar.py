"""WF-NORM: normaliza los campos de texto que escribe el bot hacia los dropdowns reales.
Trigger: Contact Changed en cualquiera de los 4 campos '(bot)'.
11 ramas: Familia(3) + Modalidad(2) + Sede(4) + Pack x2(2). Draft."""
import os, sys, uuid, pathlib
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient
LOC=os.environ["GHL_LOCATION_ID"]
c=InternalGHLClient(TokenManager(), LOC)

cf={f["fieldKey"]:f for f in api.get(f"/locations/{LOC}/customFields").get("customFields",[])}
def fid(k): return cf[k]["id"]

NESTED=["inboundWebhookRequest","sheet","datetime_formatter","custom_webhook","array_functions","ivr_gather","ivr_connect_call","custom_code","ai_agent","task-notification"]
ALLOWIS=["contact_reply","inboundWebhookRequest","custom_webhook","custom_code","ai_agent","contact_detail","array_functions","appointment","service_booking","rental_booking"]

def cond(field_id, val):
    return {"conditionType":"contact_detail","conditionSubType":field_id,"conditionOperator":"contain",
            "conditionValue":val,"__conditionId":str(uuid.uuid4()),"ifElseNodeId":"",
            "__customFieldType__":"standard","isWait":False,
            "nestedDropdownTypes":NESTED,"allowIsOperatorTypes":ALLOWIS}

# (nombre rama, campo_bot_key, texto a detectar, campo_destino_key, título destino, valor final)
MAPEO=[
 ("Familia → Talleres","contact.familia_de_inters_bot","taller","contact.familia_de_inters","Familia de interés","Talleres"),
 ("Familia → Software","contact.familia_de_inters_bot","software","contact.familia_de_inters","Familia de interés","Software"),
 ("Familia → Gestion","contact.familia_de_inters_bot","gestion","contact.familia_de_inters","Familia de interés","Gestion"),
 ("Modalidad → Presencial","contact.modalidad_bot","presencial","contact.modalidad","Modalidad","Presencial"),
 ("Modalidad → Online","contact.modalidad_bot","online","contact.modalidad","Modalidad","Online"),
 ("Sede → Surco","contact.sede_bot","surco","contact.sede","Sede","Surco"),
 ("Sede → Los Olivos","contact.sede_bot","olivos","contact.sede","Sede","Los Olivos"),
 ("Sede → Arequipa","contact.sede_bot","arequipa","contact.sede","Sede","Arequipa"),
 ("Sede → No aplica","contact.sede_bot","no aplica","contact.sede","Sede","No aplica"),
 ("Pack x2 → Sí","contact.pack_x2_bot","s","contact.pack_x2","Pack x2","Sí"),
 ("Pack x2 → No","contact.pack_x2_bot","no","contact.pack_x2","Pack x2","No"),
]

header_id=str(uuid.uuid4()); none_id=str(uuid.uuid4())
branches=[]; nodes=[]; bids=[]
for nombre, k_bot, texto, k_dest, titulo, valor in MAPEO:
    bid=str(uuid.uuid4()); upd=str(uuid.uuid4()); bids.append(bid)
    branches.append({"id":bid,"name":nombre,"segments":[{"__segmentId":str(uuid.uuid4()),"operator":"and",
        "conditions":[cond(fid(k_bot), texto)]}]})
    nodes.append({"id":bid,"order":0,"attributes":{"if":False,"conditionName":"Condition","operator":"and","branches":[]},
        "name":nombre,"type":"if_else","nodeType":"branch-yes","cat":"conditions","parent":header_id,"parentKey":header_id,"next":upd})
    nodes.append({"id":upd,"order":0,"attributes":{"type":"update_contact_field","actionType":"update_field_data",
        "fields":[{"field":fid(k_dest),"value":valor,"title":titulo,"type":"string","date":""}]},
        "name":f"Set {titulo} = {valor}","type":"update_contact_field","parent":bid,"parentKey":bid,"next":""})

for n in nodes:
    if n.get("nodeType")=="branch-yes":
        n["sibling"]=[x for x in bids+[none_id] if x!=n["id"]]

header={"id":header_id,"order":0,"attributes":{"currentRecipeType":"CUSTOM","branches":branches,
    "operator":"and","if":True,"conditionName":"Condition","version":2,"noneBranchName":"None"},
    "name":"yes","type":"if_else","nodeType":"condition-node","cat":"conditions","next":bids+[none_id]}
none_node={"id":none_id,"order":0,"attributes":{"else":True},"name":"None","type":"if_else",
    "nodeType":"branch-no","cat":"conditions","sibling":bids,"parent":header_id,"parentKey":header_id}
templates=[header]+nodes+[none_node]
print("nodos:", len(templates))

wfs=c.request("GET", f"/workflow/{LOC}")
fid_dir=[w["id"] for w in wfs if w.get("name")=="SP · Pipeline de Ventas (NUEVO)" and w.get("type")=="directory"]
wf=c.request("POST", f"/workflow/{LOC}", {"name":"WF-NORM | Normalizar campos del bot","parentId":fid_dir[0] if fid_dir else None})
wid=wf.get("id") if isinstance(wf,dict) else None
print("workflow:", wid)
if not wid: print("ABORT", wf); sys.exit(1)
put=c.request("PUT", f"/workflow/{LOC}/{wid}", {"name":"WF-NORM | Normalizar campos del bot","version":1,"workflowData":{"templates":templates}})
print("PUT ok:", bool(put and not (isinstance(put,dict) and put.get("_error"))), put if isinstance(put,dict) and put.get("_error") else "")
d=c.request("GET", f"/workflow/{LOC}/{wid}")
print("VERIFY nodos guardados:", len((d.get("workflowData") or {}).get("templates") or []))
print("WORKFLOW_ID:", wid)
