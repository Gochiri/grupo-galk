"""Build SP05 (envío de ficha · árbol 24 ramas) as a DRAFT via internal API.
Router if_else on curso + sede/modalidad → whatsapp_v2 per branch wired to the
matching Custom Value (§6: no hardcoded URLs). None branch → notify internal.
Structure mirrors HORARIOS - Drywall. template_id/from_phone are PLACEHOLDERS
(Fase 0.5/0.6). Never published."""
import os, sys, json, uuid, pathlib
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient
LOC=os.environ["GHL_LOCATION_ID"]
c=InternalGHLClient(TokenManager(), LOC)

CURSO="bjDW7b9QoRiFWL5d578w"; SEDE="B2tnsFlAOp9kYWF9Ij4R"; MODAL="M2Ra6FDckxrylnFygVVH"
PH_TEMPLATE="1596544212169540"   # PLACEHOLDER (Francisco/GoGHL) → reemplazar por plantilla WABA nueva (Fase 0.6)
PH_PHONE="1138517799350419"      # PLACEHOLDER → número WABA nuevo (Fase 0.5)
NESTED=["inboundWebhookRequest","sheet","datetime_formatter","custom_webhook","array_functions","ivr_gather","ivr_connect_call","custom_code","ai_agent","task-notification"]
ALLOWIS=["contact_reply","inboundWebhookRequest","custom_webhook","custom_code","ai_agent","contact_detail","array_functions","appointment","service_booking","rental_booking"]

def cond(field,val):
    return {"conditionType":"contact_detail","conditionSubType":field,"conditionOperator":"contain",
            "conditionValue":val,"__conditionId":str(uuid.uuid4()),"ifElseNodeId":"",
            "__customFieldType__":"standard","isWait":False,"nestedDropdownTypes":NESTED,"allowIsOperatorTypes":ALLOWIS}

# (nombre corto, [(field,val),...], custom_value_key)
FICHAS=[
 ("Melamina DC Surco",[(CURSO,"melamina desde cero"),(SEDE,"surco")],"ficha_melamina_desde_cero__surco"),
 ("Melamina DC Olivos",[(CURSO,"melamina desde cero"),(SEDE,"olivos")],"ficha_melamina_desde_cero__los_olivos"),
 ("Melamina DC Arequipa",[(CURSO,"melamina desde cero"),(SEDE,"arequipa")],"ficha_melamina_desde_cero__arequipa"),
 ("Melamina Av Surco",[(CURSO,"melamina avanzado"),(SEDE,"surco")],"ficha_melamina_avanzado__surco"),
 ("Melamina Av Olivos",[(CURSO,"melamina avanzado"),(SEDE,"olivos")],"ficha_melamina_avanzado__los_olivos"),
 ("Melamina Av Arequipa",[(CURSO,"melamina avanzado"),(SEDE,"arequipa")],"ficha_melamina_avanzado__arequipa"),
 ("Drywall DC Surco",[(CURSO,"drywall desde cero"),(SEDE,"surco")],"ficha_drywall_desde_cero__surco"),
 ("Drywall DC Olivos",[(CURSO,"drywall desde cero"),(SEDE,"olivos")],"ficha_drywall_desde_cero__los_olivos"),
 ("Drywall DC Arequipa",[(CURSO,"drywall desde cero"),(SEDE,"arequipa")],"ficha_drywall_desde_cero__arequipa"),
 ("Drywall Av Surco",[(CURSO,"drywall avanzado"),(SEDE,"surco")],"ficha_drywall_avanzado__surco"),
 ("Drywall Av Olivos",[(CURSO,"drywall avanzado"),(SEDE,"olivos")],"ficha_drywall_avanzado__los_olivos"),
 ("Drywall Av Arequipa",[(CURSO,"drywall avanzado"),(SEDE,"arequipa")],"ficha_drywall_avanzado__arequipa"),
 ("Electricidad Surco",[(CURSO,"electricidad"),(SEDE,"surco")],"ficha_electricidad_y_domtica__surco"),
 ("Electricidad Olivos",[(CURSO,"electricidad"),(SEDE,"olivos")],"ficha_electricidad_y_domtica__los_olivos"),
 ("SketchUp Online",[(CURSO,"sketchup"),(MODAL,"online")],"ficha_sketchup__online"),
 ("SketchUp Surco",[(CURSO,"sketchup"),(MODAL,"presencial")],"ficha_sketchup__presencial_surco"),
 ("Revit Online",[(CURSO,"revit"),(MODAL,"online")],"ficha_revit_bim__online"),
 ("Revit Surco",[(CURSO,"revit"),(MODAL,"presencial")],"ficha_revit_bim__presencial_surco"),
 ("Mobiliario Online",[(CURSO,"mobiliario"),(MODAL,"online")],"ficha_mobiliario__online"),
 ("AutoCAD Online",[(CURSO,"autocad"),(MODAL,"online")],"ficha_autocad__online"),
 ("Cocinas Online",[(CURSO,"cocinas")],"ficha_cocinas__online"),
 ("Obra Interiorista",[(CURSO,"interiorista")],"ficha_obra_interiorista__online"),
 ("Espacios Comerciales",[(CURSO,"espacios comerciales")],"ficha_espacios_comerciales__online"),
 ("Supervisión Melamina",[(CURSO,"supervisi")],"ficha_supervisin_melamina__online"),
]
assert len(FICHAS)==24

