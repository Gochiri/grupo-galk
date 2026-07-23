import os, sys, json, pathlib
ROOT = pathlib.Path("/home/user/grupo-galk")
for line in (ROOT / ".env").read_text().splitlines():
    line=line.strip()
    if line and not line.startswith("#") and "=" in line:
        k,v=line.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
LOC=os.environ["GHL_LOCATION_ID"]
pls=api.get("/opportunities/pipelines", params={"locationId":LOC}).get("pipelines",[])
for p in pls:
    print(f"\nPIPELINE: {p['name']}  (id={p['id']})  etapas={len(p.get('stages',[]))}")
    for s in p.get("stages",[]):
        print(f"  {s['position']}. {s['name']}")
