import os, sys, json, pathlib
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient
LOC=os.environ["GHL_LOCATION_ID"]
tm=TokenManager()
print("token len:", len(tm.get_token() or ""))
c=InternalGHLClient(tm, LOC)
# READ-ONLY: list workflows/folders via internal workflow service
for p in [f"/workflow/{LOC}", f"/workflow/{LOC}/list", f"/workflows/{LOC}"]:
    r=c.request("GET", p)
    if r and not r.get("_error"):
        keys=list(r.keys()) if isinstance(r,dict) else type(r).__name__
        print(f"OK GET {p} -> keys={keys}")
        blob=json.dumps(r)[:300]
        print("   sample:", blob)
    else:
        print(f"fail GET {p} -> {(r or {}).get('code','401/None')}")
