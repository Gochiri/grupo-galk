"""SP05 v2 — "Secuencia de ficha" según reunión 19-ago (ACUERDOS-reunion-2026-08-19.md §1).

La ficha se dispara AL DETECTAR EL CURSO (ya no al confirmar sede). Árbol por CURSO con las
3 ramas de talleres; software/gestión caen en None (silencioso) hasta que llegue su contenido.

Cada rama de taller (9 nodos):
  1. apagar bot          (update_conversation_ai_status keep-same/inactive, clonado de SP06)
  2. SMS apertura        (texto oficial de Lucía, firmado Valeria)
  3-6. SMS imagen 1-4    (caption corto + línea "image - <url>" que el gateway vuelve imagen)
  7. SMS pregunta final  ("¿Surco, Los Olivos o Provincia Arequipa?")
  8. tag ficha-enviada   (marcador DESPUÉS del envío)
  9. activar BOT-01      (update_conversation_ai_status bot concreto/active, clonado de LS01)

Guarda de entrada (exit): tag ficha-enviada presente OR Curso de interés vacío.
Triggers que quedan: 'Curso de interés cambió' + 'Enviar Ficha' (tag). Los de Sede/Modalidad
se ELIMINAN (con la ficha temprana provocarían dobles envíos por carrera con el marcador).

El PUT reutiliza el workflow SP05 existente (mismo ID). Los nodos v1 quedan respaldados en
sp05_v1_backup.json. allowMultiple SIEMPRE en el body (gotcha 19-ago).

Excepción temporal documentada: URLs del CDN en el body (pilot SMS); los custom values
se remodelan cuando entren las plantillas WABA.

Uso: build_sp05_v2.py [--aplicar]   (sin flag = dry-run: imprime resumen y valida clones)
"""
import os, sys, json, uuid, pathlib
ROOT = pathlib.Path("/home/user/grupo-galk")
for l in (ROOT / ".env").read_text().splitlines():
    l = l.strip()
    if l and not l.startswith("#") and "=" in l:
        k, v = l.split("=", 1); os.environ.setdefault(k.strip(), v.strip())
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts_ghl"))
from wf_lib import C, LOC

SP05 = "ae78625c-8f91-4af1-a7b0-3be0b2e4a667"
SP06 = "84811c16-30d8-4c08-a05d-0c12fa46567d"
BOT01 = "L9hj6kGF7Ie73EhRzgqD"          # BOT-01 Talleres
CURSO_ID = "bjDW7b9QoRiFWL5d578w"        # ID del campo Curso de interés (el de los triggers)
BACKUP = ROOT / "scripts_ghl" / "sp05_v1_backup.json"
CDN = "https://assets.cdn.filesafe.space/YN2uRSDcNeBdTWm3UPCU/media/%s.jpeg"

def nid(): return str(uuid.uuid4())

# ---------- contenido oficial (contenido-fichas/*.md, verbatim, firmado Valeria) ----------
APERTURA_ELEC = """💬 ¡Hola! ¿Cuál es tu nombre? 😊
Soy Valeria de Grupo GALK y tengo una oportunidad especial para ti 🎉

Aprende una habilidad muy demandada con nuestro G25 Taller de Electricidad y Automatización Residencial ⚡💡
Un curso *100% práctico*, ideal para comenzar desde cero y desarrollar competencias reales en instalaciones eléctricas y automatización.

📌 Ofertas vigentes por tiempo limitado:
✅ S/600 – separa tu vacante con S/100

📍*Sedes:* Lima-Surco (Calle Aldabas 559) o Los Olivos (Av. Antunes de Mayolo 822). Provincia-Arequipa (Calle José Santos Chocano 249– Umacollo)
🧾 Incluye: certificación, materiales y asesorías personalizadas

📸 Te comparto las imágenes del taller con toda la información y beneficios. ¡Mira lo completo que está este programa! 👇"""

