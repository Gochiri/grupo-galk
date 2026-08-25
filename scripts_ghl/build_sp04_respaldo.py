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
    → Wait (30 s; 10 s el de Supervisión)        ← escalón anti-colisión
    → if/else:  "Ya tiene ESTE curso" (Curso CONTIENE el propio)   → salir
                None (vacío u OTRO curso — CONMUTADOR, 25-ago):
                    quitar tag ficha-enviada → limpiar modalidad/sede/nivel →
                    escribir el curso nuevo → SP05 envía la ficha nueva

Con eso el trigger `contact_changed(Curso)` de SP05 dispara la secuencia como siempre.
El bot queda igual: esto solo atrapa los turnos en que GHL no ejecuta sus capturas.

DETALLES QUE IMPORTAN
---------------------
- El Wait ANTES de la guarda serializa contra el bot: si la captura sí corrió, la
  guarda ve el campo lleno y sale — sin carreras ni dobles envíos. La carrera inversa
  también es benigna: si el respaldo escribe primero, Contact Info solo llena campos
  vacíos y el bot simplemente salta. Por eso el wait puede ser corto: los datos del
  24-ago muestran que cuando la captura del bot corre, escribe en el mismo minuto
  (y cuando no, no escribe ni en 7). Ajustado de 90/60 a 45/15 y luego a 20/5 a pedido de Oliver (con 20 s el
  respaldo suele ganarle al bot — da igual: escriben el mismo nombre oficial y el
  que llega segundo respeta al primero).
- Supervisión espera 5 s y los demás 20: "supervisión de melamina" contiene
  "melamina" y dispara ambos triggers; el de Supervisión escribe primero y la guarda
  del de Melamina lo respeta. (Mismo problema que resuelve la rama atrapadora de SP05.
  El escalón de ~15 s absorbe el jitter del motor de waits.)
- Palabras clave: heredadas de los CAMPOS de Francisco (en producción desde julio),
  menos los códigos cortos ambiguos (g1..g8, que son subcadena de g13/g16/g24/g25/g28).
- Valores escritos = nombres oficiales v4.2, que matchean las conds `contains` del
  árbol de SP05.
- Todo queda en DRAFT. ⚠️ PUBLICAR: SOLO con el toggle de la UI (Borrador→Publicar,
  una persona). La publicación por API resultó RULETA (24-ago): status:"published" es
  inerte, status:"publish" a veces publica de verdad y a veces deja el workflow en
  Borrador real mientras la API responde publish/active=true — la lectura por API del
  estado de publicación NO es confiable. La verdad: la lista de la UI + el Historial
  de inscripciones.
- Formas clonadas de moldes vivos: trigger de "CAMPOS 01 - Melamina" (message-body
  string-contains-any-of) + LS01 (has-tag) + guarda de SP06 (has_value, sin
  conditionValue) + esqueleto arbol() de WF-MOD.

RECETA DE TRIGGERS POR API QUE SÍ FUNCIONA (24-ago, validada dos veces):
  1. DELETE de triggers viejos → PAUSA ~25 s (el compilador del bucket es asíncrono;
     borrar y crear en ráfaga deja el evaluador desincronizado — ese fue el bug).
  2. POST del trigger fresco → pausa ~10 s.
  3. Transición GENUINA de publicación: GET fresco → PUT status draft → pausa →
     GET fresco → PUT status publish → pausa.
  4. Verificar que `active` del trigger quedó True COMO RESULTADO del publish (esa es
     la firma del publish real). Confirmar en la LISTA de la UI (Publicado verde) y
     con una prueba de mensaje + fila en Historial de inscripciones.

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
#
# ⚠️ LAS KEYWORDS SON PALABRAS COMPLETAS (TOKENS), NO RAÍCES. El operador
# string-contains-any-of matchea tokens exactos dentro del mensaje, NO subcadenas
# (experimento del 24-ago: "elect" no matchea la keyword "elec"). Cada variante y typo
# va como palabra completa; "sketch" no atrapa "sketchup" (van ambas); los códigos g#
# son seguros por tokens (g1 ≠ g13). Case-insensitive; tildes = carácter distinto.
CURSOS = [
    # (nombre, keywords, valor oficial, espera seg, "propio": si Curso de interés ya
    #  CONTIENE esto, el flujo sale sin actuar — es el mismo curso, no se re-envía)
    ("SP04.0 | Respaldo curso — Supervisión",
     ["supervision", "supervisión", "gestion de proyectos", "gestión de proyectos", "g2"],
     "Gestión y Supervisión de Melamina", 10, "Supervisi"),
    ("SP04.1 | Respaldo curso — Melamina",
     ["melamina", "melaminas", "melamine", "melanina", "malamina", "g13", "g16"],
     "Melamina", 30, "Melamina"),
    ("SP04.2 | Respaldo curso — Drywall",
     ["drywall", "draywall", "driwall", "drywal", "dry wall", "tabiqueria",
      "tabiquería", "g24", "g28"], "Drywall", 30, "Drywall"),
    ("SP04.3 | Respaldo curso — Electricidad",
     ["electricidad", "electricista", "electrica", "eléctrica", "electrico",
      "eléctrico", "domotica", "domótica", "g25"], "Electricidad y Domótica", 30,
     "Electricidad"),
    ("SP04.4 | Respaldo curso — SketchUp",
     ["sketchup", "sketch", "sketch up", "skechup", "skp", "g1"], "SketchUp", 30,
     "SketchUp"),
    ("SP04.5 | Respaldo curso — Revit",
     ["revit", "rebit", "bim", "lumion", "rvt", "g4", "g4.2"], "Revit BIM", 30, "Revit"),
    ("SP04.6 | Respaldo curso — Mobiliario",
     ["mobiliario", "mobiliarios", "g8"], "Diseño de Mobiliario", 30, "Mobiliario"),
    ("SP04.7 | Respaldo curso — Cocinas",
     ["cocina", "cocinas", "g5"], "Cocinas", 30, "Cocinas"),
    ("SP04.8 | Respaldo curso — AutoCAD",
     ["autocad", "auto cad", "g7"], "AutoCAD", 30, "AutoCAD"),
]


