"""Helpers para construir workflows por API interna con los esquemas verificados."""
import os, sys, uuid, json, pathlib, time
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient

LOC=os.environ["GHL_LOCATION_ID"]
C=InternalGHLClient(TokenManager(), LOC)
CARPETAS=json.loads((ROOT/"scripts_ghl/carpetas_ghl.json").read_text())

PIPE="Pm48HGVyRbd5TAZDrKQS"
ST={"nuevo":"cff49047-ba9e-48a2-913d-502a9d7c3c5c","conversacion":"2af2c764-dda1-4c44-ba2a-80355ab654af",
    "ficha":"3c63e11a-ca60-4e35-b01c-a2e17fa9837f","calificado":"a8fc4fba-b821-44f4-9c22-f3d58636fadd",
    "asignado":"cad87dc6-85d5-4790-b399-2899d7949d97","pago_enviado":"6a31b31e-3b73-4aae-8156-e6cf41ec131a",
    "pago_validacion":"52655bf6-5718-44c2-9b32-abb5b4eeca25","matriculado":"adc03786-792f-4db7-9950-158a9a47b5ec",
    "perdido":"0d22f17e-6b1c-4c17-bc7c-4c22af5c179f"}
SUPERVISORA="w7Lzp83UoLfgFb9s8H8w"   # Lucía Galvez
GERMAN="mubBlotps59Jarh728fe"
PH_TEMPLATE="1596544212169540"       # PLACEHOLDER -> plantilla WABA (Fase 0.6)
PH_PHONE="1138517799350419"          # PLACEHOLDER -> número WABA (Fase 0.5)

_cf={f["fieldKey"]:f for f in api.get(f"/locations/{LOC}/customFields").get("customFields",[])}
def FID(k): return _cf[k]["id"]
def TITLE(k): return _cf[k]["name"]

NESTED=["inboundWebhookRequest","sheet","datetime_formatter","custom_webhook","array_functions","ivr_gather","ivr_connect_call","custom_code","ai_agent","task-notification"]
ALLOWIS=["contact_reply","inboundWebhookRequest","custom_webhook","custom_code","ai_agent","contact_detail","array_functions","appointment","service_booking","rental_booking"]
nid=lambda: str(uuid.uuid4())

def cond_field(key, val, op="contain"):
    return {"conditionType":"contact_detail","conditionSubType":FID(key),"conditionOperator":op,
            "conditionValue":val,"__conditionId":nid(),"ifElseNodeId":"","__customFieldType__":"standard",
            "isWait":False,"nestedDropdownTypes":NESTED,"allowIsOperatorTypes":ALLOWIS}

def cond_tag(tag):
    return {"conditionType":"contact_detail","conditionSubType":"tags","conditionOperator":"index-of-true",
            "conditionValue":[tag],"__conditionId":nid(),"ifElseNodeId":"","__customFieldType__":"standard",
            "isWait":False,"nestedDropdownTypes":NESTED,"allowIsOperatorTypes":ALLOWIS}

def n_update(nodo_id, campos, nxt="", parent=None, name="Update contact field"):
    """campos = [(fieldKey, valor)]"""
    fs=[{"field":FID(k),"value":v,"title":TITLE(k),
         "type":"date" if _cf[k]["dataType"]=="DATE" else "string",
         "date":v if _cf[k]["dataType"]=="DATE" else ""} for k,v in campos]
    n={"id":nodo_id,"order":0,"attributes":{"type":"update_contact_field","actionType":"update_field_data","fields":fs},
       "name":name,"type":"update_contact_field","next":nxt}
    if parent: n.update({"parent":parent,"parentKey":parent})
    return n

def n_tag(nodo_id, tags, nxt="", parent=None, quitar=False):
    t="remove_contact_tag" if quitar else "add_contact_tag"
    n={"id":nodo_id,"order":0,"attributes":{"tags":tags},"name":("Remove Tag" if quitar else "Add Tag"),"type":t,"next":nxt}
    if parent: n.update({"parent":parent,"parentKey":parent})
    return n

def n_opp(nodo_id, stage, nxt="", parent=None, status="open", name="Update opportunity", extra=None):
    a={"fields":[],"type":"create_opportunity","pipeline_id":PIPE,"pipeline_stage_id":stage,
       "opportunity_name":"{{contact.name}}","opportunity_status":status}
    if extra: a.update(extra)
    n={"id":nodo_id,"order":0,"attributes":a,"name":name,"type":"create_opportunity","next":nxt}
    if parent: n.update({"parent":parent,"parentKey":parent})
    return n

def n_wa(nodo_id, mensaje, nxt="", parent=None, media=None, name="WhatsApp"):
    a={"template_id":PH_TEMPLATE,"toggle_branch":False,"from_phone_number":PH_PHONE,
       "message":mensaje,"type":"whatsapp_v2","__customInputs__":{},"cat":"",
       "convertToMultipath":False,"transitions":[],"__name__":"WhatsApp"}
    if media: a["media_url"]=media
    n={"id":nodo_id,"order":0,"attributes":a,"name":name,"type":"whatsapp_v2",
       "cat":"","workflowsActionType":"INTERNAL","next":nxt}
    if parent: n.update({"parent":parent,"parentKey":parent})
    return n

