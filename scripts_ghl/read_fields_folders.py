import os, sys, json, pathlib, requests
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
LOC=os.environ["GHL_LOCATION_ID"]

# Existing custom fields
d=api.get(f"/locations/{LOC}/customFields")
cf=d.get("customFields",[])
print(f"=== EXISTING FIELDS: {len(cf)} ===")
for f in cf:
    print(f"  model={f.get('model')} key={f.get('fieldKey')} name={f.get('name')!r} type={f.get('dataType')} parentId={f.get('parentId')}")

# Folders: try the customFields folders endpoint (read-only)
h=api._headers(path=f"/locations/{LOC}/customFields")
for url in [
    f"https://services.leadconnectorhq.com/locations/{LOC}/customFields/folders",
]:
    r=requests.get(url, headers=h, timeout=30)
    print(f"\n=== FOLDERS GET {url.split('/customFields')[1]} -> {r.status_code} ===")
    print(r.text[:1200])
