"""Organiza los workflows del sistema nuevo en carpetas con prefijo común.
Prefijo 'GALK 2.0 ·' => todas quedan juntas y se distinguen de las 40 heredadas.
Espeja las listas de ClickUp. Idempotente."""
import os, sys, json, time, pathlib
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient
LOC=os.environ["GHL_LOCATION_ID"]
c=InternalGHLClient(TokenManager(), LOC)

REG=ROOT/"scripts_ghl/carpetas_ghl.json"
CARPETAS=[
 "GALK 2.0 · 01 Setup y Normalización",
 "GALK 2.0 · 03 Lead Sources",
 "GALK 2.0 · 04 Sales Pipeline",
 "GALK 2.0 · 05 Pagos y Cierres",
 "GALK 2.0 · 06 Post-venta",
 "GALK 2.0 · 07 Reviews y Recompra",
]
# a qué carpeta va cada workflow (por prefijo del nombre)
DESTINO={
 "WF-NORM": "SP05":    "GALK 2.0 · 04 Sales Pipeline",
 "SP06":    "GALK 2.0 · 04 Sales Pipeline",
 "SP08":    "GALK 2.0 · 04 Sales Pipeline",
 "LS01":    "GALK 2.0 · 03 Lead Sources",
 "LS02":    "GALK 2.0 · 03 Lead Sources",
 "LS03":    "GALK 2.0 · 03 Lead Sources",
 "SP09":    "GALK 2.0 · 05 Pagos y Cierres",
 "SP10":    "GALK 2.0 · 05 Pagos y Cierres",
 "SP11":    "GALK 2.0 · 05 Pagos y Cierres",
 "SP12":    "GALK 2.0 · 05 Pagos y Cierres",
 "AP01":    "GALK 2.0 · 06 Post-venta",
 "AP02":    "GALK 2.0 · 06 Post-venta",
 "AP03":    "GALK 2.0 · 06 Post-venta",
 "AP04":    "GALK 2.0 · 06 Post-venta",
 "PS01":    "GALK 2.0 · 07 Reviews y Recompra",
 "PS02":    "GALK 2.0 · 07 Reviews y Recompra",
 "PS03":    "GALK 2.0 · 07 Reviews y Recompra",
}

reg = json.loads(REG.read_text()) if REG.exists() else {}
print("=== CARPETAS ===")
for nombre in CARPETAS:
    if nombre in reg:
        print(f"  SKIP {nombre}  ({reg[nombre]})"); continue
    r=c.request("POST", f"/workflow/{LOC}", {"name":nombre,"type":"directory"})
    fid=r.get("id") if isinstance(r,dict) else None
    if fid:
        reg[nombre]=fid; print(f"  OK   {nombre}  -> {fid}")
    else:
        print(f"  ERR  {nombre}: {r}")
    time.sleep(0.2)
REG.write_text(json.dumps(reg, ensure_ascii=False, indent=1))

print("\n=== MOVER WORKFLOWS ===")
wfs=c.request("GET", f"/workflow/{LOC}")
movidos=0
for w in wfs:
    if w.get("type")!="workflow": continue
    pref=w["name"].split(" ")[0].split("|")[0].strip()
    destino=DESTINO.get(pref)
    if not destino: continue                      # heredado de Francisco -> no tocar
    fid=reg.get(destino)
    if not fid: continue
    if w.get("parentId")==fid:
        print(f"  ya está  {w['name']}"); continue
    # PUT exige 'version'; incluimos workflowData tal cual para no perder los nodos
    actual=c.request("GET", f"/workflow/{LOC}/{w['id']}")
    body={"name":w["name"],"parentId":fid,"version":actual.get("version",1)}
    if isinstance(actual,dict) and actual.get("workflowData"):
        body["workflowData"]=actual["workflowData"]
    r=c.request("PUT", f"/workflow/{LOC}/{w['id']}", body)
    ok=bool(r and not (isinstance(r,dict) and r.get("_error")))
    if not ok: print("     detalle:", str(r)[:150])
    print(f"  {'OK  ' if ok else 'ERR '} {w['name']:<45} -> {destino}")
    movidos+=1 if ok else 0
    time.sleep(0.2)
print(f"\nmovidos: {movidos}")
