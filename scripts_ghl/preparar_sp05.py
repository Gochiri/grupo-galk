"""SP05 queda armado y conectado. El contenido de las fichas se carga al final.

POR QUÉ AHORA
-------------
Los 24 custom values de ficha están vacíos y las plantillas WABA son placeholders. Da igual:
lo que se quiere dejar listo hoy es **la fontanería** — que SP05 entre cuando debe, no entre
dos veces y no diga cosas que el cliente ya descartó. El contenido se carga después, en una
sola pasada, sin volver a tocar la estructura.

LOS TRES ARREGLOS
-----------------

1. **Entra por los datos, no por el capricho del bot.** Mismo problema que SP06: la acción
   *Enviar ficha del curso* llama a SP05 con `add_to_workflow` en el mismo turno en que
   *Contact Info* extrae el dato, así que llega antes de que el campo se escriba, la guarda
   ve `Sede` vacía y corta. Se le agregan tres triggers `contact_changed`, uno por campo
   canónico: el último dato en llegar es el que enrola.

2. **Marcador de "ya enviada".** Con tres triggers, sin marcador, la ficha saldría hasta tres
   veces. Se agrega un nodo que pone el tag `ficha-enviada` justo después de la guarda, y el
   tag se suma a la guarda. Primera pasada envía, las demás cortan.

   Ojo: el tag se pone **antes** del árbol, así que si un curso no matchea ninguna de las 24
   ramas el contacto queda marcado sin haber recibido nada. Es el caso raro y el precio de no
   meter 24 nodos más; si algún día molesta, se mueve el tag al final de cada rama.

3. **Fuera la pregunta por el horario.** Los 24 mensajes decían *"¿qué horario te acomoda
   mejor?"*, que es del flujo viejo — el cliente decidió que los horarios los da el asesor
   (§D1). Además una pregunta lanzada desde un workflow **compite con el bot**, que está
   llevando la conversación en paralelo. Queda solo la línea de entrega.

NO SE TOCA
----------
El `template_id` y el `from_phone_number` siguen siendo los placeholders de `wf_lib`, y los
`media_url` siguen apuntando a los `{{custom_values.ficha_*}}` vacíos. Eso es justamente lo
que se carga al final.
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, nid

WID = "ae78625c-8f91-4af1-a7b0-3be0b2e4a667"
TAG = "ficha-enviada"
CAMPOS = ["contact.curso_de_inters", "contact.modalidad", "contact.sede"]
MSG_VIEJO = "Cuéntame, ¿qué horario te acomoda mejor?"
MSG_NUEVO = "¡Aquí tienes la información de tu curso! 👇"


def cond_tag_puesto(tag):
    """El contacto YA tiene el tag. Distinto de cond_tag(), que es para triggers."""
    return {"conditionType": "contact_detail", "conditionSubType": "tags",
            "conditionOperator": "index-of-true", "conditionValue": [tag],
            "__conditionId": nid(), "ifElseNodeId": "", "__customFieldType__": "standard",
            "isWait": False, "nestedDropdownTypes": wf_lib.NESTED,
            "allowIsOperatorTypes": wf_lib.ALLOWIS}


def main():
    d = C.request("GET", f"/workflow/{LOC}/{WID}")
    if not d or not (d.get("workflowData") or {}).get("templates"):
        d = C.request("GET", f"/workflow/{LOC}/{WID}")          # el API interna falla a veces
    tpl = (d.get("workflowData") or {}).get("templates") or []
    estado = d.get("status")
    if not tpl:
        sys.exit("ABORT: no pude leer los nodos de SP05")
    print(f"SP05 {estado} v{d.get('version')} · {len(tpl)} nodos")

    heads = [n for n in tpl if n.get("nodeType") == "condition-node"]
    guarda, arbol = heads[0], heads[1]
    rama = guarda["attributes"]["branches"][0]
    seg = rama["segments"][0]
    none_guarda = next(n for n in tpl if n.get("nodeType") == "branch-no"
                       and n.get("parentKey") == guarda["id"])

    cambios = []

    # 1 · tag en la guarda, para no reenviar
    if not any(c.get("conditionSubType") == "tags" for c in seg["conditions"]):
        seg["operator"] = "or"
        rama["operator"] = "or"
        seg["conditions"].insert(0, cond_tag_puesto(TAG))
        rama["name"] = "No enviar (ya enviada o faltan datos)"
        cambios.append(f"guarda + tag '{TAG}'")

    # 2 · nodo que pone el tag, entre la guarda y el árbol de 24 ramas
    ya = next((n for n in tpl if n.get("type") == "add_contact_tag"
               and TAG in ((n.get("attributes") or {}).get("tags") or [])), None)
    if not ya:
        marcador = nid()
        tpl.append({**wf_lib.n_tag(marcador, [TAG], nxt=arbol["id"],
                                   parent=none_guarda["id"]),
                    "name": "Marcar ficha enviada"})
        none_guarda["next"] = marcador
        arbol["parent"] = marcador
        arbol["parentKey"] = marcador
        cambios.append("nodo 'Marcar ficha enviada'")

    # 3 · fuera la pregunta por el horario
    n_msg = 0
    for n in tpl:
        a = n.get("attributes") or {}
        if n.get("type") == "whatsapp_v2" and MSG_VIEJO in (a.get("message") or ""):
            a["message"] = MSG_NUEVO
            n_msg += 1
    if n_msg:
        cambios.append(f"{n_msg} mensajes sin la pregunta de horario")

    if cambios:
        r = C.request("PUT", f"/workflow/{LOC}/{WID}",
                      {"name": d.get("name"), "version": d.get("version"),
                       "parentId": d.get("parentId"), "status": estado,
                       "workflowData": {"templates": tpl}})
        print("PUT:", "OK" if r and not r.get("_error") else r, "·", " · ".join(cambios))
    else:
        print("Nodos: ya estaban bien (idempotencia §3)")

    # 4 · triggers por datos, con el formato bueno (§ handoff)
    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    entrada = next(n["id"] for n in vt if n.get("nodeType") == "condition-node")
    trs = C.request("GET", f"/workflow/{LOC}/trigger?workflowId={WID}") or []
    puestos = {str(c.get("field", "")).split(".")[-1] for t in trs for c in (t.get("conditions") or [])}
    for k in CAMPOS:
        if wf_lib.FID(k) in puestos:
            print(f"  SKIP trigger {wf_lib.TITLE(k)}"); continue
        C.request("POST", f"/workflow/{LOC}/trigger", {
            "status": estado, "workflowId": WID, "schedule_config": {},
            "conditions": [wf_lib.cond_trigger_campo(k)],
            "type": "contact_changed", "masterType": "highlevel",
            "name": f"{wf_lib.TITLE(k)} cambió", "allowMultiple": "yes",
            "actions": [{"workflow_id": WID, "type": "add_to_workflow"}],
            "active": True, "triggersChanged": True, "location_id": LOC,
            "targetActionId": entrada,
            "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})
        print(f"  +    trigger {wf_lib.TITLE(k)}")

    # verificación
    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    g = next(n for n in vt if n.get("nodeType") == "condition-node")
    b = g["attributes"]["branches"][0]
    byid = {f["id"]: f["name"] for f in wf_lib._cf.values()}
    def et(c):
        s = c.get("conditionSubType")
        return ("tag " + str(c.get("conditionValue")) if s == "tags"
                else f"{byid.get(s, s)} {c.get('conditionOperator')}")
    print(f"\nVERIFY: {v.get('status')} · {len(vt)} nodos")
    print(f"  guarda '{b['name']}' ({b['segments'][0]['operator']}): "
          f"{' OR '.join(et(c) for c in b['segments'][0]['conditions'])}")
    print(f"  mensajes con la pregunta vieja: "
          f"{sum(1 for n in vt if MSG_VIEJO in ((n.get('attributes') or {}).get('message') or ''))}")
    for t in C.request("GET", f"/workflow/{LOC}/trigger?workflowId={WID}") or []:
        print(f"  [{t.get('type'):16}] {str(t.get('name')):26} active={t.get('active')} "
              f"entrada={'OK' if t.get('targetActionId') == g['id'] else 'ROTA'}")


if __name__ == "__main__":
    main()
