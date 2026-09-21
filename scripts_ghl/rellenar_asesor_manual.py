"""Rellena `Asesor asignado (nuevo)` y `Fecha de asignación` en los leads que el
cliente asignó A MANO, para que dejen de ser invisibles en los reportes.

POR QUÉ HACE FALTA (hallazgo del 21-sep)
----------------------------------------
El 19-sep el lado de Francisco vació el backlog de huérfanos asignando ~210 leads
a mano desde la UI (136 en una sola hora; reparto desigual, nada que ver con un
round robin; los dos workflows ajenos que asignan están en draft). La asignación
manual pone el PROPIETARIO NATIVO del contacto, pero no toca nuestros campos: se
quedaron con `Asesor asignado (nuevo)` y `Fecha de asignación` vacíos. Cualquier
reporte que lea esos campos —los que llenan SP06 y SP07— los subcuenta.

QUÉ ESCRIBE
-----------
Exactamente el mismo formato que ya escriben SP06/SP07, verificado contra
contactos vivos:
    Asesor asignado (nuevo) = nombre del propietario, tal cual ("Pablo Chavez")
    Fecha de asignación     = fecha a medianoche UTC ("2026-09-19T00:00:00.000Z")

La fecha sale de `dateUpdated` del contacto, que para estos es el momento en que
los tocaron a mano. Es una APROXIMACIÓN: si a un contacto lo actualizaron después
por otra razón, la fecha será esa. Se captura antes de escribir (escribir mueve
`dateUpdated`), y el resumen dice cuántos caen fuera del 19-sep.

SEGURIDAD
---------
· Idempotente (§3): si el campo ya tiene valor, salta. Correr dos veces no duplica.
· Solo toca contactos con propietario nativo puesto — nunca asigna a nadie.
· Ventana acotada a la cohorte medida (8-sep → 15-sep 14:21 UTC, la anterior al
  go-live de SP07). Informa de lo que hay fuera de la ventana, pero NO lo toca.
· Sin --aplicar solo simula. Con --aplicar N limita a los primeros N (para probar
  en uno y verificar que el PUT no se lleve por delante otros campos custom).
"""
import os, sys, time, pathlib, collections

ROOT = pathlib.Path("/home/user/grupo-galk")
for l in (ROOT / ".env").read_text().splitlines():
    if "=" in l and not l.startswith("#"):
        k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api

LOC      = os.environ["GHL_LOCATION_ID"]
DESDE    = "2026-09-08T00:00:00Z"
HASTA    = "2026-09-15T14:21:00Z"        # go-live de SP07
SIN_RASTRO = ("rescate-15min", "bot-silenciado")   # si los tiene, lo asignó un workflow


def campos():
    cf = {f["fieldKey"]: f for f in api.get(f"/locations/{LOC}/customFields").get("customFields", [])}
    return cf["contact.asesor_asignado_nuevo"]["id"], cf["contact.fecha_de_asignacin"]["id"]


def buscar(desde, hasta=None):
    val = {"gte": desde} | ({"lte": hasta} if hasta else {})
    out, page = [], 1
    while page <= 30:
        r = api.post("/contacts/search", {
            "locationId": LOC, "pageLimit": 100, "page": page,
            "filters": [{"field": "dateAdded", "operator": "range", "value": val}],
            "sort": [{"field": "dateAdded", "direction": "desc"}]})
        c = r.get("contacts", []); out += c
        if len(c) < 100:
            break
        page += 1
    return out


def valor(c, fid):
    for f in (c.get("customFields") or []):
        if f.get("id") == fid:
            return f.get("value")


def main():
    aplicar = "--aplicar" in sys.argv
    limite = None
    if aplicar:
        i = sys.argv.index("--aplicar")
        if i + 1 < len(sys.argv) and sys.argv[i + 1].isdigit():
            limite = int(sys.argv[i + 1])

    ASE, FAS = campos()
    users = {u["id"]: u for u in api.get(f"/users/?locationId={LOC}").get("users", [])}

    objetivo, sin_usuario = [], []
    for c in buscar(DESDE, HASTA):
        tags = [t.lower() for t in (c.get("tags") or [])]
        if not c.get("assignedTo") or valor(c, ASE) or any(t in tags for t in SIN_RASTRO):
            continue
        u = users.get(c["assignedTo"])
        (objetivo if u and u.get("name") else sin_usuario).append(c)

    # informativo: mismo síntoma fuera de la ventana acordada — NO se toca
    fuera = sum(1 for c in buscar("2026-08-01T00:00:00Z", DESDE)
                if c.get("assignedTo") and not valor(c, ASE))

    print(f"ventana {DESDE[:10]} → {HASTA[:10]} · a rellenar: {len(objetivo)}")
    if sin_usuario:
        print(f"  (saltados: {len(sin_usuario)} con propietario que no resuelve a un usuario)")
    print(f"  reparto: {dict(collections.Counter(users[c['assignedTo']]['name'] for c in objetivo))}")
    fechas = collections.Counter(str(c.get("dateUpdated"))[:10] for c in objetivo)
    print(f"  fechas que se escribirán: {dict(sorted(fechas.items()))}")
    print(f"  FUERA de la ventana, mismo síntoma (NO se tocan): {fuera} contactos anteriores al 8-sep")

    if not aplicar:
        print("\n(simulación; --aplicar para escribir, --aplicar N para limitar a N)")
        for c in objetivo[:3]:
            print(f"   ej: {c['id']} → {users[c['assignedTo']]['name']!r} · "
                  f"{str(c.get('dateUpdated'))[:10]}")
        return

    lote = objetivo[:limite] if limite else objetivo
    print(f"\nescribiendo {len(lote)}…")
    ok = err = 0
    for n, c in enumerate(lote, 1):
        fecha = str(c.get("dateUpdated"))[:10] + "T00:00:00.000Z"
        r = api.put(f"/contacts/{c['id']}", {"customFields": [
            {"id": ASE, "value": users[c["assignedTo"]]["name"]},
            {"id": FAS, "value": fecha}]})
        if isinstance(r, dict) and (r.get("contact") or r.get("succeded") or r.get("id")):
            ok += 1
        else:
            err += 1
            print(f"   ERROR {c['id']}: {str(r)[:120]}")
        if n % 25 == 0:
            print(f"   … {n}/{len(lote)}")
        time.sleep(0.25)                      # cortesía con el rate limit
    print(f"\nescritos: {ok} · errores: {err}")


if __name__ == "__main__":
    main()
