"""Cambia el trigger de SP06 a un tag SIN colisión.
Motivo: 'lead-calificado' lo usa el WF1 de Francisco, que está PUBLICADO y vivo.
Si SP06 se publicaba, se disparaba con leads reales."""
import os, sys, pathlib
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient
LOC=os.environ["GHL_LOCATION_ID"]
c=InternalGHLClient(TokenManager(), LOC)

WID="84811c16-30d8-4c08-a05d-0c12fa46567d"   # SP06
TRIGGER="cWcPrqqFpsQyWkLAHcHm"
NUEVO_TAG="galk-bot-calificado"               # exclusivo del sistema nuevo

c.create_location_tag(NUEVO_TAG)
d=c.request("GET", f"/workflow/{LOC}/{WID}")
first=((d.get("workflowData") or {}).get("templates") or [{}])[0].get("id")

body={"status":"draft","workflowId":WID,"schedule_config":{},
 "conditions":[{"operator":"index-of-true","field":"tagsAdded","value":NUEVO_TAG,
                "title":"Tag Added","type":"select","id":"tag-added"}],
 "type":"contact_tag","masterType":"highlevel","name":"GALK Bot Calificado","allowMultiple":"no",
 "actions":[{"workflow_id":WID,"type":"add_to_workflow"}],"active":True,"triggersChanged":True,
 "location_id":LOC,"targetActionId":first,
 "advanceCanvasMeta":{"position":{"x":57.5,"y":-73}}}
r=c.request("PUT", f"/workflow/{LOC}/trigger/{TRIGGER}", body)
ok = bool(r and not (isinstance(r,dict) and r.get("_error")))
print(f"Trigger SP06 -> '{NUEVO_TAG}':", "OK" if ok else f"ERROR {r}")
