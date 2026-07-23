"""SETUP-02: create the NEW 'Ventas GALK' pipeline (9 stages) via GHL public API.
Additive only — does NOT touch the inherited '[GALK] Cursos y Capacitaciones' pipeline.
Loads .env internally so the command is a clean venv-python invocation."""
import os, sys, json, pathlib, requests

ROOT = pathlib.Path("/home/user/grupo-galk")
# --- load .env ---
for line in (ROOT / ".env").read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    os.environ.setdefault(k.strip(), v.strip())

sys.path.insert(0, str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api

LOC = os.environ["GHL_LOCATION_ID"]
STAGES = ["Nuevo Lead","En conversación (bot)","Ficha enviada","Calificado",
          "Asignado a asesor","Datos de pago enviados","Pago en validación",
          "Matriculado","Perdido"]

# Guard: confirm the new pipeline doesn't already exist (idempotency / no dupes)
existing = api.get("/opportunities/pipelines", params={"locationId": LOC}).get("pipelines", [])
names = [p["name"] for p in existing]
print("Existing pipelines:", names)
if "Ventas GALK" in names:
    print("ALREADY EXISTS — no action taken.")
    sys.exit(0)

body = {"locationId": LOC, "name": "Ventas GALK",
        "stages": [{"name": n, "position": i} for i, n in enumerate(STAGES)]}
url = "https://services.leadconnectorhq.com/opportunities/pipelines"
h = api._headers(path="/opportunities/pipelines")
r = requests.post(url, headers=h, json=body, timeout=30)
print("POST status:", r.status_code)
print("response:", r.text[:600])
