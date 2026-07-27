"""Crea los tags y custom values operativos que faltan para bots y workflows.
Idempotente: salta lo que ya existe."""
import os, sys, time, pathlib, requests
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient
LOC=os.environ["GHL_LOCATION_ID"]
BASE="https://services.leadconnectorhq.com"

# ---------- TAGS ----------
TAGS=[
 # ciclo del bot / calificación
 "bot-silenciado",       # SP06 silencia al bot tras asignar
 "origen-meta",          # LS01 marca leads de CTWA
 # seguimiento
 "recuperacion-enviada", # SP08 fuera de ventana
 # post-venta
 "matriculado",          # SP11
 "alumno-activo",        # AP03/AP04 — alumnos en curso
 "reintento-60d",        # PS03
 # razones de pérdida (SP12) — 7 ramas
 "perdido-precio","perdido-solo-informacion","perdido-ya-se-matriculo",
 "perdido-no-responde","perdido-horario-sede","perdido-sin-presupuesto","perdido-otro",
]
existing={t["name"].strip().lower() for t in api.get(f"/locations/{LOC}/tags").get("tags",[])}
c=InternalGHLClient(TokenManager(), LOC)
print("=== TAGS ===")
ok=skip=err=0
for t in TAGS:
    if t in existing:
        print(f"  SKIP {t}"); skip+=1; continue
    if c.create_location_tag(t):
        print(f"  OK   {t}"); ok+=1
    else:
        print(f"  ERR  {t}"); err+=1
    time.sleep(0.2)
print(f"  → OK={ok} SKIP={skip} ERR={err}")

# ---------- CUSTOM VALUES OPERATIVOS ----------
# (nombre, valor por defecto). Vacíos = los llena el cliente en Fase 0.
CVS=[
 ("Yape - Número",""),
 ("Plin - Número",""),
 ("Link de pago con tarjeta",""),
 ("Dirección sede Surco",""),
 ("Dirección sede Los Olivos",""),
 ("Dirección sede Arequipa",""),
 ("Link Zoom clases online",""),
 ("Link reseña Google Surco",""),
 ("Link reseña Google Los Olivos",""),
 ("Link reseña Google Arequipa",""),
 ("Link grupo WhatsApp",""),
 ("Link encuesta satisfacción",""),
]
h=api._headers(path=f"/locations/{LOC}/customValues")
have={v["name"].strip().lower() for v in api.get(f"/locations/{LOC}/customValues").get("customValues",[])}
print("\n=== CUSTOM VALUES ===")
ok=skip=err=0
for name,val in CVS:
    if name.strip().lower() in have:
        print(f"  SKIP {name}"); skip+=1; continue
    r=requests.post(f"{BASE}/locations/{LOC}/customValues", headers=h, json={"name":name,"value":val}, timeout=30)
    if r.status_code in (200,201):
        print(f"  OK   {name}"); ok+=1
    else:
        print(f"  ERR  {name}: {r.text[:90]}"); err+=1
    time.sleep(0.25)
print(f"  → OK={ok} SKIP={skip} ERR={err}")
