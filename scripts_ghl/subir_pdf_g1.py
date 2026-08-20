"""Sube el brochure G1-SketchUp-Brochure.pdf al media store (carpeta FICHAS WHATSAPP)
e imprime la tupla SKETCHUP_PDF lista para pegar en build_sp05_v2.py.

Idempotente: si ya existe un archivo con ese nombre en la carpeta, no re-sube.
Uso: python3 scripts_ghl/subir_pdf_g1.py
"""
import os, sys, json, pathlib, requests

ROOT = pathlib.Path("/home/user/grupo-galk")
for l in (ROOT / ".env").read_text().splitlines():
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip())

H = {"Authorization": f"Bearer {os.environ['GHL_API_KEY']}", "Version": "2021-07-28",
     "Accept": "application/json"}
LOC = os.environ["GHL_LOCATION_ID"]
B = "https://services.leadconnectorhq.com"
CARPETA = "6a4b0f6a1209780f804ad8b5"   # FICHAS WHATSAPP
PDF = ROOT / "contenido-fichas" / "assets" / "G1-SketchUp-Brochure.pdf"
NOMBRE = "G1-SketchUp-Brochure.pdf"

def listar():
    r = requests.get(f"{B}/medias/files", headers=H,
                     params={"altId": LOC, "altType": "location", "sortBy": "createdAt",
                             "sortOrder": "desc", "type": "file", "parentId": CARPETA, "limit": 100})
    r.raise_for_status()
    return r.json().get("files", [])

ya = [f for f in listar() if f.get("name") == NOMBRE]
if ya:
    f = ya[0]
else:
    with open(PDF, "rb") as fh:
        r = requests.post(f"{B}/medias/upload-file", headers=H,
                          files={"file": (NOMBRE, fh, "application/pdf")},
                          data={"hosted": "false", "name": NOMBRE, "parentId": CARPETA,
                                "altId": LOC, "altType": "location"})
    print("upload:", r.status_code, str(r.json())[:200])
    r.raise_for_status()
    ya2 = [f for f in listar() if f.get("name") == NOMBRE]
    if not ya2:
        print("ABORT: subido pero no aparece en la carpeta — revisar a mano"); sys.exit(1)
    f = ya2[0]

url = f.get("url", "")
mid = url.rsplit("/", 1)[-1].rsplit(".", 1)[0]
ext = url.rsplit(".", 1)[-1]
print(f"\nmedia id: {mid} · ext: {ext} · size: {f.get('size')}")
print("\nPega esto en build_sp05_v2.py:")
print(f'SKETCHUP_PDF = ("{mid}", "{NOMBRE}", {f.get("size")}, "{ext}")')