header_id=str(uuid.uuid4()); none_id=str(uuid.uuid4()); notif_id=str(uuid.uuid4())
branches=[]; nodes=[]; branch_next=[]; wa_ids={}
for name,conds,cvkey in FICHAS:
    bid=str(uuid.uuid4()); waid=str(uuid.uuid4()); wa_ids[bid]=waid
    branches.append({"id":bid,"name":name,"segments":[{"__segmentId":str(uuid.uuid4()),"operator":"and",
        "conditions":[cond(f,v) for f,v in conds]}]})
    branch_next.append(bid)
group=branch_next+[none_id]
for (name,conds,cvkey),bid in zip(FICHAS,branch_next):
    waid=wa_ids[bid]
    sib=[x for x in group if x!=bid]
    # branch-entry node (nodeType=branch-yes)
    nodes.append({"id":bid,"order":0,"attributes":{"if":False,"conditionName":"Condition","operator":"and","branches":[]},
        "name":name,"type":"if_else","nodeType":"branch-yes","cat":"conditions","sibling":sib,
        "parent":header_id,"parentKey":header_id,"next":waid})
    # whatsapp node (media = custom value) — needs workflowsActionType
    nodes.append({"id":waid,"order":0,"attributes":{"template_id":PH_TEMPLATE,"toggle_branch":False,
        "from_phone_number":PH_PHONE,"media_url":"{{custom_values.%s}}"%cvkey,
        "message":"¡Aquí tienes la información de tu curso! 👇\nCuéntame, ¿qué horario te acomoda mejor? 😊",
        "type":"whatsapp_v2","__customInputs__":{},"cat":"","convertToMultipath":False,"transitions":[],"__name__":"WhatsApp"},
        "name":"Ficha: "+name,"type":"whatsapp_v2","cat":"","workflowsActionType":"INTERNAL","parent":bid,"parentKey":bid,"next":""})

# header router node (condition-node, next=list)
header={"id":header_id,"order":0,"attributes":{"currentRecipeType":"CUSTOM","branches":branches,
    "operator":"and","if":True,"conditionName":"Condition","version":2,"noneBranchName":"None"},
    "name":"yes","type":"if_else","nodeType":"condition-node","cat":"conditions","next":branch_next+[none_id]}
# none branch + notify
none_node={"id":none_id,"order":0,"attributes":{"else":True},"name":"None","type":"if_else",
    "nodeType":"branch-no","cat":"conditions","sibling":branch_next,"parent":header_id,"parentKey":header_id,"next":notif_id}
notif={"id":notif_id,"order":0,"attributes":{"type":"notification","notification":{"type":"send_notification",
    "body":"Ficha no encontrada para {{contact.name}} — curso '{{contact.curso_de_inters}}' / sede '{{contact.sede}}' / modalidad '{{contact.modalidad}}'. Revisar catálogo.",
    "title":"⚠️ SP05: ficha sin match","redirectPage":"conversation","selectedUser":"mubBlotps59Jarh728fe","userType":"user"}},
    "name":"Avisar (sin match)","type":"internal_notification","parentKey":none_id}

templates=[header]+nodes+[none_node,notif]
print("total nodos:", len(templates), "(1 header + 24 ramas x2 + none + notif)")

# create draft
folder=c.request("GET", f"/workflow/{LOC}")
fid=[w for w in folder if w.get("name")=="SP · Pipeline de Ventas (NUEVO)" and w.get("type")=="directory"]
fid=fid[0]["id"] if fid else None
wf=c.request("POST", f"/workflow/{LOC}", {"name":"SP05 | Envío de ficha (árbol 24 ramas)","parentId":fid})
wid=wf.get("id") if isinstance(wf,dict) else None
print("workflow:", wid)
if not wid: print("ABORT", wf); sys.exit(1)
c.create_location_tag("enviar-ficha")
tb={"status":"draft","workflowId":wid,"schedule_config":{},
 "conditions":[{"operator":"index-of-true","field":"tagsAdded","value":"enviar-ficha","title":"Tag Added","type":"select","id":"tag-added"}],
 "type":"contact_tag","masterType":"highlevel","name":"Enviar Ficha","allowMultiple":"no",
 "actions":[{"workflow_id":wid,"type":"add_to_workflow"}],"active":True,"triggersChanged":True,"location_id":LOC}
tr=c.request("POST", f"/workflow/{LOC}/trigger", tb)
tid=tr.get("id") if isinstance(tr,dict) else None
print("trigger:", tid)
if tid: c.request("PUT", f"/workflow/{LOC}/trigger/{tid}", {**tb,"targetActionId":header_id,"advanceCanvasMeta":{"position":{"x":57.5,"y":-73}}})
put=c.request("PUT", f"/workflow/{LOC}/{wid}", {"name":"SP05 | Envío de ficha (árbol 24 ramas)","version":1,"workflowData":{"templates":templates}})
print("PUT ok:", bool(put and not (isinstance(put,dict) and put.get("_error"))), (put if isinstance(put,dict) and put.get("_error") else ""))
d=c.request("GET", f"/workflow/{LOC}/{wid}")
saved=(d.get("workflowData") or {}).get("templates") or []
print(f"VERIFY steps saved: {len(saved)}")
print("WORKFLOW_ID:", wid)
