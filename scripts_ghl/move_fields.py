"""Move custom fields into a target folder by PUT parentId.
Usage: python move_fields.py <folderId> <key1> <key2> ..."""
import os, sys, json, time, pathlib, requests
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

folder_id=sys.argv[1]
keys=set(sys.argv[2:])
cf=api.get(f"/locations/{LOC}/customFields").get("customFields",[])
bykey={f["fieldKey"]:f for f in cf}
for key in sys.argv[2:]:
    f=bykey.get(key)
    if not f:
        print(f"  NOT FOUND {key}"); continue
    body={"name":f["name"],"parentId":folder_id}
    r=requests.put(f"{BASE}/locations/{LOC}/customFields/{f['id']}", headers=h, json=body, timeout=30)
    if r.status_code in (200,201):
        newp=r.json().get("customField",{}).get("parentId")
        print(f"  OK {key:<35} parentId->{newp}")
    else:
        print(f"  ERR {r.status_code} {key}: {r.text[:120]}")
    time.sleep(0.2)
