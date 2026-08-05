"""SP06 v2 — la asignación deja de ser lineal y pasa a ser condicional.

QUÉ ESTABA MAL EN v1 (7 nodos, lineales)
----------------------------------------
1. Dos `create_opportunity` seguidos: etapa "Calificado" y, milisegundos después,
   etapa "Asignado a asesor". Nadie ve nunca la oportunidad en Calificado y el
   tiempo-en-etapa de esa etapa da ~0 para todos los leads.
2. El segundo `create_opportunity` omitía `opportunity_source`. Como en realidad es
   create-OR-UPDATE y reescribe con lo que le mandes, borraba la atribución de Meta
   que LS01 se toma el trabajo de capturar.
3. Sin rama de fallo: si el round robin no asignaba, el flujo igual escribía el campo
   vacío, igual movía la oportunidad, igual notificaba a nadie e igual ponía
   `bot-silenciado`. El lead quedaba marcado como atendido, con el bot mudo y sin
   dueño humano. Se perdía en silencio.

v2: el segundo movimiento de etapa cuelga de un if/else sobre "Asesor asignado".
Así "Calificado" pasa a significar algo real — calificado y todavía sin dueño —
que es donde se queda la oportunidad si el round robin falla.

Operadores verificados contra la subcuenta: `has_value` / `has_no_value` van SIN
clave `conditionValue` (visto en WF1 de Francisco y en LS01/SP05).
"""
import os, sys, json, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, ST, PIPE, SUPERVISORA, nid, n_opp, n_update, n_tag, n_notif, n_wait, arbol

WID = "84811c16-30d8-4c08-a05d-0c12fa46567d"
TAG_FALLO = "asignacion-fallida"

# --- claves de campo (fieldKey) que usa n_update -----------------------------
K_CALIF      = "contact.calificado"
K_F_CALIF    = "contact.fecha_de_calificacin"
K_ASESOR     = "contact.asesor_asignado_nuevo"
K_F_ASIGNA   = "contact.fecha_de_asignacin"


def cond_has_value(field_key):
    """has_value NO lleva conditionValue. Verificado en workflows vivos."""
    return {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(field_key),
            "conditionOperator": "has_value", "__conditionId": nid(), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": wf_lib.NESTED, "allowIsOperatorTypes": wf_lib.ALLOWIS}


def construir(assign_node_attrs):
    n_calif, n_oppc, n_asig, n_wt, n_upd = nid(), nid(), nid(), nid(), nid()

    # --- rama SÍ: la asignación funcionó ---
    s_opp, s_notif, s_tag = nid(), nid(), nid()
    rama_ok = [
        n_opp(s_opp, ST["asignado"], nxt=s_notif, name="Oportunidad → Asignado a asesor",
              extra={"opportunity_source": "{{contact.fuente}}"}),   # NO omitir la fuente
        {**n_notif(s_notif, "🎯 Lead calificado asignado",
                   "Nuevo lead calificado asignado: {{contact.name}} ({{contact.phone}}) — "
                   "{{contact.curso_de_inters}} / {{contact.sede}} / {{contact.horario_de_inters}}",
                   tipo_user="assigned_user"),
         "next": s_tag},
        n_tag(s_tag, ["bot-silenciado"]),
    ]

    # --- rama NO: el round robin no asignó a nadie ---
    f_notif, f_tag = nid(), nid()
    rama_fallo = [
        {**n_notif(f_notif, "⚠️ Round robin no asignó — lead sin dueño",
                   "El lead {{contact.name}} ({{contact.phone}}) quedó CALIFICADO pero sin asesor. "
                   "Revisar disponibilidad del round robin y asignarlo a mano.",
                   usuario=SUPERVISORA, tipo_user="specific_user"),
         "next": f_tag},
        n_tag(f_tag, [TAG_FALLO]),
        # OJO: aquí NO se pone bot-silenciado a propósito. Si nadie tomó el lead,
        # el bot sigue vivo para que el lead no quede hablando solo.
    ]

    ramas = arbol([("Asesor asignado", [cond_has_value(K_ASESOR)], rama_ok)],
                  none_next=rama_fallo)
    header = ramas[0]["id"]

    return [
        n_update(n_calif, [(K_CALIF, "Sí"), (K_F_CALIF, "currentDate")], nxt=n_oppc,
                 name="Calificado = Sí + Fecha"),
        n_opp(n_oppc, ST["calificado"], nxt=n_asig, name="Oportunidad → Calificado",
              extra={"opportunity_source": "{{contact.fuente}}"}),
        {"id": n_asig, "order": 0, "attributes": assign_node_attrs,
         "name": "Round Robin (6 asesores)", "type": "assign_user", "next": n_wt},
        n_wait(n_wt, 1, "minutes", nxt=n_upd),
        n_update(n_upd, [(K_ASESOR, "{{user.name}}"), (K_F_ASIGNA, "currentDate")],
                 nxt=header, name="Asesor + Fecha EN EL CONTACTO"),
    ] + ramas


def main():
    d = C.request("GET", f"/workflow/{LOC}/{WID}")
    if not d or d.get("_error"):
        sys.exit(f"ABORT: no pude leer SP06 -> {d}")
    viejo = (d.get("workflowData") or {}).get("templates") or []
    assign = next((n["attributes"] for n in viejo if n["type"] == "assign_user"), None)
    if not assign:
        sys.exit("ABORT: no encontré el nodo assign_user en SP06, no invento el round robin")
    print(f"SP06 actual: {len(viejo)} nodos · status={d.get('status')}")

    templates = construir(assign)
    body = {"name": d.get("name"), "version": d.get("version"), "parentId": d.get("parentId"),
            "status": "draft",                       # regla 2: nada publicado sin revisión humana
            "workflowData": {"templates": templates}}
    r = C.request("PUT", f"/workflow/{LOC}/{WID}", body)
    print("PUT:", "OK" if r and not r.get("_error") else r)

    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    tpl = (v.get("workflowData") or {}).get("templates") or []
    print(f"VERIFY: {len(tpl)} nodos · status={v.get('status')}")
    return tpl


if __name__ == "__main__":
    main()
