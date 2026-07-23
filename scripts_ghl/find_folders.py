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

# 1) top-level keys of customFields response (maybe includes folders)
d=api.get(f"/locations/{LOC}/customFields")
print("customFields response top-level keys:", list(d.keys()))
if "folders" in d:
    for fo in d["folders"]:
        print("  FOLDER", fo)

# 2) dedicated v2 folder listing endpoints (read-only probes)
for suffix in [
    f"/locations/{LOC}/customFields?model=contact",
    f"/locations/{LOC}/customFields?model=opportunity",
]:
    r=requests.get("https://services.leadconnectorhq.com"+suffix, headers=h, timeout=30)
    try: j=r.json()
    except: j={}
    fkeys=list(j.keys()) if isinstance(j,dict) else "?"
    print(f"\nGET {suffix} -> {r.status_code} keys={fkeys}")
    if isinstance(j,dict) and j.get("folders"):
        for fo in j["folders"]:
            print("   FOLDER:", fo.get("id"), fo.get("name"), "model=", fo.get("model"))