def n_notif(nodo_id, titulo, cuerpo, usuario=None, tipo_user="assigned_user", parent=None):
    notif={"type":"send_notification","body":cuerpo,"title":titulo,"redirectPage":"conversation","userType":tipo_user}
    if usuario: notif["selectedUser"]=usuario
    n={"id":nodo_id,"order":0,"attributes":{"type":"notification","notification":notif},
       "name":"Internal Notification","type":"internal_notification"}
    if parent: n["parentKey"]=parent
    return n

def n_wait(nodo_id, valor, unidad="days", nxt="", parent=None):
    n={"id":nodo_id,"order":0,"attributes":{"type":"time","startAfter":{"type":unidad,"value":valor,"when":"after"},
       "name":"Wait","cat":"","timePeriodInputMode":"standard","unitInputMode":"standard",
       "isHybridAction":True,"hybridActionType":"wait","convertToMultipath":False,"transitions":[]},
       "name":"Wait","type":"wait","next":nxt}
    if parent: n.update({"parent":parent,"parentKey":parent})
    return n

def arbol(ramas, none_next=None):
    """ramas = [(nombre, [conditions], [nodos_de_la_rama])] -> devuelve lista de templates"""
    hid=nid(); noneid=nid(); bids=[]; out=[]; brs=[]
    for nombre, conds, nodos in ramas:
        bid=nid(); bids.append(bid)
        brs.append({"id":bid,"name":nombre,"segments":[{"__segmentId":nid(),"operator":"and","conditions":conds}]})
        primero = nodos[0]["id"] if nodos else ""
        out.append({"id":bid,"order":0,"attributes":{"if":False,"conditionName":"Condition","operator":"and","branches":[]},
                    "name":nombre,"type":"if_else","nodeType":"branch-yes","cat":"conditions",
                    "parent":hid,"parentKey":hid,"next":primero})
        for x in nodos:
            x.setdefault("parent",bid); x.setdefault("parentKey",bid)
            out.append(x)
    grupo=bids+[noneid]
    for o in out:
        if o.get("nodeType")=="branch-yes": o["sibling"]=[x for x in grupo if x!=o["id"]]
    head={"id":hid,"order":0,"attributes":{"currentRecipeType":"CUSTOM","branches":brs,"operator":"and",
          "if":True,"conditionName":"Condition","version":2,"noneBranchName":"None"},
          "name":"yes","type":"if_else","nodeType":"condition-node","cat":"conditions","next":grupo}
    nn={"id":noneid,"order":0,"attributes":{"else":True},"name":"None","type":"if_else",
        "nodeType":"branch-no","cat":"conditions","sibling":bids,"parent":hid,"parentKey":hid}
    if none_next:
        nn["next"]=none_next[0]["id"]
        for x in none_next:
            x.setdefault("parent",noneid); x.setdefault("parentKey",noneid)
    return [head]+out+[nn]+(none_next or [])

def crear(nombre, carpeta, templates, tag_trigger=None, trigger_name=None):
    fid=CARPETAS.get(carpeta)
    wf=C.request("POST", f"/workflow/{LOC}", {"name":nombre,"parentId":fid})
    wid=wf.get("id") if isinstance(wf,dict) else None
    if not wid: return None, f"ERROR creando: {wf}"
    if tag_trigger:
        C.create_location_tag(tag_trigger)
        tb={"status":"draft","workflowId":wid,"schedule_config":{},
            "conditions":[{"operator":"index-of-true","field":"tagsAdded","value":tag_trigger,
                           "title":"Tag Added","type":"select","id":"tag-added"}],
            "type":"contact_tag","masterType":"highlevel","name":trigger_name or tag_trigger,
            "allowMultiple":"no","actions":[{"workflow_id":wid,"type":"add_to_workflow"}],
            "active":True,"triggersChanged":True,"location_id":LOC}
        tr=C.request("POST", f"/workflow/{LOC}/trigger", tb)
        tid=tr.get("id") if isinstance(tr,dict) else None
        if tid:
            C.request("PUT", f"/workflow/{LOC}/trigger/{tid}",
                      {**tb,"targetActionId":templates[0]["id"],"advanceCanvasMeta":{"position":{"x":57.5,"y":-73}}})
    r=C.request("PUT", f"/workflow/{LOC}/{wid}", {"name":nombre,"version":1,"workflowData":{"templates":templates}})
    if isinstance(r,dict) and r.get("_error"): return wid, f"ERROR nodos: {str(r)[:120]}"
    d=C.request("GET", f"/workflow/{LOC}/{wid}")
    n=len((d.get("workflowData") or {}).get("templates") or [])
    return wid, f"OK {n} nodos"
