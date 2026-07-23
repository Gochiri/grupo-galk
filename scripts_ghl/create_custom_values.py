"""SETUP-04: create the 24 ficha Custom Values (empty) via GHL public API.
Idempotent. Values empty on purpose — the RoasSeeker panel fills the real URLs
in Fase 0. Naming: 'Ficha <Curso> - <Sede/Modalidad>'."""
import os, sys, json, time, pathlib, requests
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
LOC=os.environ["GHL_LOCATION_ID"]
h=api._headers(path=f"/locations/{LOC}/customValues")
BASE="https://services.leadconnectorhq.com"

FICHAS=[
 # Talleres presenciales (14)
 "Ficha Melamina Desde Cero - Surco","Ficha Melamina Desde Cero - Los Olivos","Ficha Melamina Desde Cero - Arequipa",
 "Ficha Melamina Avanzado - Surco","Ficha Melamina Avanzado - Los Olivos","Ficha Melamina Avanzado - Arequipa",
 "Ficha Drywall Desde Cero - Surco","Ficha Drywall Desde Cero - Los Olivos","Ficha Drywall Desde Cero - Arequipa",
 "Ficha Drywall Avanzado - Surco","Ficha Drywall Avanzado - Los Olivos","Ficha Drywall Avanzado - Arequipa",
 "Ficha Electricidad y Domótica - Surco","Ficha Electricidad y Domótica - Los Olivos",
 # Software (6)
 "Ficha SketchUp - Online","Ficha SketchUp - Presencial Surco",
 "Ficha Revit BIM - Online","Ficha Revit BIM - Presencial Surco",
 "Ficha Mobiliario - Online","Ficha AutoCAD - Online",
 # Gestión (4)
 "Ficha Cocinas - Online","Ficha Obra Interiorista - Online",
 "Ficha Espacios Comerciales - Online","Ficha Supervisión Melamina - Online",
]
assert len(FICHAS)==24, len(FICHAS)

existing={cv["name"].strip().lower() for cv in api.get(f"/locations/{LOC}/customValues").get("customValues",[])}
ok=skip=err=0
for name in FICHAS:
    if name.strip().lower() in existing:
        print(f"  SKIP (existe) {name}"); skip+=1; continue
    r=requests.post(f"{BASE}/locations/{LOC}/customValues", headers=h, json={"name":name,"value":""}, timeout=30)
    if r.status_code in (200,201):
        cv=r.json().get("customValue",{})
        print(f"  OK  {name:<42} -> {cv.get('id','')}"); ok+=1
    else:
        print(f"  ERR {r.status_code} {name}: {r.text[:100]}"); err+=1
    time.sleep(0.25)
print(f"\nOK={ok} SKIP={skip} ERR={err} / 24")
