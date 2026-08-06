"""Arregla la cadena de pago SP09 → SP10 → SP10-B → SP11.

QUÉ ESTABA MAL
--------------
1. **Nadie disparaba nada.** SP10, SP10-B y SP11 tenían 0 triggers.
2. **SP10-B y SP11 movían los dos a Matriculado.** SP10-B con `status=open`, SP11 con
   `status=won`. Como nada dispara SP11, la oportunidad se quedaba en Matriculado
   **abierta** — el problema original de GALK (2.370 oportunidades 100% abiertas).
3. **Faltaba el nodo de tarea** en SP10, que la tarjeta sí pedía.
4. El trigger que pedía la tarjeta —"Customer Replied + filtro de etapa"— **no existe**:
   `customer_reply` solo filtra por `contact.tags`, `message.body` y `message.type`
   (que es *canal*, no tipo de adjunto).

CÓMO QUEDA
----------
    SP09  ─ manda datos de pago ─ tag `pago-datos-enviados`
      ↓  (el lead responde mencionando un pago)
    SP10  ─ trigger customer_reply: keywords de pago Y tag pago-datos-enviados
          ─ Comprobante recibido=Sí · etapa "Pago en validación" · TAREA · notif a Lucía
      ↓  (Lucía marca Comprobante validado)
    SP10-B ─ trigger contact_changed sobre "Comprobante validado"
           ─ IF = "Sí" → Validado por + fecha + tag `pago-validado`
           ─ IF = "No" → no hace nada (rechazo)
      ↓
    SP11  ─ trigger tag `pago-validado`
          ─ etapa Matriculado + status **won** + tags matriculado/alumno-activo

Cada workflow con una sola responsabilidad, y el cierre en `won` ocurre en un solo lugar.
El truco de las keywords sale del workflow VIVO de Francisco `ALERTA - Pago por verificar`.
"""
import sys, json, pathlib

sys.path.insert(0, str(pathlib.Path("/home/user/grupo-galk/scripts_ghl")))
import wf_lib
from wf_lib import C, LOC, ST, nid, n_opp, n_update, n_tag, n_notif, arbol

SP09, SP10 = "23059046-b1d2-4419-b520-2c45b2342af1", "0b0ff827-27d1-4351-85ad-5365ca116d0c"
SP10B, SP11 = "231be518-b996-4b2f-b916-4ac407f77956", "2a7a0689-7162-40a8-9485-46578438e3bd"

TAG_ENVIADO, TAG_VALIDADO = "pago-datos-enviados", "pago-validado"
SUPERVISORA = wf_lib.SUPERVISORA
KEYWORDS = ["yape", "plin", "voucher", "boleta", "comprobante", "pagué", "pague",
            "deposité", "transferí", "constancia", "captura", "pago"]


def put(wid, templates, nombre=None):
    d = C.request("GET", f"/workflow/{LOC}/{wid}")
    r = C.request("PUT", f"/workflow/{LOC}/{wid}",
                  {"name": nombre or d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"), "status": "draft",
                   "workflowData": {"templates": templates}})
    return bool(r and not (isinstance(r, dict) and r.get("_error")))