def cond_curso_tiene_valor():
    """Molde: guarda de SP06 (has_value NO lleva conditionValue)."""
    return {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(CURSO_KEY),
            "conditionOperator": "has_value", "__conditionId": nid(), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": NESTED, "allowIsOperatorTypes": ALLOWIS}


# Campos que se LIMPIAN al conmutar de curso (los datos del curso anterior no valen)
CAMPOS_LIMPIAR = [
    ("8oOOHVIItH65BSpNZPSq", "Modalidad (bot)", "string"),
    ("M2Ra6FDckxrylnFygVVH", "Modalidad", "select"),
    ("eEiZLOsgrVD8MPl16pOV", "Sede (bot)", "string"),
    ("B2tnsFlAOp9kYWF9Ij4R", "Sede", "select"),
    ("onMkfwvy1HsFUBZH13CJ", "Nivel de interés (bot)", "string"),
]

def n_limpiar(nodo_id, nxt=""):
    """Forma validada de clear_field_data (playbook §4: sin value/date/type correcto
    ejecuta customFields:[] — no-op silencioso)."""
    fs = [{"field": fid, "value": "", "title": titulo, "type": tipo, "date": ""}
          for fid, titulo, tipo in CAMPOS_LIMPIAR]
    return {"id": nodo_id, "order": 0,
            "attributes": {"actionType": "clear_field_data",
                           "type": "update_contact_field", "fields": fs},
            "name": "Limpiar datos del curso anterior",
            "type": "update_contact_field", "next": nxt}


def plantillas(valor, espera, propio):
    """CONMUTADOR DE CURSO (v2, 25-ago a pedido de Oliver):
    wait → ¿Curso ya CONTIENE el curso propio? → salir (no re-enviar la misma ficha)
         → None (campo vacío U OTRO curso): quitar ficha-enviada → limpiar modalidad/
           sede/nivel → escribir el curso nuevo → (el cambio dispara SP05, que ya sin
           el tag envía la ficha nueva y activa el bot de la familia nueva)."""
    q_id, l_id, u_id = nid(), nid(), nid()
    q = wf_lib.n_tag(q_id, ["ficha-enviada"], nxt=l_id, quitar=True)
    # ⚠️ Validador (25-ago): en cadenas, parentKey = el nodo que te REFERENCIA por next
    # (el predecesor), no la rama. El 1er nodo lo referencia la rama (arbol se lo pone);
    # del 2º en adelante hay que ponerlo explícito o el PUT rechaza con
    # "parentKey is <rama> instead of <predecesor>".
    l = n_limpiar(l_id, nxt=u_id); l["parent"] = q_id; l["parentKey"] = q_id
    u = n_update(u_id, [(CURSO_KEY, valor)], name=f"Curso = {valor}",
                 parent=l_id)
    t = arbol([
        ("Ya tiene ESTE curso (no re-enviar)",
         [wf_lib.cond_field(CURSO_KEY, propio, "contain")], []),
    ], none_next=[q, l, u])
    wait_id = nid()
    w = n_wait(wait_id, espera, unidad="seconds", nxt=t[0]["id"])
    # Validador de publicación: cadena raíz exige parent/parentKey del que referencia.
    t[0]["parent"] = wait_id
    t[0]["parentKey"] = wait_id
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

    for nombre, keywords, valor, espera, propio in CURSOS:
        corto = nombre.split("—")[-1].strip()
        if nombre in existentes and not args.aplicar:
            print(f"YA EXISTE  {nombre}")
            continue
        if not args.aplicar:
            print(f"DRY-RUN    {nombre}: keywords={keywords} → Curso='{valor}' (wait {espera}s, propio={propio})")
            continue

        wid = existentes.get(nombre)
        if not wid:                                    # idempotencia
            wf = C.request("POST", f"/workflow/{LOC}", {"name": nombre, "parentId": CARPETA})
            wid = wf.get("id") if isinstance(wf, dict) else None
            if not wid:
                print(f"ERROR creando {nombre}: {wf}"); continue

        temps, wait_id = plantillas(valor, espera, propio)
        d = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
        r = C.request("PUT", f"/workflow/{LOC}/{wid}",
                      {"name": nombre, "version": d.get("version", 1), "parentId": CARPETA,
                       "status": d.get("status") or "draft", "allowMultiple": True,
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
