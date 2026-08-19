"""SP05: convierte los 24 nodos whatsapp_v2 en nodos SMS *in situ* para poder probar
el envío de ficha por el plugin de WhatsApp-por-SMS (los WABA templates aún no existen).

- Mismo ID de nodo -> la cadena (rama -> envío -> quitar tag -> ficha-enviada) y el
  targetActionId del trigger NO se tocan.
- Los nodos WhatsApp originales se respaldan en sp05_wa_original.json (en el repo);
  `--revertir` los restaura tal cual en la pasada final de contenido.
- Excepción temporal a la regla de no hardcodear URLs de ficha: el campo attachments
  de SMS no tiene comprobado que resuelva {{custom_values...}}, y esto es un andamio
  de prueba que se elimina al restaurar. Los custom values siguen siendo la fuente
  de verdad para los nodos WhatsApp definitivos (ya están rellenos).

Uso: sp05_sms_prueba.py [--aplicar | --revertir]   (sin flag = dry-run)
"""
import os, sys, json, pathlib
ROOT = pathlib.Path("/home/user/grupo-galk")
for l in (ROOT / ".env").read_text().splitlines():
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, str(ROOT))
from cli_anything.gohighlevel.utils.ghl_internal_client import TokenManager, InternalGHLClient

LOC = os.environ["GHL_LOCATION_ID"]
WID = "ae78625c-8f91-4af1-a7b0-3be0b2e4a667"  # SP05
BACKUP = ROOT / "scripts_ghl" / "sp05_wa_original.json"
CDN = "https://assets.cdn.filesafe.space/YN2uRSDcNeBdTWm3UPCU/media/%s.jpeg"

# imagen elegida por curso (la -1 de cada carpeta de FICHAS WHATSAPP)
IMG = {
    "ficha_melamina_desde_cero": CDN % "6a4b0fed70834e617c689aa1",   # Melamina-1
    "ficha_melamina_avanzado":   CDN % "6a4b0ffb6f5641e105b96f55",   # Melamina-1 Avanzado
    "ficha_drywall_desde_cero":  CDN % "6a4da7e82467f0ff08fed87d",   # Drywall-1
    "ficha_drywall_avanzado":    CDN % "6a4dc1fa50dd270fd6aadf05",   # Drywall-1 Avanzado
    "ficha_electricidad":        CDN % "6a51b6b10e67afc013822d3f",   # Electricidad-1
}

def imagen_para(cvkey):
    for pref, url in IMG.items():
        if cvkey.startswith(pref):
            return url
    return None  # software/gestión: Francisco aún no sube esas imágenes

aplicar = "--aplicar" in sys.argv
revertir = "--revertir" in sys.argv
c = InternalGHLClient(TokenManager(), LOC)
det = c.request("GET", f"/workflow/{LOC}/{WID}")
tpl = det["workflowData"]["templates"]

if revertir:
    orig = {n["id"]: n for n in json.loads(BACKUP.read_text())}
    n_rest = 0
    for i, n in enumerate(tpl):
        if n["id"] in orig and n["type"] == "sms":
            tpl[i] = orig[n["id"]]; n_rest += 1
    print(f"restaurados {n_rest} nodos WhatsApp desde el backup")
else:
    wa = [n for n in tpl if n["type"] == "whatsapp_v2"]
    print(f"whatsapp_v2: {len(wa)} · sms ya convertidos: {sum(n['type']=='sms' for n in tpl)}")
    if wa and not BACKUP.exists():
        BACKUP.write_text(json.dumps(wa, ensure_ascii=False, indent=1))
        print(f"backup de {len(wa)} nodos WhatsApp -> {BACKUP.name}")
    # mapa id -> nodo WhatsApp original (para re-correr sobre nodos ya convertidos)
    orig = {n["id"]: n for n in json.loads(BACKUP.read_text())} if BACKUP.exists() else {}
    con_img = sin_img = 0
    for n in tpl:
        if n["type"] == "whatsapp_v2":
            base = n
        elif n["type"] == "sms" and n["id"] in orig:
            base = orig[n["id"]]
        else:
            continue
        cvkey = base["attributes"].get("media_url", "").replace("{{custom_values.", "").replace("}}", "")
        url = imagen_para(cvkey)
        con_img += bool(url); sin_img += not url
        msg = base["attributes"].get("message") or "¡Aquí tienes la información de tu curso! 👇"
        # el gateway WaAutoReply convierte la línea "image - <url>" en imagen real
        # (así lo hacía Francisco por este mismo plugin); attachments ejecuta [null].
        if url:
            msg = f"{msg}\n\nimage - {url}"
        n["type"] = "sms"
        n["name"] = n["name"].replace("Ficha:", "Ficha SMS:")
        n["attributes"] = {"template_id": "", "body": msg, "attachments": []}
        n.pop("workflowsActionType", None)  # clave de whatsapp_v2, no del nodo sms de la UI
    print(f"a convertir: {con_img} con imagen · {sin_img} sin imagen (software/gestión, pendiente Francisco)")

if not (aplicar or revertir):
    print("(dry-run: nada escrito — usa --aplicar)")
    sys.exit(0)

# ⚠️ allowMultiple SIEMPRE en el body: el PUT resetea a False cualquier campo
# raíz omitido (aprendido el 19-ago: este mismo script dejó SP05 sin reingreso).
r = c.request("PUT", f"/workflow/{LOC}/{WID}",
              {"name": det.get("name"), "version": det.get("version"),
               "parentId": det.get("parentId"), "status": det.get("status"),
               "allowMultiple": True,  # SP05 requiere reingreso, ver permitir_reingreso.py
               "workflowData": {"templates": tpl}})
print("PUT:", "OK" if r and not (isinstance(r, dict) and r.get("_error")) else r)

# verificación: releer y comprobar triggers
det2 = c.request("GET", f"/workflow/{LOC}/{WID}")
tipos = {}
for n in det2["workflowData"]["templates"]:
    tipos[n["type"]] = tipos.get(n["type"], 0) + 1
print("nodos tras el PUT:", tipos)
trs = c.request("GET", f"/workflow/{LOC}/trigger?workflowId={WID}") or []
if isinstance(trs, dict): trs = trs.get("triggers", trs.get("data", []))
ids = {n["id"] for n in det2["workflowData"]["templates"]}
for t in trs:
    ta = t.get("targetActionId")
    ok = "OK" if (ta is None or ta in ids) else "ROTO ->" + str(ta)
    print(f"trigger {t.get('name')!r}: active={t.get('active')} targetActionId={ta} {ok}")
