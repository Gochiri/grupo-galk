"""SP06 deja de confiar en quien lo llama — v2.

QUÉ PASÓ (15-ago, contacto x6H97utgqcqKL7tlbzcR)
------------------------------------------------
BOT-01 tiene una acción *Trigger a Workflow* llamada "Marcar lead calificado", con esta
condición de inicio escrita a mano:

    "Cuando ya tengas guardados los tres datos: curso, modalidad y sede. No antes.
     Si falta alguno, no ejecutes: sigue conversando hasta completarlos."

El bot la ejecutó igual, con los tres campos VACÍOS. Y es esperable: esa condición no es
una validación, es una frase que interpreta el modelo. El bot creía tener los datos porque
él mismo los había dicho en su texto — pero *Contact Info* extrae de lo que dice la
persona, no de lo que escribe el bot. Además la acción usa `add_to_workflow`, o sea que se
salta el trigger propio de SP06 (`Tag Added: galk-bot-calificado`).

POR QUÉ LA v1 DE ESTA GUARDA NO SERVÍA
--------------------------------------
La v1 metió los tres campos en el if/else de entrada, que ya traía `assigned_to has_value`.
Pero ese if/else **ya no cortaba**: Oliver le había colgado un nodo `Go to` que salta a
"Calificado = Sí + Fecha", o sea a la misma cadena que la rama else. Las dos ramas
terminaban en el mismo sitio y la guarda era decorativa.

Y el `Go to` estaba bien puesto, por una razón real: el plugin de pruebas que conecta
WhatsApp por SMS **solo funciona si el contacto tiene un usuario asignado** — si no, da
error al responder. O sea que en pruebas *todos* los contactos tienen asesor, `assigned_to
has_value` se cumplía siempre y SP06 moría antes de empezar. El `Go to` era el parche.

EL ARREGLO (v2)
---------------
El problema es que la guarda mezclaba dos cosas distintas:

  · "faltan datos"      → tiene que cortar SIEMPRE, sin excepción
  · "ya tiene asesor"   → anti-reproceso, pero choca de frente con el plugin

Así que se cambia el marcador de anti-reproceso. En vez de `assigned_to` — que el plugin
llena de entrada — se usa **`Calificado`**, que es lo primero que escribe SP06 cuando de
verdad procesa un lead. El plugin no lo toca, así que ya no hace falta el `Go to`.

    NO calificar si:  Calificado ya tiene valor      (ya se procesó)
                  O   Curso de interés está vacío
                  O   Modalidad está vacía
                  O   Sede está vacía

Un solo nodo de condición, sin anidar nada, y la rama vuelve a ser un callejón sin salida.
Se comprueban los campos **canónicos**, no los gemelos de texto del bot, así que la guarda
verifica de paso que WF-NORM y WF-MOD ya hicieron su parte.

PENDIENTE CONOCIDO
------------------
WF-SWITCH limpia los 10 campos de interés cuando el lead cambia de familia, pero NO limpia
`Calificado`. Así que un lead ya calificado que cambia de familia no se puede recalificar.
No es una regresión — con `assigned_to` pasaba lo mismo y peor, porque el dueño no se
limpia nunca. Se decide aparte, porque recalificar implica mover la oportunidad hacia atrás
y volver a pasar por el round robin.
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, nid

WID = "84811c16-30d8-4c08-a05d-0c12fa46567d"
RAMA = "No calificar (ya procesado o faltan datos)"

MARCADOR = "contact.calificado"                       # lo escribe SP06, el plugin no lo toca
REQUERIDOS = ["contact.curso_de_inters", "contact.modalidad", "contact.sede"]


def cond(field_key, operador):
    """has_value / has_no_value van SIN conditionValue. Verificado en WF1 y en LS01/SP05."""
    return {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(field_key),
            "conditionOperator": operador, "__conditionId": nid(), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": wf_lib.NESTED, "allowIsOperatorTypes": wf_lib.ALLOWIS}


def main():
    d = C.request("GET", f"/workflow/{LOC}/{WID}")
    if not d or d.get("_error"):
        sys.exit(f"ABORT: no pude leer SP06 -> {d}")
    tpl = (d.get("workflowData") or {}).get("templates") or []
    estado = d.get("status")
    print(f"SP06: {len(tpl)} nodos · status={estado} · version={d.get('version')}")

    head = next((n for n in tpl if n.get("nodeType") == "condition-node"), None)
    if not head:
        sys.exit("ABORT: no encontré el if/else de entrada, no invento la estructura")
    brs = (head.get("attributes") or {}).get("branches") or []
    if len(brs) != 1:
        sys.exit(f"ABORT: esperaba 1 rama en la guarda, hay {len(brs)}. Revisar a mano.")
    bid = brs[0]["id"]

    quiero = [(MARCADOR, "has_value")] + [(k, "has_no_value") for k in REQUERIDOS]
    actual = {(c.get("conditionSubType"), c.get("conditionOperator"))
              for c in brs[0]["segments"][0]["conditions"]}
    hijos = [n for n in tpl if n.get("parentKey") == bid]

    if actual == {(wf_lib.FID(k), op) for k, op in quiero} and not hijos:
        print("La guarda ya está como debe. Nada que hacer (idempotencia §3).")
        return

    # 1. condiciones nuevas, unidas por OR
    brs[0]["name"] = RAMA
    brs[0]["operator"] = "or"
    brs[0]["segments"][0]["operator"] = "or"
    brs[0]["segments"][0]["conditions"] = [cond(k, op) for k, op in quiero]

    # 2. la rama vuelve a ser callejón sin salida: fuera el Go to
    for n in tpl:
        if n["id"] == bid:
            n.pop("next", None)
    quitados = [n["name"] for n in hijos]
    tpl = [n for n in tpl if n.get("parentKey") != bid]

    r = C.request("PUT", f"/workflow/{LOC}/{WID}",
                  {"name": d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"),
                   "status": estado,                  # se respeta como estaba, no se despublica
                   "workflowData": {"templates": tpl}})
    print("PUT:", "OK" if r and not r.get("_error") else r)
    if quitados:
        print("  nodos quitados de la rama:", ", ".join(quitados))

    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    vh = next(n for n in vt if n.get("nodeType") == "condition-node")
    vb = vh["attributes"]["branches"][0]
    byid = {f["id"]: f["name"] for f in wf_lib._cf.values()}
    print(f"VERIFY: {len(vt)} nodos · status={v.get('status')}")
    print(f"  rama '{vb['name']}' (operador {vb['segments'][0]['operator']}) "
          f"-> next={next((n.get('next') for n in vt if n['id'] == vb['id']), None)}")
    for c in vb["segments"][0]["conditions"]:
        st = c.get("conditionSubType")
        print(f"    · {byid.get(st, st)} {c.get('conditionOperator')}")


if __name__ == "__main__":
    main()