APERTURA_MELA = """💬 ¡Hola! ¿Cuál es tu nombre? 😊
Soy Valeria del equipo de Grupo GALK, ¡un gusto saludarte! 🙌
Me alegra mucho tu interés en nuestro Taller de Armado de Muebles en Melamina 🎉

Este taller es una gran oportunidad para aprender desde cero a trabajar con melamina y fabricar tus propios muebles paso a paso, incluso si nunca antes lo has hecho 🪚✨

📌 Ofertas vigentes hasta el 24 de agosto:
✅ S/525 un taller (G13 – Taller desde Cero o G16 – Taller Avanzado 16 hrs cada uno) – separa tu vacante con S/100
✅ S/890 el Pack Completo (G13 + G16 – Desde Cero + Avanzado 32 hrs) – separa con S/200

📍*Sedes:* Lima-Surco (Calle Aldabas 559) o Los Olivos (Av. Antunes de Mayolo 822). Provincia-Arequipa (Calle José Santos Chocano 249)
🧾 Incluye: certificación, materiales y asesorías personalizadas
⚠️ Importante – Requisitos para el taller: Por temas de *seguridad e higiene*, los alumnos deberán asistir obligatoriamente con:
🧤 Guantes con palma de nitrilo
👓 Lentes de seguridad transparentes

📸 Te comparto las imágenes del taller con toda la información y beneficios. ¡Mira lo completo que está este programa! 👇"""

APERTURA_DRY = """💬 ¡Hola! ¿Cuál es tu nombre? 😊
Soy Valeria del equipo de Grupo GALK y tengo una oferta especial para ti 🎉

Aprende a construir y diseñar con Drywall desde cero con nuestro Taller de Sistemas Constructivos en Drywall 🧱💪
Ideal si buscas capacitarte profesionalmente o emprender en el rubro de la construcción ligera.

📌 Ofertas vigentes hasta el 24 de agosto:
✅ S/450 – un taller (G24 – Desde Cero o G28 – Avanzado, 16 hrs cada uno) – reserva con S/100
✅ S/850 – Pack Completo (G24 + G28 – Desde Cero + Avanzado, 32 hrs) – reserva con S/200

📍*Sedes:* Lima-Surco (Calle Aldabas 559) o Los Olivos (Av. Antunes de Mayolo 822). Provincia-Arequipa (Calle José Santos Chocano 249)
🧾 Incluye: certificación y asesoría personalizada
⚠️ Importante – Requisitos para el taller: Por temas de *seguridad e higiene*, los alumnos deberán asistir obligatoriamente con:
🧤 Guantes con palma de nitrilo
👓 Lentes de seguridad transparentes
*CUTTERS DE MANGO GRUESO*

📸 Te comparto las imágenes del taller con toda la información y beneficios. ¡Mira lo completo que está este programa! 👇"""

FINAL_MSG = """✨ Una vez que me confirmes tu nombre, te envío los horarios y fechas disponibles en la sede que te quede más cerca.
¿Te interesa en Surco, Los Olivos o Provincia Arequipa? 😊"""

# (nombre, condiciones "contains" sobre Curso de interés, apertura, [(caption, media_id) x4])
# La rama Supervisión va PRIMERA y sin nodos: "Gestión y Supervisión de Melamina" contiene
# "melamina" y sin esta atrapadora se llevaría la ficha del taller. Sale sin enviar nada
# (su ficha de gestión llega después).
RAMAS = [
    ("Supervision (gestion, sin ficha aun)", ["supervisi"], None, []),
    ("Melamina", ["melamina"], APERTURA_MELA, [
        ("🪚 Así se vive el taller — 100% práctico y presencial", "6a4b0fed70834e617c689aa1"),
        ("📚 Temario completo: las 16 horas, paso a paso",          "6a4b0fed1bf938e5479bed61"),
        ("💪 Dos niveles: G13 desde cero a intermedio · G16 avanzado", "6a4b0fed8a69aa2441919a1a"),
        ("📝 Reserva tu vacante con S/100 — medios de pago",        "6a4b0fed8a69aa2441919a14"),
    ]),
    ("Drywall", ["drywall"], APERTURA_DRY, [
        ("🧱 Así se vive el taller — 100% práctico y presencial",   "6a4da7e82467f0ff08fed87d"),
        ("📚 Temario completo: las 16 horas, paso a paso",          "6a4da7f02467f0ff08ff12a5"),
        ("💪 Dos niveles: G24 desde cero a intermedio · G28 avanzado", "6a4da7f01e3d535c0821a6ae"),
        ("📝 Reserva tu vacante con S/100 — medios de pago",        "6a4da7f02d9cf805155950d4"),
    ]),
    ("Electricidad", ["electricidad"], APERTURA_ELEC, [
        ("⚡ Así se vive el taller — 100% práctico y presencial",   "6a51b6b1eada8c1f450813db"),
        ("📚 Temario completo: las 20 horas, paso a paso",          "6a51b6b19c9b37b5fd3f5d4a"),
        ("💪 Empiezas desde cero, sales instalando y automatizando", "6a51b6b10e67afc013822d3f"),
        ("📝 Reserva tu vacante con S/100 — medios de pago",        "6a51b6b1eada8c1f450813d7"),
    ]),
]

