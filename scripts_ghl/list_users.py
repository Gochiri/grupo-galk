import os, sys, json, pathlib, requests
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
LOC=os.environ["GHL_LOCATION_ID"]
h=api._headers(path="/users/")
BASE="https://services.leadconnectorhq.com"
r=requests.get(f"{BASE}/users/", headers=h, params={"locationId":LOC}, timeout=30)
print("GET /users ->", r.status_code)
if r.status_code==200:
    users=r.json().get("users",[])
    print("total users:", len(users))
    for u in users:
        print(f"  {u.get('id')} | {u.get('name')} | {u.get('email')} | roles={ (u.get('roles') or {}).get('role') }")
else:
    print(r.text[:300])
