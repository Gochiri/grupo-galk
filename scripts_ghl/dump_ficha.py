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
wfs=c.request("GET", f"/workflow/{LOC}")
for nm in ["FICHA - Drywall","HORARIOS - Drywall"]:
    w=[x for x in wfs if x["name"]==nm]
    if not w: print("not found",nm); continue
    d=c.request("GET", f"/workflow/{LOC}/{w[0]['id']}")
    tmpls=(d.get("workflowData") or {}).get("templates") or []
    print(f"\n########## {nm} — {len(tmpls)} nodos ##########")
    for s in tmpls:
        print(f"\n--- type={s.get('type')} name={s.get('name')!r} ---")
        print(json.dumps(s.get("attributes",{}), ensure_ascii=False)[:1400])
    (ROOT/f"scripts_ghl/dump_{nm.replace(' ','_').replace('-','')}.json").write_text(json.dumps(tmpls,ensure_ascii=False,indent=1))