# ---------- clonar formas vivas (regla de oro) ----------
def clonar_ai_status():
    """Devuelve (attrs_apagar, attrs_activar) clonados de nodos hechos/validados en la UI."""
    apagar = activar = None
    d6 = C.request("GET", f"/workflow/{LOC}/{SP06}")
    for n in d6["workflowData"]["templates"]:
        if n["type"] == "update_conversation_ai_status":
            a = json.loads(json.dumps(n["attributes"]))
            if str(a.get("status", a.get("botStatus", ""))).lower().startswith("inactive") or "inactive" in json.dumps(a).lower():
                apagar = a
    ws = C.request("GET", f"/workflow/{LOC}")
    ls01 = [w for w in ws if w.get("name", "").startswith("LS01")][0]
    dl = C.request("GET", f"/workflow/{LOC}/{ls01['id']}")
    for n in dl["workflowData"]["templates"]:
        if n["type"] == "update_conversation_ai_status" and "active" == str(n["attributes"].get("status", "")).lower():
            activar = json.loads(json.dumps(n["attributes"]))
    if not (apagar and activar):
        print("ABORT: no pude clonar los nodos de AI status (apagar=%s activar=%s)" % (bool(apagar), bool(activar)))
        print("  SP06 y LS01 deben tener sus nodos update_conversation_ai_status vivos.")
        sys.exit(1)
    # el de activar debe apuntar a BOT-01 (el bot va en assignedEmployeeId)
    activar["assignedEmployeeId"] = BOT01
    return apagar, activar

def cond_curso(valor):
    return {"conditionType": "contact_detail", "conditionSubType": CURSO_ID,
            "conditionOperator": "contains", "conditionValue": valor,
            "__conditionId": nid(), "ifElseNodeId": "", "__customFieldType__": "standard", "isWait": False}

def n_sms(nodo_id, body, name, nxt="", parent=None):
    n = {"id": nodo_id, "order": 0,
         "attributes": {"template_id": "", "body": body, "attachments": []},
         "name": name, "type": "sms", "next": nxt}
    if parent: n.update({"parent": parent, "parentKey": parent})
    return n

