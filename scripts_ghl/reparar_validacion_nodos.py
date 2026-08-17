"""Nodos que GHL ya no acepta al guardar — y que además no funcionaban.

CÓMO APARECIÓ
-------------
Intentando quitar el silenciado del ramal de fallo de SP06, el PUT empezó a rebotar en
cadena con `Action validation failed`. Cada error tapaba al siguiente, así que fueron
saliendo de a uno:

    create_opportunity     -> "Monetary Value is invalid"
    internal_notification  -> 'User Type has an invalid value "assigned_user"'

Lo importante: **no es solo un problema de guardado**. Un `userType` que GHL considera
inválido no avisa a nadie. Nuestras notificaciones al asesor probablemente nunca llegaron —
lo que sí llegaba era el `asesor-notificado` de WF3 de Francisco, que es otro workflow.

LOS FORMATOS BUENOS
-------------------
Sacados de WF3 y ALERTA de Francisco, que están hechos en la UI:

    al dueño del contacto  -> userType="assign", assignedOwners=["contact_owner"]
    a un usuario concreto  -> userType="user",   selectedUser="<userId>"

`assigned_user` y `specific_user`, que es lo que usábamos, no existen.

Y `create_opportunity` necesita `monetary_value`. Se pone nuestro campo `Precio cotizado`,
el mismo que ya usa SP11, no el `PRECIO_CURSO` heredado (política §3). En calificación viene
vacío y no molesta: el valor lo escribe el asesor y las etapas siguientes lo arrastran.

CÓMO CORRE
----------
En seco por defecto; `--aplicar` para escribir. Si un PUT sigue rebotando, imprime el error
tal cual: es la forma de descubrir la siguiente validación sin adivinar.
"""
import sys, json, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
from wf_lib import C, LOC

SOLO_MIRAR = "--aplicar" not in sys.argv
NUESTROS = ("SP0", "SP1", "AP0", "PS0", "LS0", "WF-")
VALOR = "{{contact.precio_cotizado}}"


def arreglar(tpl):
    """Devuelve la lista de cambios hechos in-place sobre los nodos."""
    cambios = []
    for n in tpl:
        a = n.get("attributes") or {}

        if n.get("type") == "create_opportunity" and not a.get("monetary_value"):
            a["monetary_value"] = VALOR
            cambios.append(f"monetary_value en {n['id'][:8]}")

        if n.get("type") == "internal_notification":
            no = a.get("notification") or {}
            ut = no.get("userType")
            if ut in ("assign", "user"):
                continue
            if no.get("selectedUser"):                 # iba a alguien concreto
                no["userType"] = "user"
                no.pop("assignedOwners", None)
                cambios.append(f"userType {ut!r}→'user' en {n['id'][:8]}")
            else:                                      # iba al dueño del contacto
                no["userType"] = "assign"
                no["assignedOwners"] = ["contact_owner"]
                no.pop("selectedUser", None)
                cambios.append(f"userType {ut!r}→'assign' en {n['id'][:8]}")
    return cambios


def main():
    total, fallos = 0, []
    for w in C.request("GET", f"/workflow/{LOC}") or []:
        if not w["name"].startswith(NUESTROS):
            continue
        d = C.request("GET", f"/workflow/{LOC}/{w['id']}") or {}
        tpl = (d.get("workflowData") or {}).get("templates") or []
        if not tpl:
            continue
        cambios = arreglar(tpl)
        if not cambios:
            continue
        total += 1
        print(f"  {w['name'][:44]:46} {' · '.join(cambios)}")
        if SOLO_MIRAR:
            continue
        r = C.request("PUT", f"/workflow/{LOC}/{w['id']}",
                      {"name": d.get("name"), "version": d.get("version"),
                       "parentId": d.get("parentId"), "status": d.get("status"),
                       "allowMultiple": d.get("allowMultiple"),
                       "workflowData": {"templates": tpl}})
        if r and not (isinstance(r, dict) and r.get("_error")):
            print("      PUT: OK")
        else:
            msg = (r or {}).get("message", str(r))
            fallos.append((w["name"], msg))
            print(f"      PUT REBOTÓ: {msg[:220]}")

    print(f"\n{total} workflow(s) con nodos que GHL no acepta."
          if total else "\nTodos los nodos pasan la validación.")
    if fallos:
        print("\nSiguen rebotando (validación nueva por descubrir):")
        for n, m in fallos:
            print(f"  · {n}\n      {m[:300]}")
    elif SOLO_MIRAR and total:
        print("(simulación; --aplicar para escribir)")


if __name__ == "__main__":
    main()
