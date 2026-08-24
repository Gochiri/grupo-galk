# -*- coding: utf-8 -*-
"""SP04.x — Respaldo determinístico de la captura de curso (sin IA).

POR QUÉ
-------
24-ago: la ejecución de las acciones Contact Info de Conversation AI resultó
INTERMITENTE del lado de GHL (2 de 6 turnos completos en un día de pruebas; a veces
corre solo la primera acción, a veces ninguna). Nuestra config demostró estar bien:
cuando las acciones corren, escriben perfecto. Pero SP05 depende al 100% de que
`Curso de interés` se llene, y no controlamos cuándo GHL decide fallar.

QUÉ HACE
--------
6 mini-workflows (uno por curso con ficha), todos con la misma forma:

    trigger `customer_reply` (message.body contiene alguna palabra clave del curso,
                              contacto con etiqueta `pruebas demo`)
    → Wait (90 s; 60 s el de Supervisión)        ← le da el primer turno al bot
    → if/else:  "Ya hay curso"      (Curso de interés has_value)   → salir
                "Ficha ya enviada"  (tag ficha-enviada)            → salir
                None                                               → escribir el
                                                     nombre oficial en Curso de interés

Con eso el trigger `contact_changed(Curso)` de SP05 dispara la secuencia como siempre.
El bot queda igual: esto solo atrapa los turnos en que GHL no ejecuta sus capturas.

DETALLES QUE IMPORTAN
---------------------
- El Wait ANTES de la guarda serializa contra el bot: si la captura sí corrió, la
  guarda ve el campo lleno y sale — sin carreras ni dobles envíos.
- Supervisión espera 60 s y los demás 90: "supervisión de melamina" contiene
  "melamina" y dispara ambos triggers; el de Supervisión escribe primero y la guarda
  del de Melamina lo respeta. (Mismo problema que resuelve la rama atrapadora de SP05.)
- Palabras clave: heredadas de los CAMPOS de Francisco (en producción desde julio),
  menos los códigos cortos ambiguos (g1..g8, que son subcadena de g13/g16/g24/g25/g28).
- Valores escritos = nombres oficiales v4.2, que matchean las conds `contains` del
  árbol de SP05.
- Todo queda en DRAFT con triggers inactivos. Publicar = PUT del trigger con
  active:true, tras revisión humana (política §3).
- Formas clonadas de moldes vivos: trigger de "CAMPOS 01 - Melamina" (message-body
  string-contains-any-of) + LS01 (has-tag) + guarda de SP06 (has_value, sin
  conditionValue) + esqueleto arbol() de WF-MOD.

Uso:  build_sp04_respaldo.py [--aplicar]     (sin flag = dry-run)
"""
import sys, pathlib, argparse, time, os

sys.path.insert(0, str(pathlib.Path("/home/user/grupo-galk/scripts_ghl")))
import wf_lib
from wf_lib import C, LOC, nid, n_update, n_wait, arbol, cond_tag, NESTED, ALLOWIS

CARPETA = "3dc6be37-5389-4385-9806-36722ba042ef"   # GALK 2.0 · 04 Sales Pipeline
CURSO_KEY = "contact.curso_de_inters"
TAG_MARCADOR = "ficha-enviada"
TAG_PRUEBAS = "pruebas demo"                        # quitar en go-live, como en LS01

# (nombre workflow, keywords message.body, valor oficial a escribir, espera en seg)
CURSOS = [
    ("SP04.0 | Respaldo curso — Supervisión",
     ["supervision", "supervisión", "gestion de proyectos", "gestión de proyectos"],
     "Gestión y Supervisión de Melamina", 60),
    ("SP04.1 | Respaldo curso — Melamina",
     ["melamina", "melamine", "g13", "g16"], "Melamina", 90),
    ("SP04.2 | Respaldo curso — Drywall",
     ["drywall", "g24", "g28"], "Drywall", 90),
    ("SP04.3 | Respaldo curso — Electricidad",
     ["g25", "electricidad", "domotica", "domótica", "electricista"],
     "Electricidad y Domótica", 90),
    ("SP04.4 | Respaldo curso — SketchUp",
     ["sketchup", "sketch up", "skp"], "SketchUp", 90),
    ("SP04.5 | Respaldo curso — Revit",
     ["revit", "bim", "lumion"], "Revit BIM", 90),
]