def main():
    aplicar = "--aplicar" in sys.argv
    d5 = C.request("GET", f"/workflow/{LOC}/{SP05}")
    v1 = d5["workflowData"]["templates"]
    if not BACKUP.exists():
        BACKUP.write_text(json.dumps(v1, ensure_ascii=False, indent=1))
        print(f"backup v1: {len(v1)} nodos -> {BACKUP.name}")
    ya_v2 = any("Supervision" in (n.get("name") or "") for n in v1)
    if ya_v2:
        print("SP05 ya es v2 (idempotencia §3). Nada que hacer."); return

    apagar_attrs, activar_attrs = clonar_ai_status()
    print("clones OK · apagar:", json.dumps(apagar_attrs, ensure_ascii=False)[:120])
    print("           activar:", json.dumps(activar_attrs, ensure_ascii=False)[:120])

    # ---- guarda de entrada: salir si ficha-enviada o curso vacío ----
    hdr_id, out_id, tree_id, none_id = nid(), nid(), nid(), nid()
    guard_branch = {"id": out_id, "name": "No enviar (ya enviada o sin curso)",
        "segments": [{"__segmentId": nid(), "operator": "or", "conditions": [
            {"conditionType": "contact_detail", "conditionSubType": "tags",
             "conditionOperator": "index-of-true", "conditionValue": ["ficha-enviada"],
             "__conditionId": nid(), "ifElseNodeId": "", "__customFieldType__": "standard", "isWait": False},
            {"conditionType": "contact_detail", "conditionSubType": CURSO_ID,
             "conditionOperator": "has_no_value",
             "__conditionId": nid(), "ifElseNodeId": "", "__customFieldType__": "standard", "isWait": False},
        ]}]}
    nodes = []
    hdr = {"id": hdr_id, "order": 0, "attributes": {"if": False, "conditionName": "Condition",
           "operator": "and", "branches": [guard_branch]}, "name": "yes", "type": "if_else",
           "cat": "conditions", "next": ""}
    out_node = {"id": out_id, "order": 0, "attributes": {"if": False, "conditionName": "Condition",
        "operator": "and", "branches": []}, "name": "No enviar (ya enviada o sin curso)",
        "type": "if_else", "nodeType": "branch-yes", "cat": "conditions", "sibling": [],
        "parent": hdr_id, "parentKey": hdr_id, "next": ""}      # rama de salida: FIN
    guard_none = {"id": tree_id, "order": 0, "attributes": {"if": False, "conditionName": "Condition",
        "operator": "and", "branches": []}, "name": "None", "type": "if_else",
        "nodeType": "branch-no", "cat": "conditions", "sibling": [out_id],
        "parent": hdr_id, "parentKey": hdr_id, "next": ""}
    out_node["sibling"] = [tree_id]

    # ---- árbol por curso colgado del None de la guarda ----
    branch_ids = {nombre: nid() for nombre, *_ in RAMAS}
    tree_hdr_id = nid()
    tree_branches = []
    for nombre, conds, _, _ in RAMAS:
        tree_branches.append({"id": branch_ids[nombre], "name": nombre,
            "segments": [{"__segmentId": nid(), "operator": "or",
                          "conditions": [cond_curso(v) for v in conds]}]})
    tree_hdr = {"id": tree_hdr_id, "order": 0, "attributes": {"if": False,
        "conditionName": "Condition", "operator": "and", "branches": tree_branches},
        "name": "yes", "type": "if_else", "cat": "conditions",
        "parent": tree_id, "parentKey": tree_id, "next": ""}
    guard_none["next"] = tree_hdr_id

    grupo = list(branch_ids.values()) + [none_id]
    for nombre, conds, apertura, imgs in RAMAS:
        bid = branch_ids[nombre]
        sib = [x for x in grupo if x != bid]
        if apertura is None:      # rama atrapadora: sale sin enviar nada
            nodes.append({"id": bid, "order": 0, "attributes": {"if": False, "conditionName": "Condition",
                "operator": "and", "branches": []}, "name": nombre, "type": "if_else",
                "nodeType": "branch-yes", "cat": "conditions", "sibling": sib,
                "parent": tree_hdr_id, "parentKey": tree_hdr_id, "next": ""})
            continue
        ids = [nid() for _ in range(9)]
        nodes.append({"id": bid, "order": 0, "attributes": {"if": False, "conditionName": "Condition",
            "operator": "and", "branches": []}, "name": nombre, "type": "if_else",
            "nodeType": "branch-yes", "cat": "conditions", "sibling": sib,
            "parent": tree_hdr_id, "parentKey": tree_hdr_id, "next": ids[0]})
        # 1 apagar bot
        nodes.append({"id": ids[0], "order": 0, "attributes": json.loads(json.dumps(apagar_attrs)),
            "name": "Bot en pausa (secuencia)", "type": "update_conversation_ai_status",
            "workflowsActionType": "INTERNAL", "parent": bid, "parentKey": bid, "next": ids[1]})
        # 2 apertura
        nodes.append(n_sms(ids[1], apertura, f"Secuencia ficha: {nombre}", nxt=ids[2], parent=ids[0]))
        # 3-6 imágenes
        for i, (cap, mid) in enumerate(imgs):
            body = f"{cap}\n\nimage - {CDN % mid}"
            nodes.append(n_sms(ids[2 + i], body, f"Imagen {i+1}: {nombre}", nxt=ids[3 + i], parent=ids[1 + i]))
        # 7 pregunta final
        nodes.append(n_sms(ids[6], FINAL_MSG, f"Pregunta de sede: {nombre}", nxt=ids[7], parent=ids[5]))
        # 8 marcador
        nodes.append({"id": ids[7], "order": 0, "attributes": {"tags": ["ficha-enviada"]},
            "name": "Marcar ficha-enviada", "type": "add_contact_tag",
            "parent": ids[6], "parentKey": ids[6], "next": ids[8]})
        # 9 activar BOT-01
        nodes.append({"id": ids[8], "order": 0, "attributes": json.loads(json.dumps(activar_attrs)),
            "name": "Activar BOT-01 Talleres", "type": "update_conversation_ai_status",
            "workflowsActionType": "INTERNAL", "parent": ids[7], "parentKey": ids[7], "next": ""})
    # None del árbol: software/gestión — salida silenciosa hasta tener su contenido
    nodes.append({"id": none_id, "order": 0, "attributes": {"if": False, "conditionName": "Condition",
        "operator": "and", "branches": []}, "name": "None", "type": "if_else",
        "nodeType": "branch-no", "cat": "conditions", "sibling": list(branch_ids.values()),
        "parent": tree_hdr_id, "parentKey": tree_hdr_id, "next": ""})

    tpl = [hdr, out_node, guard_none, tree_hdr] + nodes
    print(f"v2: {len(tpl)} nodos · 3 ramas x 9 + guarda + árbol")
    if not aplicar:
        print("(dry-run — usa --aplicar)"); return

    r = C.request("PUT", f"/workflow/{LOC}/{SP05}",
                  {"name": d5.get("name"), "version": d5.get("version"),
                   "parentId": d5.get("parentId"), "status": d5.get("status"),
                   "allowMultiple": True, "workflowData": {"templates": tpl}})
    print("PUT:", "OK" if r and not (isinstance(r, dict) and r.get("_error")) else r)
    if isinstance(r, dict) and r.get("_error"):
        sys.exit(1)

    # ---- triggers: reapuntar los 2 buenos al header nuevo, borrar Sede/Modalidad ----
    trs = C.request("GET", f"/workflow/{LOC}/trigger?workflowId={SP05}") or []
    if isinstance(trs, dict): trs = trs.get("triggers", [])
    for t in trs:
        nombre = t.get("name", "")
        if nombre in ("Sede cambió", "Modalidad cambió"):
            rr = C.request("DELETE", f"/workflow/{LOC}/trigger/{t['id']}")
            print(f"trigger {nombre!r}: DELETE", "OK" if not (isinstance(rr, dict) and rr.get("_error")) else rr)
        else:
            body = {k: t[k] for k in t if not k.startswith("_")}
            body["targetActionId"] = hdr_id
            rr = C.request("PUT", f"/workflow/{LOC}/trigger/{t['id']}", body)
            print(f"trigger {nombre!r}: retarget ->", "OK" if not (isinstance(rr, dict) and rr.get("_error")) else rr)

    # ---- verificación ----
    d2 = C.request("GET", f"/workflow/{LOC}/{SP05}")
    tipos = {}
    for n in d2["workflowData"]["templates"]:
        tipos[n["type"]] = tipos.get(n["type"], 0) + 1
    print("tras PUT:", tipos, "· allowMultiple:", d2.get("allowMultiple"), "· status:", d2.get("status"))
    trs2 = C.request("GET", f"/workflow/{LOC}/trigger?workflowId={SP05}") or []
    if isinstance(trs2, dict): trs2 = trs2.get("triggers", [])
    ids2 = {n["id"] for n in d2["workflowData"]["templates"]}
    for t in trs2:
        ta = t.get("targetActionId")
        print(f"trigger {t.get('name')!r}: active={t.get('active')} target={'OK' if (ta is None or ta in ids2) else 'ROTO'}")

if __name__ == "__main__":
    main()