def trigger(wid, body_extra, nombre, tipo):
    """Los triggers viven fuera del workflow. active=False SIEMPRE: True publica."""
    if C.request("GET", f"/workflow/{LOC}/trigger?workflowId={wid}"):
        print(f"      trigger ya existía, no lo toco")
        return
    d = C.request("GET", f"/workflow/{LOC}/{wid}") or {}
    first = ((d.get("workflowData") or {}).get("templates") or [{}])[0].get("id")
    body = {"status": "draft", "workflowId": wid, "schedule_config": {},
            "type": tipo, "masterType": "highlevel", "name": nombre, "allowMultiple": "no",
            "actions": [{"workflow_id": wid, "type": "add_to_workflow"}],
            "active": False, "triggersChanged": True, "location_id": LOC,
            "targetActionId": first, "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}}
    body.update(body_extra)
    C.request("POST", f"/workflow/{LOC}/trigger", body)


def n_task(nodo_id, titulo, cuerpo, nxt="", parent=None):
    """Nodo 'Add task'. Requiere workflowsActionType INTERNAL, como whatsapp_v2."""
    n = {"id": nodo_id, "order": 0,
         "attributes": {"title": titulo,
                        "body": f'<p style="margin:0px; padding-left: 0px!important;">{cuerpo}</p>',
                        "assignedTo": SUPERVISORA,
                        "dueDate": {"duration": 1, "unit": "days", "skipWeekends": False},
                        "type": "task_notification", "__customInputs__": {}},
         "name": "Add task", "type": "task-notification",
         "workflowsActionType": "INTERNAL", "next": nxt}
    if parent:
        n["parentKey"] = parent
    return n


def main():
    for t in (TAG_ENVIADO, TAG_VALIDADO):
        C.create_location_tag(t)

    # ---------- SP09: marcar que ya se mandaron los datos de pago ----------
    d = C.request("GET", f"/workflow/{LOC}/{SP09}")
    tpl = (d.get("workflowData") or {}).get("templates") or []
    nuevos = []
    for n in tpl:
        # los dos finales de rama (el whatsapp del pack y la notificación del estándar)
        if n.get("type") in ("whatsapp_v2", "internal_notification") and not n.get("next"):
            t = nid()
            n = {**n, "next": t}
            nuevos.append(n)
            nuevos.append(n_tag(t, [TAG_ENVIADO], parent=n.get("parentKey") or n.get("parent")))
        else:
            nuevos.append(n)
    print(f"SP09  tag '{TAG_ENVIADO}' en los finales de rama:",
          "OK" if put(SP09, nuevos) else "ERR", f"({len(tpl)}→{len(nuevos)} nodos)")

    # ---------- SP10: nodo de tarea + trigger por keywords ----------
    d = C.request("GET", f"/workflow/{LOC}/{SP10}")
    tpl = (d.get("workflowData") or {}).get("templates") or []
    opp = next(n for n in tpl if n["type"] == "create_opportunity")
    notif = next(n for n in tpl if n["type"] == "internal_notification")
    tid = nid()
    tpl = [({**n, "next": tid} if n["id"] == opp["id"] else n) for n in tpl]
    tpl.insert([i for i, n in enumerate(tpl) if n["id"] == opp["id"]][0] + 1,
               n_task(tid, "🧾 Validar comprobante de pago",
                      "El lead envió un comprobante. Verificar el pago en la cuenta real. "
                      "Si es correcto, marcar el campo «Comprobante validado» = Sí en el "
                      "contacto: eso dispara la matrícula automáticamente.",
                      nxt=notif["id"]))
    print("SP10  nodo de tarea:", "OK" if put(SP10, tpl) else "ERR", f"({len(tpl)} nodos)")
    trigger(SP10, {"conditions": [
        {"operator": "string-contains-any-of", "field": "message.body", "value": KEYWORDS,
         "title": "Message body", "type": "string", "id": "message-body"},
        {"operator": "index-of-true", "field": "contact.tags", "value": TAG_ENVIADO,
         "title": "Has tag", "type": "select", "id": "has-tag"}]},
        "Comprobante de pago recibido", "customer_reply")

    # ---------- SP10-B: solo valida, ya no mueve etapa ----------
    campo = "contact.comprobante_validado"
    upd, tag = nid(), nid()
    rama = [n_update(upd, [("contact.validado_por", "{{user.name}}"),
                           ("contact.fecha_de_validacin", "{{right_now}}")],
                     nxt=tag, name="Validado por + fecha"),
            n_tag(tag, [TAG_VALIDADO])]
    cond = {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(campo),
            "conditionOperator": "is", "conditionValue": "Sí", "__conditionId": nid(),
            "ifElseNodeId": "", "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": wf_lib.NESTED, "allowIsOperatorTypes": wf_lib.ALLOWIS}
    tpl = arbol([("Comprobante validado = Sí", [cond], rama)])
    print("SP10-B sin movimiento de etapa + if/else:", "OK" if put(SP10B, tpl) else "ERR",
          f"({len(tpl)} nodos)")
    trigger(SP10B, {"conditions": [
        {"operator": "has-changed", "field": wf_lib.FID(campo),
         "title": "Comprobante validado", "type": "text"}]},
        "Comprobante validado cambió", "contact_changed")

    # ---------- SP11: dispara con el tag ----------
    trigger(SP11, {"conditions": [
        {"operator": "index-of-true", "field": "tagsAdded", "value": TAG_VALIDADO,
         "title": "Tag Added", "type": "select", "id": "tag-added"}]},
        "Pago validado", "contact_tag")
    print("SP11  trigger por tag: OK")


if __name__ == "__main__":
    main()