def cond_curso_tiene_valor():
    """Molde: guarda de SP06 (has_value NO lleva conditionValue)."""
    return {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(CURSO_KEY),
            "conditionOperator": "has_value", "__conditionId": nid(), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": NESTED, "allowIsOperatorTypes": ALLOWIS}


def plantillas(valor, espera):
    u = nid()
    upd = n_update(u, [(CURSO_KEY, valor)], name=f"Curso = {valor}")
    t = arbol([
        ("Ya hay curso (el bot sí capturó)", [cond_curso_tiene_valor()], []),
        ("Ficha ya enviada", [cond_tag(TAG_MARCADOR)], []),
    ], none_next=[upd])
    wait_id = nid()
    w = n_wait(wait_id, espera, unidad="seconds", nxt=t[0]["id"])
    return [w] + t, wait_id


def trigger_body(wid, nombre_corto, keywords, wait_id):
    return {"status": "draft", "workflowId": wid, "schedule_config": {},
            "conditions": [
                {"operator": "string-contains-any-of", "field": "message.body",
                 "value": keywords, "title": "Message body", "type": "string",
                 "id": "message-body"},                       # molde: CAMPOS 01
                {"operator": "index-of-true", "field": "contact.tags",
                 "value": TAG_PRUEBAS, "title": "Tiene etiqueta", "type": "select",
                 "id": "has-tag"},                            # molde: LS01
            ],
            "type": "customer_reply", "masterType": "highlevel",
            "name": f"Mencionó {nombre_corto}", "allowMultiple": "yes",
            "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
            "active": False,           # nunca True aquí: publicaría el workflow (§3)
            "triggersChanged": True, "location_id": LOC, "targetActionId": wait_id,
            "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()

    # workaround proxy: id_token directo si el shell lo pasó (el refresh por urllib
    # a veces recibe 403 del proxy; con curl sí sale — ver sesión 24-ago)
    tok = os.environ.get("GHL_FB_ID_TOKEN", "").strip()
    if tok:
        C.token_mgr._token = tok
        C.token_mgr._token_time = time.time()

    existentes = {w.get("name"): w["id"] for w in (C.request("GET", f"/workflow/{LOC}") or [])}

    for nombre, keywords, valor, espera in CURSOS:
        corto = nombre.split("—")[-1].strip()
        if nombre in existentes and not args.aplicar:
            print(f"YA EXISTE  {nombre}")
            continue
        if not args.aplicar:
            print(f"DRY-RUN    {nombre}: keywords={keywords} → Curso='{valor}' (wait {espera}s)")
            continue

        wid = existentes.get(nombre)
        if not wid:                                    # idempotencia
            wf = C.request("POST", f"/workflow/{LOC}", {"name": nombre, "parentId": CARPETA})
            wid = wf.get("id") if isinstance(wf, dict) else None
            if not wid:
                print(f"ERROR creando {nombre}: {wf}"); continue

        temps, wait_id = plantillas(valor, espera)
        d = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
        r = C.request("PUT", f"/workflow/{LOC}/{wid}",
                      {"name": nombre, "version": d.get("version", 1), "parentId": CARPETA,
                       "status": "draft", "allowMultiple": True,
                       "workflowData": {"templates": temps}})
        if isinstance(r, dict) and r.get("_error"):
            print(f"ERROR PUT {nombre}: {r}"); continue

        trs = C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}") or []
        if isinstance(trs, dict):
            trs = trs.get("triggers", [])
        if not trs:
            tr = C.request("POST", f"/workflow/{LOC}/trigger",
                           trigger_body(wid, corto, keywords, wait_id))
            ok = isinstance(tr, dict) and not tr.get("_error")
        else:   # nodos regenerados: reapuntar el targetActionId del trigger existente
            t = trs[0]
            t.update({"targetActionId": wait_id, "triggersChanged": True})
            tr = C.request("PUT", f"/workflow/{LOC}/trigger/{t['id']}", t)
            ok = isinstance(tr, dict) and not tr.get("_error")

        v = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
        n = len((v.get("workflowData") or {}).get("templates") or [])
        print(f"OK  {nombre}  id={wid}  status={v.get('status')} "
              f"allowMultiple={v.get('allowMultiple')} nodos={n} trigger={'OK' if ok else 'ERROR'}")


if __name__ == "__main__":
    main()
