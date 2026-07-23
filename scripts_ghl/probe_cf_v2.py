import os, sys, json, pathlib, requests
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
LOC=os.environ["GHL_LOCATION_ID"]
BASE="https://services.leadconnectorhq.com"
# v2 custom-fields uses version 2021-07-28; try object-key listing (fields + folders)
for ver in ["2021-07-28"]:
    h=api._headers(version=ver)
    for suffix in [
        f"/custom-fields/object-key/contact?locationId={LOC}",
        f"/custom-fields/object-key/opportunity?locationId={LOC}",
    ]:
        r=requests.get(BASE+suffix, headers=h, timeout=30)
        print(f"\nGET {suffix} [v{ver}] -> {r.status_code}")
        if r.status_code==200:
            j=r.json()
            print("  keys:", list(j.keys()))
            for fo in j.get("folders",[]):
                print("  FOLDER:", fo.get("id"), "|", fo.get("name"))
        else:
            print("  ", r.text[:200])
