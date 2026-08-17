"""El ramal de fallo de SP06 silenciaba el bot. No debía.

QUÉ ESTABA MAL
--------------
Los dos ramales del if/else de "Asesor asignado" terminaban silenciando el bot:

    rama "Asesor asignado"  -> oportunidad -> notificación -> tag bot-silenciado   -> SILENCIAR
    rama None (falló)       ->               notificación -> tag asignacion-fallida -> SILENCIAR  ← mal

El sentido del ramal de fallo es el contrario: si el round robin no asignó a nadie, **el bot
tiene que seguir vivo** para que la persona no quede hablando con una pared mientras un humano
recoge el lead a mano. Con el bot mudo y sin dueño, el lead se pierde en silencio — que es
exactamente lo que ese ramal se construyó para evitar (ver docstring de `rebuild_sp06.py`).

El tag `asignacion-fallida` y el aviso a Lucía se quedan: son la señal de que hay que asignar
a mano.

PENDIENTE EN EL OTRO RAMAL
--------------------------
El silenciado del ramal bueno usa `assignedEmployeeId: "keep-same"`, que es la opción "Keep
Same" del desplegable. En la prueba del 17-ago el bot siguió contestando después de asignar,
así que la sospecha es que `keep-same` resuelve al bot que el contacto tiene asignado a nivel
de contacto, y que el Transfer Bot de BOT-00 → BOT-01 no mueve esa asignación: silenciaría a
BOT-00, que ya estaba callado, mientras BOT-01 sigue hablando.

Para dejarlo explícito hacen falta los IDs de BOT-01/02/03, y no hay endpoint que los liste
(probados públicos e internos, todos 404). Se leen del URL al abrir cada bot en AI Agents.
Con esos tres IDs esto pasa a ser un if/else sobre `Familia de interés` con un nodo por
familia, misma forma que WF-MOD.
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
from wf_lib import C, LOC

WID = "84811c16-30d8-4c08-a05d-0c12fa46567d"
TAG_FALLO = "asignacion-fallida"


def main():
    d = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    tpl = (d.get("workflowData") or {}).get("templates") or []
    if not tpl:
        sys.exit("ABORT: no pude leer los nodos de SP06")
    byid = {n["id"]: n for n in tpl}
    print(f"SP06 {d.get('status')} v{d.get('version')} · {len(tpl)} nodos")

    # el tag de fallo marca el ramal malo; se busca por ahí y no por posición
    tag_fallo = next((n for n in tpl if n.get("type") == "add_contact_tag"
                      and TAG_FALLO in ((n.get("attributes") or {}).get("tags") or [])), None)
    if not tag_fallo:
        sys.exit(f"ABORT: no encontré el nodo del tag '{TAG_FALLO}'. Revisar a mano.")

    sig = byid.get(tag_fallo.get("next")) if isinstance(tag_fallo.get("next"), str) else None
    if not sig or sig.get("type") != "update_conversation_ai_status":
        print("El ramal de fallo ya no silencia. Nada que hacer (idempotencia §3).")
        return

    print(f"  quitando {sig['id'][:8]} ({sig['type']}) del ramal de fallo")
    tpl = [n for n in tpl if n["id"] != sig["id"]]
    tag_fallo.pop("next", None)

    # GHL empezó a validar `monetary_value` en create_opportunity y sin esa clave rechaza el
    # PUT entero con "Monetary Value is invalid", aunque los nodos funcionen en ejecución.
    # Se usa nuestro campo `Precio cotizado`, el mismo que ya usa SP11, no el PRECIO_CURSO
    # heredado de Francisco (política §3). En calificación viene vacío y no pasa nada: el
    # valor lo escribe el asesor y las etapas siguientes lo arrastran.
    for n in tpl:
        if n.get("type") == "create_opportunity" and "monetary_value" not in (n.get("attributes") or {}):
            n["attributes"]["monetary_value"] = "{{contact.precio_cotizado}}"
            print(f"  + monetary_value en {n['id'][:8]} ({n.get('name')})")

    r = C.request("PUT", f"/workflow/{LOC}/{WID}",
                  {"name": d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"), "status": d.get("status"),
                   "allowMultiple": d.get("allowMultiple"),
                   "workflowData": {"templates": tpl}})
    print("PUT:", "OK" if r and not r.get("_error") else r)

    # verificación: recorrer los dos ramales
    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    vbyid = {n["id"]: n for n in vt}
    h = [n for n in vt if n.get("nodeType") == "condition-node"][1]
    print(f"\nVERIFY: {v.get('status')} · reingreso={v.get('allowMultiple')} · {len(vt)} nodos")
    for hijo in [n for n in vt if n.get("parentKey") == h["id"]
                 and str(n.get("nodeType", "")).startswith("branch")]:
        cadena, cur = [], vbyid.get(hijo.get("next"))
        while cur:
            cadena.append(cur.get("type"))
            cur = vbyid.get(cur.get("next")) if isinstance(cur.get("next"), str) else None
        silencia = "update_conversation_ai_status" in cadena
        print(f"  rama {str(hijo.get('name')):18} silencia={silencia}  {' → '.join(cadena)}")


if __name__ == "__main__":
    main()
