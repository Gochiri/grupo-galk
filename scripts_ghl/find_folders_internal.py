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
paths=[
 f"/custom-fields/?locationId={LOC}&model=contact",
 f"/custom-fields/folder?locationId={LOC}&model=contact",
 f"/locations/{LOC}/customFields/folder",
 f"/custom-fields/folders?locationId={LOC}",
 f"/custom-fields?locationId={LOC}&model=contact",
]
for p in paths:
    r=c.request("GET", p)
    if r and not r.get("_error"):
        keys=list(r.keys()) if isinstance(r,dict) else type(r)
        print("OK", p, "keys=", keys)
        # print any folder-like entries
        blob=json.dumps(r)
        for kk in ("folder","Folder"):
            if kk in blob:
                print("   (contains folder data)")
                print("   ", blob[:800]); break
    else:
        print("fail", p, "->", (r or {}).get("code","401/None"))
