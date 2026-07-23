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

# idempotency: skip if 'Modalidad' already exists
ex=api.get(f"/locations/{LOC}/customFields").get("customFields",[])
if any(f["name"].strip().lower()=="modalidad" for f in ex):
    print("Modalidad already exists — skipping create."); sys.exit(0)

body={"name":"Modalidad","dataType":"SINGLE_OPTIONS","model":"contact",
      "options":["Presencial","Online"]}
r=requests.post(f"{BASE}/locations/{LOC}/customFields", headers=h, json=body, timeout=30)
print("POST status:", r.status_code)
print(json.dumps(r.json(), ensure_ascii=False)[:700])
