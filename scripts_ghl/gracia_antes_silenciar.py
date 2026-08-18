"""SP06 silenciaba al especialista antes de que hablara. Se le da un periodo de gracia.

QUÉ PASÓ (18-ago, prueba de AutoCAD en BOT-02)
----------------------------------------------
El lead escribió "hola, quiero info del curso de autocad" y con ESE PRIMER MENSAJE quedó
calificado, asignado y con el bot mudo. BOT-02 nunca llegó a responder.

La cadena: BOT-00 capturó `Curso de interés` en el saludo → WF-MOD dedujo Modalidad=Online →
WF-SEDE puso Sede=No aplica → los 3 campos completos → SP06 calificó y silenció. Todo en el
primer turno, antes de la presentación del curso.

En talleres esto nunca se vio porque la Sede obliga al especialista a preguntar: la
calificación llegaba naturalmente al FINAL de la conversación. En los cursos online el curso
solo basta —Modalidad y Sede se derivan— así que la calificación puede llegar al PRINCIPIO.

EL ARREGLO (dos partes, esta es la automática)
----------------------------------------------
1. (UI, Oliver) BOT-00 deja de capturar `Curso de interés`: solo captura Familia. Así el
   curso lo captura el especialista en su primer turno, junto con la presentación.
2. (este script) Un WAIT de 3 minutos antes del tag `bot-silenciado` y del silenciado en la
   rama buena de SP06. Es el periodo de gracia para que el especialista termine: presentar,
   dar el precio y contestar un último "¿cuánto cuesta?".

En talleres no cambia nada perceptible: cuando SP06 corre, el bot ya se despidió; si el lead
dice "gracias" en esos 3 minutos, el bot contesta con cortesía y luego se calla. Y si el
asesor entra antes, el toggle de sleep-on-manual lo silencia igual.

La notificación al asesor NO se retrasa: sale antes del wait, como siempre.
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, nid

WID = "84811c16-30d8-4c08-a05d-0c12fa46567d"
MINUTOS = 3


def main():
    d = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    tpl = (d.get("workflowData") or {}).get("templates") or []
    if not tpl:
        sys.exit("ABORT: no pude leer los nodos de SP06")
    byid = {n["id"]: n for n in tpl}
    print(f"SP06 v{d.get('version')} · {d.get('status')} · {len(tpl)} nodos")

    # la rama buena se identifica por el tag bot-silenciado
    tag = next((n for n in tpl if n.get("type") == "add_contact_tag"
                and "bot-silenciado" in ((n.get("attributes") or {}).get("tags") or [])), None)
    if not tag:
        sys.exit("ABORT: no encontré el nodo del tag 'bot-silenciado'")
    previo = next((n for n in tpl if n.get("next") == tag["id"]), None)
    if not previo:
        sys.exit("ABORT: nadie apunta al tag. Revisar a mano.")
    if previo.get("type") == "wait":
        print(f"Ya hay un wait antes del silenciado ({previo['id'][:8]}). "
              "Nada que hacer (idempotencia §3).")
        return

    w = nid()
    nodo = wf_lib.n_wait(w, MINUTOS, "minutes", nxt=tag["id"], parent=tag.get("parentKey"))
    nodo["name"] = "Gracia: el bot termina de hablar"
    tpl.append(nodo)
    previo["next"] = w
    print(f"  + wait {MINUTOS} min entre {previo.get('type')} ({previo['id'][:8]}) "
          f"y el tag bot-silenciado")

    r = C.request("PUT", f"/workflow/{LOC}/{WID}",
                  {"name": d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"), "status": d.get("status"),
                   "allowMultiple": d.get("allowMultiple"),
                   "workflowData": {"templates": tpl}})
    print("PUT:", "OK" if r and not r.get("_error") else r)

    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    vb = {n["id"]: n for n in vt}
    vt_tag = next(n for n in vt if n.get("type") == "add_contact_tag"
                  and "bot-silenciado" in ((n.get("attributes") or {}).get("tags") or []))
    cur = next(n for n in vt if n.get("next") and False) if False else None
    # recorrer desde la notificación de la rama buena
    notif = next(n for n in vt if n.get("type") == "internal_notification"
                 and (n.get("attributes") or {}).get("notification", {}).get("userType") == "assign")
    cadena, cur, i = [], notif, 0
    while cur and i < 6:
        a = cur.get("attributes") or {}
        et = cur.get("type")
        if et == "wait":
            et += f" {a.get('startAfter')}"
        cadena.append(et)
        nx = cur.get("next")
        cur = vb.get(nx) if isinstance(nx, str) and nx else None
        i += 1
    print(f"VERIFY: v{v.get('version')} · {v.get('status')} · {len(vt)} nodos")
    print("  rama buena desde la notificación: " + "  →  ".join(cadena))


if __name__ == "__main__":
    main()
