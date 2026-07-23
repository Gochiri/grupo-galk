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
# Test folder creation (v2). Use a temp probe name to avoid duplicating a real folder.
body={"name":"__ztest_folder__","model":"contact","locationId":LOC}
for suffix in [f"/locations/{LOC}/customFields/folder"]:
    r=requests.post(BASE+suffix, headers=h, json=body, timeout=30)
    print(f"POST {suffix} -> {r.status_code}: {r.text[:400]}")
    if r.status_code in (200,201):
        fid=(r.json().get("id") or r.json().get("customField",{}).get("id"))
        print("  created folder id:", r.json())
