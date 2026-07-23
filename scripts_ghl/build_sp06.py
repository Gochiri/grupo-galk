"""Build SP06 (Calificación y asignación) as a DRAFT workflow via internal API.
Nodes mirror schemas harvested from existing workflows in THIS location.
Never publishes. CAPI webhook + guard if_else are intentionally omitted (flagged)."""
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

PIPE="Pm48HGVyRbd5TAZDrKQS"
ST_CALIF="a8fc4fba-b821-44f4-9c22-f3d58636fadd"
ST_ASIG="cad87dc6-85d5-4790-b399-2899d7949d97"
F_CALIF="f4VzKV05rOxdyKX9rq1G"      # Calificado (SINGLE_OPTIONS)
F_FCALIF="aR0Dne9NV5FG5NyzYNDw"     # Fecha de calificación (DATE)
F_ASESOR="m36ikoz5RjrJFrtDh3kt"     # Asesor asignado (nuevo) (TEXT)
F_FASIG="z2mA0nEBefblpZaE3NZH"      # Fecha de asignación (DATE)
ASESORES=["IGRfggnJvAIkyAeMfycr","2O8FOfMSzbRtRMb1FnMf","izAqkNAiyM1zUWOYltFy",
          "6N9uVNvdpUCw8LdFnrzE","LCwIaJwIu1xcOAISNJsI","cRNnOExeNFPOoqvwC99z"]

def nid(): return str(uuid.uuid4())
n1,n2,n3,n4,n5,n6,n7=[nid() for _ in range(7)]

templates=[
 {"id":n1,"order":0,"attributes":{"type":"update_contact_field","actionType":"update_field_data","fields":[
    {"field":F_CALIF,"value":"Sí","title":"Calificado","type":"string","date":""},
    {"field":F_FCALIF,"value":"{{right_now}}","title":"Fecha de calificación","type":"date","date":"{{right_now}}"}]},
  "name":"Calificado = Sí + Fecha","type":"update_contact_field","next":n2},
 {"id":n2,"order":1,"attributes":{"fields":[],"type":"create_opportunity","pipeline_id":PIPE,
    "pipeline_stage_id":ST_CALIF,"opportunity_name":"{{contact.name}}","opportunity_source":"{{contact.fuente}}",
    "opportunity_status":"open"},"name":"Oportunidad → Calificado","type":"create_opportunity","next":n3},
 {"id":n3,"order":2,"attributes":{"only_unassigned_contact":False,"total_index":len(ASESORES),
    "traffic_split":"equally","traffic_weightage":{u:1 for u in ASESORES},
    "traffic_index":[{"id":u,"indexes":[i+1]} for i,u in enumerate(ASESORES)],
    "user_list":ASESORES,"type":"assign_user"},"name":"Round Robin (6 asesores)","type":"assign_user","next":n4},
 {"id":n4,"order":3,"attributes":{"type":"update_contact_field","actionType":"update_field_data","fields":[
    {"field":F_ASESOR,"value":"{{user.name}}","title":"Asesor asignado (nuevo)","type":"string","date":""},
    {"field":F_FASIG,"value":"{{right_now}}","title":"Fecha de asignación","type":"date","date":"{{right_now}}"}]},
  "name":"Asesor + Fecha EN EL CONTACTO","type":"update_contact_field","next":n5},
 {"id":n5,"order":4,"attributes":{"fields":[],"type":"create_opportunity","pipeline_id":PIPE,
    "pipeline_stage_id":ST_ASIG,"opportunity_name":"{{contact.name}}","opportunity_status":"open"},
  "name":"Oportunidad → Asignado a asesor","type":"create_opportunity","next":n6},
 {"id":n6,"order":5,"attributes":{"type":"notification","notification":{"type":"send_notification",
    "body":"Nuevo lead calificado asignado: {{contact.name}} ({{contact.phone}}) — {{contact.curso_de_inters}} / {{contact.sede}} / {{contact.horario_de_inters}}",
    "title":"🎯 Lead calificado asignado","redirectPage":"conversation","userType":"assigned_user"}},
  "name":"Notificar al asesor","type":"internal_notification","next":n7},
 {"id":n7,"order":6,"attributes":{"tags":["bot-silenciado"]},"name":"Add Tag: bot-silenciado","type":"add_contact_tag","next":""},
]

# 1) folder
folder=c.request("POST", f"/workflow/{LOC}", {"name":"SP · Pipeline de Ventas (NUEVO)","type":"directory"})
fid=folder.get("id") if isinstance(folder,dict) else None
print("folder:", fid)
# 2) workflow (draft)
wf=c.request("POST", f"/workflow/{LOC}", {"name":"SP06 | Calificación y asignación","parentId":fid})
wid=wf.get("id") if isinstance(wf,dict) else None
print("workflow:", wid)
if not wid: print("ABORT: no workflow id", wf); sys.exit(1)
# 3) tag + trigger
c.create_location_tag("lead-calificado")
tb={"status":"draft","workflowId":wid,"schedule_config":{},
 "conditions":[{"operator":"index-of-true","field":"tagsAdded","value":"lead-calificado","title":"Tag Added","type":"select","id":"tag-added"}],
 "type":"contact_tag","masterType":"highlevel","name":"Lead Calificado","allowMultiple":"no",
 "actions":[{"workflow_id":wid,"type":"add_to_workflow"}],"active":True,"triggersChanged":True,"location_id":LOC}
tr=c.request("POST", f"/workflow/{LOC}/trigger", tb)
tid=tr.get("id") if isinstance(tr,dict) else None
print("trigger:", tid)
if tid:
    c.request("PUT", f"/workflow/{LOC}/trigger/{tid}", {**tb,"targetActionId":n1,"advanceCanvasMeta":{"position":{"x":57.5,"y":-73}}})
# 4) save steps
put=c.request("PUT", f"/workflow/{LOC}/{wid}", {"name":"SP06 | Calificación y asignación","version":1,"workflowData":{"templates":templates}})
print("PUT steps ok:", bool(put and not (isinstance(put,dict) and put.get("_error"))))
# 5) verify
d=c.request("GET", f"/workflow/{LOC}/{wid}")
saved=(d.get("workflowData") or {}).get("templates") or []
print(f"VERIFY: workflow '{d.get('name')}' status={d.get('status')} steps={len(saved)}")
for s in saved: print("   -", s.get("order"), s.get("type"), "|", s.get("name"))
print("\nWORKFLOW_ID:", wid)
