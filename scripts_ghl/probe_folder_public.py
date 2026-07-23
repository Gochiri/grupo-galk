import os, sys, json, pathlib, requests
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
LOC=os.environ["GHL_LOCATION_ID"]
h=api._headers(path=f"/locations/{LOC}/customFields")
BASE="https://services.leadconnectorhq.com"
# READ probes for a public folder-list endpoint
for suffix in [
    f"/locations/{LOC}/customFields/folder",
    f"/custom-fields/folder?locationId={LOC}",
]:
    r=requests.get(BASE+suffix, headers=h, timeout=30)
    print(f"GET {suffix} -> {r.status_code}: {r.text[:200]}")
