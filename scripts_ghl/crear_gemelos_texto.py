"""Crea los campos TEXT 'gemelos' que los bots SÍ pueden escribir.
Motivo: las acciones de Conversation AI no permiten escribir en campos dropdown
(SINGLE_OPTIONS). El bot escribe en el gemelo de texto y un workflow normaliza
ese valor al dropdown real."""
import os, sys, time, pathlib, requests
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
F_IDENT="R5Aa0kU4gDXkMAlQJUJp"; F_CALIF="LMLDqpaeMoec2OEeBkyb"

# (nombre, carpeta destino)
GEMELOS=[
 ("Familia de interés (bot)", F_IDENT),
 ("Modalidad (bot)",          F_CALIF),
 ("Sede (bot)",               F_CALIF),
 ("Pack x2 (bot)",            F_CALIF),
]

existing={f["name"].strip().lower(): f for f in api.get(f"/locations/{LOC}/customFields").get("customFields",[])}
creados={}
for name, folder in GEMELOS:
    if name.strip().lower() in existing:
        f=existing[name.strip().lower()]
        print(f"  SKIP {name} (ya existe · {f['fieldKey']})")
        creados[name]=f["fieldKey"]; continue
    r=requests.post(f"{BASE}/locations/{LOC}/customFields", headers=h,
                    json={"name":name,"dataType":"TEXT","model":"contact"}, timeout=30)
    if r.status_code in (200,201):
        cf=r.json().get("customField",{})
        # mover a su carpeta
        requests.put(f"{BASE}/locations/{LOC}/customFields/{cf['id']}", headers=h,
                     json={"name":name,"parentId":folder}, timeout=30)
        print(f"  OK   {name:<28} -> {cf.get('fieldKey')}")
        creados[name]=cf.get("fieldKey")
    else:
        print(f"  ERR  {name}: {r.text[:120]}")
    time.sleep(0.3)

print("\n=== KEYS PARA USAR EN LAS ACCIONES DEL BOT ===")
for n,k in creados.items():
    print(f"  {n:<28} {k}")
