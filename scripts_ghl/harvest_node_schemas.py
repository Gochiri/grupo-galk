"""Harvest one example of each workflow node 'type' present in this location,
to use as schema reference when building SP06."""
import os, sys, json, pathlib
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient
LOC=os.environ["GHL_LOCATION_ID"]
c=InternalGHLClient(TokenManager(), LOC)
wfs=c.request("GET", f"/workflow/{LOC}")
by_type={}
type_source={}
for w in wfs:
    if w.get("type")!="workflow": continue
    d=c.request("GET", f"/workflow/{LOC}/{w['id']}")
    if not isinstance(d,dict): continue
    tmpls=(d.get("workflowData") or {}).get("templates") or []
    for s in tmpls:
        t=s.get("type")
        if t and t not in by_type:
            by_type[t]=s
            type_source[t]=w["name"]
print("NODE TYPES FOUND:", len(by_type))
for t in sorted(by_type):
    print(f"  - {t}   (ej. en '{type_source[t]}')")
# dump the ones we need for SP06
NEED=["update_contact_field","if_else","condition","update_opportunity","webhook","send_internal_notification","internal_notification","add_contact_tag","round_robin","assign_user","wait"]
out={}
for t in by_type:
    out[t]={"source":type_source[t],"example":by_type[t]}
(ROOT/"scripts_ghl/node_schemas.json").write_text(json.dumps(out,ensure_ascii=False,indent=1))
print("\nsaved scripts_ghl/node_schemas.json")
