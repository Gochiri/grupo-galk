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

# WRITE test: create a throwaway folder (type=directory)
r=c.request("POST", f"/workflow/{LOC}", {"name":"__ztest_delete_me__","type":"directory"})
print("CREATE folder ->", json.dumps(r)[:300] if r else r)
fid = r.get("id") if isinstance(r,dict) else None
if not fid:
    print("WRITE FAILED (no id returned)"); sys.exit(0)
print("created folder id:", fid)

# Clean up: try to delete it
for method,path in [("DELETE", f"/workflow/{LOC}/{fid}")]:
    d=c.request(method, path)
    print(f"{method} {path} ->", json.dumps(d)[:200] if isinstance(d,(dict,list)) else d)

# verify it's gone
lst=c.request("GET", f"/workflow/{LOC}")
still=[x for x in lst if x.get("id")==fid] if isinstance(lst,list) else "?"
print("still present after delete?:", bool(still))
